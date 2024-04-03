"""
Example Experimentalist
"""
import numpy as np
import pandas as pd

from typing import List
from autora.variable import VariableCollection, Variable
from autora.experimentalist import grid, random
from sklearn.linear_model import LinearRegression


def sample(
        variables: VariableCollection,
        conditions: pd.DataFrame,
        experiment_data: pd.DataFrame,
        models: List,
        normalize: bool = True,
        num_samples: int = 1) -> pd.DataFrame:
    """
    Samples based on the optimal divergence.
        Divergence is the distance between predicted experiment data and existing experiment data
        For each condition of the pool the summed distance between the vector (X_cond, y_pred) and
        each (X_existing, y_existing) is calculated. The vector with the highest summed distance is
        chosen first. This vector is then added to the existig experiment data and the new summed
        distances are calculated to optain the second-best vector. This process is repeated until
        the number of samples is reached.

    Args:
        variables: The variable definitions
            Attention: `variables` is a field of the standard state
        conditions: The pool to sample from.
            Attention: `conditions` is a field of the standard state
        experiment_data: The data that has already been conducted
            Attention: `expoeriment_data` is a field of the standard state
        models: The sampler might use output from the theorist.
            Attention: `models` is a field of the standard state
        normalize: Indicates weather to normalize the variables before calculating the divergence
        num_samples: number of experimental conditions to select

    Returns:
        Sampled pool of experimental conditions

    Examples:
        Declare the variables:
        >>> x_1 = Variable(name='x_1', value_range=(0, 100), allowed_values=np.linspace(0, 100, 10))
        >>> x_2 = Variable(name='x_2', value_range=(0, 1), allowed_values=np.linspace(0, 1, 10))
        >>> y = Variable(name='y', value_range=(0,2))
        >>> v_collection = VariableCollection(
        ...     independent_variables=[x_1, x_2], dependent_variables=[y]
        ...     )

        Create a pool:
        >>> pool = grid.pool(v_collection)
        >>> pool
              x_1       x_2
        0     0.0  0.000000
        1     0.0  0.111111
        2     0.0  0.222222
        3     0.0  0.333333
        4     0.0  0.444444
        ..    ...       ...
        95  100.0  0.555556
        96  100.0  0.666667
        97  100.0  0.777778
        98  100.0  0.888889
        99  100.0  1.000000
        <BLANKLINE>
        [100 rows x 2 columns]

        We create a random set for the experiment data. First randomly sample conditiont
        >>> experiment_data_random = random.sample(pool, 5, 42)
        >>> experiment_data_random
                  x_1       x_2
        83  88.888889  0.333333
        53  55.555556  0.333333
        70  77.777778  0.000000
        45  44.444444  0.555556
        44  44.444444  0.444444

        Randomly add y's to the sample as experiment data
        >>> np.random.seed(42)
        >>> experiment_data_random['y'] = 2 * np.random.random(
        ...     size=len(experiment_data_random)
        ...     )
        >>> experiment_data_random
                  x_1       x_2         y
        83  88.888889  0.333333  0.749080
        53  55.555556  0.333333  1.901429
        70  77.777778  0.000000  1.463988
        45  44.444444  0.555556  1.197317
        44  44.444444  0.444444  0.312037

        Create a linear regressor as model
        >>> model = LinearRegression()
        >>> X = np.array(experiment_data_random[['x_1', 'x_2']])
        >>> Y = np.array(experiment_data_random[['y']])
        >>> X
        array([[88.88888889,  0.33333333],
               [55.55555556,  0.33333333],
               [77.77777778,  0.        ],
               [44.44444444,  0.55555556],
               [44.44444444,  0.44444444]])

        >>> Y
        array([[0.74908024],
               [1.90142861],
               [1.46398788],
               [1.19731697],
               [0.31203728]])

        Fit the model
        >>> model.fit(X, Y)
        LinearRegression()

        Sample new conditions
        >>> sample(variables=v_collection, conditions=pool,
        ...        experiment_data=experiment_data_random, models=[model],
        ...        num_samples=5)
                  x_1  x_2
        0  100.000000  1.0
        1    0.000000  0.0
        2    0.000000  1.0
        3   88.888889  1.0
        4   11.111111  0.0

        Without normalization:
        >>> sample(variables=v_collection, conditions=pool,
        ...        experiment_data=experiment_data_random, models=[model],
        ...        num_samples=5, normalize=False)
             x_1       x_2
        0    0.0  0.000000
        1    0.0  1.000000
        2  100.0  1.000000
        3    0.0  0.111111
        4  100.0  0.000000

    """
    # If there is no model or experiment data, return a random sample
    if not models or experiment_data is None or len(experiment_data) == 0:
        return random.sample(conditions=conditions, num_samples=num_samples)

    _pred = conditions.copy()
    _real = experiment_data.copy()
    latest_model = models[-1]
    y_predict = latest_model.predict(np.array(conditions))
    _pred[variables.dependent_variables[0].name] = y_predict
    result = pd.DataFrame()

    if normalize:
        for v in variables.independent_variables + variables.dependent_variables:
            _pred[v.name] -= v.value_range[0]
            _pred[v.name] /= (v.value_range[1] - v.value_range[0])
            _pred[v.name] /= len(variables.independent_variables)
            _real[v.name] -= v.value_range[0]
            _real[v.name] /= (v.value_range[1] - v.value_range[0])
            _real[v.name] /= len(variables.independent_variables)

    for _ in range(num_samples):
        summed_distances = _pred.apply(lambda row: _calculate__distances(row, _real), axis=1)
        max_dist_index = summed_distances.idxmax()
        _row = _pred.loc[[max_dist_index]]
        _pred = _pred.drop(max_dist_index)
        _real = pd.concat([_real, _row], ignore_index=True)
        result = pd.concat([result, _row], ignore_index=True)

    if normalize:
        for v in variables.independent_variables + variables.dependent_variables:
            result[v.name] *= len(variables.independent_variables)
            result[v.name] *= (v.value_range[1] - v.value_range[0])
            result[v.name] += v.value_range[0]

    return result[[iv.name for iv in variables.independent_variables]]


def _calculate__distances(row, df2):
    # Calculate Euclidean distances from the row to all rows in df2
    distances = np.sqrt(((df2 - row) ** 2).sum(axis=1))
    # Return the sum of these distances
    return distances.sum()
