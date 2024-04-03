# AutoRA Divergence Experimentalist

The divergence experimentalist identifies experimental conditions $\vec{x}' \in X'$ with respect the
distance between existing experimental data $\vec{x}, $\vec{y} and data predicted by a model 
$\vec{x_pool}, $\vec{y_pred}:

$$
\underset{\vec{x}'}{\arg\max}~sum(d((\vec{x}, \vec{y}), (\vec{x_pool}, \vec{y_pred}))
$$
