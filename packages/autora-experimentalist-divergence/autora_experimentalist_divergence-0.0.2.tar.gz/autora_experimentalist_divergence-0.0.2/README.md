# AutoRA Divergence Experimentalist

The divergence experimentalist identifies experimental conditions $\vec{x}' \in X'$ with respect the
distance between existing experimental data $\vec{x}, $\vec{y} and data predicted by a model 
$\vec{x_pool}, $\vec{y_pred}:

$$
\underset{\vec{x}'}{\arg\max}~sum(d((\vec{x}, \vec{y}), (\vec{x_pool}, \vec{y_pred}))
$$

The aim of this experimentalist is to combine novelty and uncertainty by using a distance that
combines both: The distance between existing conditions to new conditions and the distance of 
existing observations to predictions.
