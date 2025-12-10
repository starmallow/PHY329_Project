# Exploring the Nagel-Schreckenberg Traffic Model

We are implementing the Nagel-Schreckenberg traffic cellular automaton model to simulate a single lane of traffic, studying the onset of congestion with respect to car density. We plan to build upon this model and explore the impact of simultaneous lanes of traffic.

Sources include this [model outline](https://en.wikipedia.org/wiki/Nagel%E2%80%93Schreckenberg_model).


# Planned Directory:

`demo.ipynb` overviews the project; introduces the problem, explores the base model relation of traffic and density with plots, and demonstrates the expanded lane model

`src/nsmodel.py` implements the Nagel-Schreckenberg cellular automaton model

`src/lanes.py` builds upon the Nagel-Schreckenberg model by adding simultaneous lanes

`results/plots.py` demonstrates the models with varied car density, randomization factors, and traffic lanes


# Timeline

- Code the cellular automaton for the Nagel-Schreckenberg base case of a single lane of cars that cycle through four actions: acceleration, slowing down, randomization, and car motion.
- Explore the base model with simulations.
  - Plot the road evolution over time to demonstrate traffic congestion.
  - Evaluate the average car velocity with respect to the car density.
  - Vary the deceleration probability. Plot the point of sudden traffic jams (slope discontinuity) as a function of the deceleration probability.
- Introduce complexity to the model, e.g. additional lanes of traffic.
  - Investigate the effect on the relationship between average car velocity, car density, deceleration probability, and the onset of traffic jams.


# Project Member Contributions:

**<ins>Kristine Anderson</ins>** will lead the model simulation/plotting, create the demo notebook, and assist in implementing all models.

**<ins>Srija Lahiri</ins>** will implement the base Nagel-Schreckenberg model.

**<ins>Nathan Safranek</ins>** will implement expanded models (i.e. additional lanes).
