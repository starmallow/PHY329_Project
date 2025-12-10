# The base Nagel-Schreckenberg cellular automaton models.


import numpy as np


class TrafficModelCircular:
    """
    Base implementation of the Nagel–Schreckenberg cellular automata model of a single 
    traffic lane. Uses periodic boundary conditions to create a circular, closed system.

    Parameters:
        cars (int): The total number of cars in the system. Cannot be greater than the
            number of cells.
        cells (int): The number of cells in the traffic lane, which can be occupied 
            by 0 or 1 car.
        v_max (int): Speed limit of the traffic system.
        p (float): Probability factor for random decceleration events. Float must 
            be between 0 and 1.
        t0 (int): Initial number of timesteps to run the system through to reach a 
            state of equilibrium before data collection starts. If None, 10 * cells 
            is used.
        random_state (None or int): The seed for the random number generator. If None,
            the random number generator is not seeded.
        initial_state (None or array): The initial state of the system. If None, a 
            random initial state is used.
        
    """
    def __init__(self, cars, cells=100, v_max=5, p=0.5, t0=None, random_state=None, initial_state=None):
        if cars > cells:
            raise ValueError("Number of cars cannot exceed total cells in the system.")
        # add more input error checks, like int data types
        self.cars = cars
        self.cells = cells
        self.v_max = v_max
        self.p = p

        self.random_state = random_state
        np.random.seed(random_state)

        # The system is a 1D array of integers, with -1 representing empty cells.
        #   Cars start with velocity of 0.
        if initial_state is None:
            state = np.full(cells, -1, int)
            car_indices = np.random.choice(cells, cars, replace=False)
            state[car_indices] = 0
            self.initial_state = state
        
        else:
            if len(initial_state) != cells:
                raise IndexError("Initial state must be consistent with system paramenters.")
            self.initial_state = initial_state
        
        self.state = self.initial_state
        self.initial_equilibrium(t0)
        self.history = [self.state]  # History starts saving after equilibrium


    def initial_equilibrium(self, t0):
        """
        Run the system through t0 time steps to reach an initial point of equilibrium,
        after which data collection starts.
        """
        if t0 == None:
            t0 = 10 * self.cells
        for i in range(t0):
            self.state = self.next_state()

    def simulate(self, n_steps):
        """
        Iterate the dynamics for n_steps, and return the results as an array.
        """
        for i in range(n_steps):
            self.state = self.next_state()
            self.history.append(self.state)
        return self.state
    
    def next_state(self):
        """
        Compute the next state of the circular, closed system.
        """
        # Finding distances between cars
        car_indices = np.asarray(self.state > -1).nonzero()[0]  # need to select 0 index to avoid tuple
        d_next_car = np.roll(car_indices, -1)
        d_next_car[-1] += self.cells
        d_next_car -= car_indices

        # Step 1: Acceleration
        v_cars = self.state[car_indices]
        v_accel = np.where((v_cars < self.v_max) & (v_cars + 1 < d_next_car), 
                     v_cars + 1, v_cars)

        # Step 2: Slowing Down
        v_deccel = np.where(v_accel >= d_next_car, d_next_car - 1, v_accel)

        # Step 3: Randomization
        rand_cars = np.random.choice(2, size=len(car_indices), p=[1-self.p, self.p])
        v_rand = np.where(rand_cars & (v_deccel > 0), v_deccel - 1, v_deccel)

        # Step 4: Car Motion
        car_indices += v_rand
        car_indices = np.where(car_indices < self.cells, car_indices, car_indices - self.cells)
        next_state_arr = np.full(self.cells, -1, int)
        next_state_arr[car_indices] = v_rand

        return next_state_arr
    

class TrafficBottleneck(TrafficModelCircular):
    """
    A modification of the circular Nagel–Schreckenberg model using an open boundary
    system. Cars enter the leftmost cell when empty, and cars passing the rightmost
    cell exit the system.

    Parameters:
        cars (int): The total number of cars in the system. Cannot be greater than the
            number of cells.
        cells (int): The total number of cells in the traffic lane. The road has open boundaries
            for the bottleneck model, but the number of discrete cells is held constant.
        v_max (int): The maximum velocity for cars outside the bottleneck.
        p (float): The natural breaking probability used in the NS model.
        t0 (int): The number of initial time steps to run to reach equilibrium before recording data.
            If None, defaults to 10 * cells.
        random_state (int): The seed for NumPy's random number generator. If None, the random number
            generator is not seeded.
        initial_state (array): The initial configuration of the system. If None, cars are placed
            randomly.

        bn_start (int or None): The starting cell index of the bottleneck region. If None, no bottleneck
            region is used.
        bn_end (int or None): The ending cell index of the bottleneck. If None, there is no bottleneck.
        v_max_bn (int): The maximum veolcity inside the bottleneck region.
        inflow (float): The probability that a new car enters the traffic lane at index 0 when that cell
            is empty.
    """

    def __init__(self, cars, cells=100, v_max=5, p=0.5, t0=None, random_state=None, 
                 initial_state=None, bn_start=None, bn_end=None, v_max_bn=1, inflow=0.5):

        # Extra bottleneck parameters
        self.bn_start = bn_start
        self.bn_end = bn_end
        self.v_max_bn = v_max_bn
        self.inflow = inflow

        # Call the parent class's __init__ method
        super().__init__(cars=cars, cells=cells, v_max=v_max, p=p, t0=t0, 
                         random_state=random_state, initial_state=initial_state)

    def next_state(self):
        """
            To compute the next state of each car according to the 4-step rule of the NS model
            for an open-boundary system with a bottleneck region.
        """
        state = self.state
        cells = self.cells
        p = self.p

        # Identifying where cars are in the traffic lane.
        car_indices = np.asarray(state > -1).nonzero()[0]
        next_state_arr = np.full(cells, -1, int)

        # Checking for a special case of no cars on the road.
        if len(car_indices) == 0:
            if np.random.rand() < self.inflow:
                next_state_arr[0] = 0
            return next_state_arr

        # Finding distance between the cars.
        d_next_car = np.empty(len(car_indices), int)

        if len(car_indices) == 1:
            d_next_car[0] = self.v_max + 1
        else:
            d_next_car[:-1] = car_indices[1:] - car_indices[:-1]
            d_next_car[-1] = self.v_max + 1

        # Determining v_max of each car: applying v_max if the car is outside the bottlenck, and v_max_bn for cars inside it.
        if self.bn_start is None:
            v_local = np.full(len(car_indices), self.v_max)
        else:
            in_bn = (car_indices >= self.bn_start) & (car_indices <= self.bn_end)
            v_local = np.where(in_bn, self.v_max_bn, self.v_max)

        v_cars = state[car_indices]

        # Step 1: Acceleration
        v_accel = np.where(v_cars < v_local, v_cars + 1, v_cars)

        # Step 2: Slowing down
        v_decel = np.where(v_accel >= d_next_car, d_next_car - 1, v_accel)
        v_decel = np.maximum(v_decel, 0)

        # Step 3: Randomization
        rand_mask = np.random.rand(len(car_indices)) < p
        v_rand = np.where(rand_mask & (v_decel > 0), v_decel - 1, v_decel)

        # Step 4: Car Motion
        new_positions = car_indices + v_rand
        valid = new_positions < cells
        new_positions = new_positions[valid]
        new_velocities = v_rand[valid]

        next_state_arr[new_positions] = new_velocities

        # Applying inflow at the left-most cell
        if next_state_arr[0] == -1 and np.random.rand() < self.inflow:
            next_state_arr[0] = 0

        return next_state_arr
