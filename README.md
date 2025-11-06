<<<<<<< HEAD
# Exploring the Nagel-Schreckenberg Traffic Model
=======
The Nagel-Schreckenberg Traffic Model

>>>>>>> 15dd97147b4ba2d23b856b29a04a3766f483ead7

We are implementing the Nagel-Schreckenberg traffic cellular automaton model to simulate a single lane of traffic, studying the onset of congestion with respect to car density. We plan to build upon this model and explore the impact of simultaneous lanes of traffic.

Sources include this [model outline](https://en.wikipedia.org/wiki/Nagel%E2%80%93Schreckenberg_model)


<<<<<<< HEAD
# Planned Directory:

`demo.ipynb` overviews of the project; introduces the problem, explores the base model relation of traffic and density with plots, and demonstrates the expanded lane model

`src/nsmodel.py` implements the Nagel-Schreckenberg cellular automaton model

`src/lanes.py` builds upon the Nagel-Schreckenberg model by adding simultaneous lanes

`results/plots.py` demonstrates the models with varied car density, randomization factors, and traffic lanes
=======
Description: The problem we are solving is the Nagel-Schreckenberg traffic model. This model simulates freeway traffic as a function of car density, so our solution should accurately depict and simulate traffic at different levels of car density. We may explore traffic modeling more by adding/deleting lanes of traffic, obstacles, etc. to simulate real-time road conditions.
>>>>>>> 15dd97147b4ba2d23b856b29a04a3766f483ead7


# Timeline

- Code the cellular automaton for the Nagel-Schreckenberg base case of a single lane of cars that cycle through four actions: acceleration, slowing down, randomization, and car motion.
- Explore the base model with simulations.
  - Plot the road evolution over time to demonstrate traffic congestion
  - Evaluate the average car velocity with respect to the car density
  - Vary the deceleration probability. Plot the point of sudden traffic jams (slope discontinuity) as a function of the deceleration probability
- Introduce complexity to the model, e.g. additional lanes of traffic.
  - Investigate the effect on the relationship between average car velocity, car density, deceleration probability, and the onset of traffic jams.

- demo.ipynb: an overview of the projecting, starting from introducing the problem, identifying the base model relating traffic and density, highlighting the relationship through various fine-tuned plots, and expanding the plot to further questions and features to be studied

<<<<<<< HEAD
# Project Member Contributions:
=======
- src/density.py: implements the Nagel-Schreckenberg model with the division of cells

- src/plots.py: creates visuals of the traffic models

- src/extras.py: implements the cellular automaton model while exploring different cell divisions to reproduce traffic jams 
>>>>>>> 15dd97147b4ba2d23b856b29a04a3766f483ead7

**<ins>Kristine Anderson</ins>** will lead the model simulation/plotting, create the demos notebook, and assist in implementing all models

**<ins>Srija Lahiri</ins>** will implement the base Nagel-Schreckenberg model

<<<<<<< HEAD
**<ins>Nathan Safranek</ins>** will implement expanded models (i.e. additional lanes)
=======
    * 


Team Member Contributions:
    
    Kristine Anderson:
        * will lead implementation of the different plots and rendering of example videos

    Srija Lahiri:
        * will implement the generic model of the relationship between car density and traffic jams for future plots and unit tests to build on

    Nathan Safranek: 
        * will implement unit tests of how modifying different features (i.e. adding a lane) effects the onset of traffic jams



Additional Notes:
>>>>>>> 15dd97147b4ba2d23b856b29a04a3766f483ead7
