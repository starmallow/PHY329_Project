> The idea I'm thinking of for the readme file is the overview of the project, while the demo.ipynb provides and interactive view of the code and effects of paramaters

# Title: (Exploring the Nagel-Schreckenberg Traffic Model)

## Installation Instructions
==This. (prob include needing numpy and matplotlib ?)==


## Background / Problem Motivation?

== Add background info from the presentation ==

(old proposal intro:)
We are implementing the Nagel-Schreckenberg traffic cellular automaton model to simulate a single lane of traffic, studying the onset of congestion with respect to car density. We plan to build upon this model and explore the impact of simultaneous lanes of traffic.

Sources include this [model outline](https://en.wikipedia.org/wiki/Nagel%E2%80%93Schreckenberg_model).

== Add professional/APS citation of the research paper: https://hal.science/jpa-00246697/document ==


## Governing Rules

The Nagel-Schleckenberg traffic model is defined by four rules that govern the movement of "cars" through the simulation. These rules account for normal traffic movement as well as adding in potential human factors that make this model much more life-like and accurate. The rules, which are all followed simulataneously as the model progresses, are as follows:
1. Cars that aren't at their maximum velocity ($v ≠ v_{max}$) and have adequate space in front of them ($d$ > $v + 1$) will increase their speed by one.
2. If the distance to the next car $d < v$, then $v$ is reduced by one unit.
3. For any moving vehicle (vehicles with v > 0), there is a braking probability $p$ that the velocity will be randomly decreased by one unit.
4. All cars move forward by $v$ cells.

The third rule is what accounts for the human aspect of traffic creation. People get distracted, overreact to brake lights, see obstructions in the road, etc. and that’s often how traffic gets started.

## Circular vs. Bottleneck Systems

The base Nagel-Schreckenberg model can be used in a variety of circumstances and with a variety of conditions. For this particular project, the circular and bottleneck N-S systems were examined.

### Circular System

The circular or infinite loop version of the model is defined mainly by the density of cars on the road, think "racetrack". This density can be altered to simulate different traffic conditions. Because the loop is closed, the density remains constant throughout the entirety of the simulation. This version of the model eliminates "edge effects" like traffic lights, car crashes, and other anomalies entering and leaving the system, it purely isolates traffic jam formation due to driver interactions and braking/accelerating.

You start by inputting a fixed density $\rho$ where $\rho = {N \over L} = {Number\ of\ cars\ \over Number\ of\ cells}$, as well as the number of cells you want in your traffic loop. Then, the cars are randomly placed throughout the lane with an initial velocity $v = 0$.

### Bottleneck System

The bottleneck or open system simulates a non-constant density situation. The boundary conditions of the system are redefined to create open boundaries. The model adds cars on the left when a space opens up, and deletes cars on the right when they've reached their "destination". This simulates bottleneck situations like a reduction in speed limit in a particular part of a road. Once the cars get past this bottleneck, they are opened up into free flow again. Where the circular system studies how "phantom" traffic jams are formed, this system studies how differing road conditions and restrictions limit the flow of traffic.

As with the circular system, the cars added to the left side begin with an initial velocity $v=0$, and the same rules from above apply with the addition of the bottleneck condition.


## Results
== example of a couple of the most important kinds of plot demonstrations. == \
 - save the image of these plots in results/plots.py and import them into here?
== include how we calculated the density and flow (same equations in the paper) ? ==


## (future directions, applications, connections to other interesting ideas)



## Directory:

`demo.ipynb` overviews the project; introduces the problem, explores the base model relation of traffic and density with plots, and demonstrates the expanded lane model

`src/nsmodel.py` implements the base (circular) Nagel-Schreckenberg cellular automaton model and the additional bottleneck model

`src/lanes.py` builds upon the Nagel-Schreckenberg model by adding simultaneous lanes

`results/plots.py` initializes the plots to demonstrate the models with varied car density, randomization factors, and traffic lanes

`results/analysis.py` implements the functions for analyzing the models


## Project Member Contributions:

**<ins>Kristine Anderson</ins>** implemented the base Nagel-Schreckenberg model, led the model simulation/plotting, and co-led the demo notebook.

**<ins>Srija Lahiri</ins>** implemented the bottleneck Nagel-Schreckenberg model and co-led the demo notebook.

**<ins>Nathan Safranek</ins>** assisted in the model simulation/plotting and led the README.md file.
