# Functions for plotting and analyzing the models

import sys
sys.path.append('../code/')
from nsmodel import *

import numpy as np
import matplotlib.pyplot as plt




def SpaceTimePlot(cells, system_density, timesteps, bottleneck=False,
                        random_state=None, save_file_name="", 
                        v_max=5, p=0.5, t0=None, initial_state=None,
                        bn_start=None, bn_end=None, v_max_bn=1, inflow=0.5):
    """
    Function to streamline creation of the time evolution plots of the traffic lane 
    cells from the Nagel–Schreckenberg models. Displays the plot in jupyter notebook. 
    Optionally saves the .jpg file.

    Parameters:
        cells (int): The number of cells in the traffic lane, which can be occupied 
            by 0 or 1 car.
        system_density (float): The total density of cars in the system. The number 
            of cars passed to the traffic model will equal int(system_density * cells).
            Float must be between 0 and 1.
        timesteps (int): The number of timesteps to simulate for data collection.
        random_state (None or int): The seed for the random number generator. If None,
            the random number generator is not seeded.
        
        save_file_name (str): Name of the .jpg file, if saving the plot. If unnamed,
            the plot won't be saved.


        v_max (int): Speed limit of the traffic system.
        p (float): Probability factor for random decceleration events. Float must 
            be between 0 and 1.
        t0 (int): Initial number of timesteps to run the system through to reach a 
            state of equilibrium before data collection starts. If None, 10 * cells 
            is used.
        initial_state (None or array): The initial state of the system. If None, a 
            random initial state is used.

        bn_start (int or None): The starting cell index of the bottleneck region. If None, no bottleneck
            region is used.
        bn_end (int or None): The ending cell index of the bottleneck. If None, there is no bottleneck.
        v_max_bn (int): The maximum veolcity inside the bottleneck region.
        inflow (float): The probability that a new car enters the traffic lane at index 0 when that cell
            is empty.
    """


    cars = int(system_density * cells)

    if bottleneck:
        model = TrafficBottleneck(cars, cells=cells, v_max=v_max, p=p, t0=t0, random_state=random_state, 
                                  initial_state=initial_state, bn_start=bn_start, bn_end=bn_end, 
                                  v_max_bn=v_max_bn, inflow=inflow)
    else:
        model = TrafficModelCircular(cars, cells, v_max, p, t0, random_state, initial_state)
   
    model.simulate(timesteps)
    data = np.asarray(model.history)

    fig, ax = plt.subplots(figsize=(0.12*cells, timesteps//10), dpi=300)
    im = ax.imshow(data, cmap='Greys')

    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)

    ax.set_ylabel("Timestep", fontsize=12)
    ax.set_xlabel("Cell Index", fontsize=12)
    if bottleneck:
        ax.set_title(f"Time Evolution of Single, Bottleneck Traffic Lane", fontsize=14)
    else:
        ax.set_title(f"Time Evolution of Single, Circular Traffic Lane ($\\rho$ = {system_density})", fontsize=14)
    cbar = plt.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label(f"Car Velocity (cells/timestep)\n(-1 indicates no cars present)", fontsize=10, labelpad=1)
    cbar.ax.tick_params(labelsize=10)

    if save_file_name:
        file = save_file_name + ".jpg"
        # put the file in specific folder ?
        plt.savefig(file, format='jpg', bbox_inches='tight')
    
    plt.show()





def DensityFlowResults(cells, system_density, timesteps, bottleneck=False, 
                       random_state=None, sample_spacing=100, first_sample=50,
                       v_max=5, p=0.5, t0=None, initial_state=None,
                       bn_start=None, bn_end=None, v_max_bn=1, inflow=0.5):
    """
    Function to streamline the collection of traffic flow vs. density data from the 
    Nagel–Schreckenberg models. 
    Output: a tuple of two 1d numpy arrays; ([density], [flow])

    Parameters:
        cells (int): The number of cells in the traffic lane, which can be occupied 
            by 0 or 1 car.
        system_density (float): The total density of cars in the system. The number 
            of cars passed to the traffic model will equal int(system_density * cells).
            Float must be between 0 and 1.
        timesteps (int): The number of timesteps to simulate for data collection.
        random_state (None or int): The seed for the random number generator. If None,
            the random number generator is not seeded.

        sample_spacing (int): Steps to take between the sampled cell indices used for 
            data collection. Defaults to 100.
        first_sample (int): First index to start the sample cell selection with. 
            Defaults to 50.

        v_max (int): Speed limit of the traffic system.
        p (float): Probability factor for random decceleration events. Float must 
            be between 0 and 1.
        t0 (int): Initial number of timesteps to run the system through to reach a 
            state of equilibrium before data collection starts. If None, 10 * cells 
            is used.
        initial_state (None or array): The initial state of the system. If None, a 
            random initial state is used.

        bn_start (int or None): The starting cell index of the bottleneck region. If None, no bottleneck
            region is used.
        bn_end (int or None): The ending cell index of the bottleneck. If None, there is no bottleneck.
        v_max_bn (int): The maximum veolcity inside the bottleneck region.
        inflow (float): The probability that a new car enters the traffic lane at index 0 when that cell
            is empty.
    """

    cars = int(system_density * cells)
    if bottleneck:
        model = TrafficBottleneck(cars, cells=cells, v_max=v_max, p=p, t0=t0, random_state=random_state, 
                                  initial_state=initial_state, bn_start=bn_start, bn_end=bn_end, 
                                  v_max_bn=v_max_bn, inflow=inflow)
    else:
        model = TrafficModelCircular(cars, cells, v_max, p, t0, random_state, initial_state)

    model = TrafficModelCircular(cars, cells, v_max, p, t0, random_state, initial_state)
    model.simulate(timesteps)
    history = np.asarray(model.history)

    sample_indices = np.arange(first_sample, cells, sample_spacing)

    transpose = history.T
    occupy = np.where(transpose[sample_indices]>-1, 1, 0)
    occupy_sum = np.sum(occupy, axis=1)
    density = occupy_sum / timesteps

    flow_conditions = [transpose[sample_indices-i]>i for i in range(v_max)]
    flow = np.where(np.logical_or.reduce(flow_conditions), 1, 0)
    flow = np.sum(flow, axis=1, dtype=float)
    flow /= timesteps

    return (density, flow)





def PlotDensityFlow(cells, timesteps, bottleneck=False, save_file_name="", 
                    densities=[0.02, 0.04, 0.06, 0.08, 0.1, 0.13, 0.16, 0.2],
                    random_state=None, sample_spacing=100, first_sample=50,
                    v_max=5, p=0.5, t0=None, initial_state=None,
                    bn_start=None, bn_end=None, v_max_bn=1, inflow=0.5):
    """
    Function to streamline plotting of several runs of traffic flow vs. density data from the 
    Nagel–Schreckenberg models, with varying system densities.
    Displays the plot in jupyter notebook. Optionally saves the .jpg file.

    Parameters:
        cells (int): The number of cells in the traffic lane, which can be occupied 
            by 0 or 1 car.
        densities (list of floats): List of the total density of cars in the system for each
            data run to be plotted. The number of cars passed to the traffic model will equal 
            int(system_density * cells). Floats must be between 0 and 1.
        timesteps (int): The number of timesteps to simulate for data collection.
        random_state (None or int): The seed for the random number generator. If None,
            the random number generator is not seeded.

        save_file_name (str): Name of the .jpg file, if saving the plot. If unnamed,
            the plot won't be saved.

        sample_spacing (int): Steps to take between the sampled cell indices used for 
            data collection. Defaults to 100.
        first_sample (int): First index to start the sample cell selection with. 
            Defaults to 50.

        v_max (int): Speed limit of the traffic system.
        p (float): Probability factor for random decceleration events. Float must 
            be between 0 and 1.
        t0 (int): Initial number of timesteps to run the system through to reach a 
            state of equilibrium before data collection starts. If None, 10 * cells 
            is used.
        initial_state (None or array): The initial state of the system. If None, a 
            random initial state is used.

        bn_start (int or None): The starting cell index of the bottleneck region. If None, no bottleneck
            region is used.
        bn_end (int or None): The ending cell index of the bottleneck. If None, there is no bottleneck.
        v_max_bn (int): The maximum veolcity inside the bottleneck region.
        inflow (float): The probability that a new car enters the traffic lane at index 0 when that cell
            is empty.
    """

    # cars = (np.asarray(densities) * cells).astype(int)
    density_data = np.empty((2,))
    flow_data = np.empty((2,))

    for system_density in densities:
        dens_temp, flow_temp = DensityFlowResults(cells, system_density, timesteps, bottleneck=bottleneck, 
                                                random_state=random_state, sample_spacing=sample_spacing, 
                                                first_sample=first_sample, v_max=v_max, p=p, t0=t0, 
                                                initial_state=initial_state, bn_start=bn_start, bn_end=bn_end, 
                                                v_max_bn=v_max_bn, inflow=inflow)
        density_data = np.hstack((density_data.copy(), dens_temp.copy()))
        flow_data = np.hstack((flow_data.copy(), flow_temp.copy()))
    
    plt.figure(dpi=300)
    plt.plot(density_data, flow_data, ".k", ms=3, alpha=0.5)

    plt.ylim(0,0.45)
    plt.ylabel("Flow (car/timestep)")
    plt.xlabel("Density (cell occupancy / timestep)")

    if save_file_name:
        file = save_file_name + ".jpg"
        # put the file in specific folder ?
        plt.savefig(file, format='jpg', bbox_inches='tight')
    
    plt.show()
    