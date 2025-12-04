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
        next_state = np.full(self.cells, -1, int)
        next_state[car_indices] = v_rand

        return next_state
    



class TrafficBottleneck(TrafficModelCircular):
    """
    A modification of the circular Nagel–Schreckenberg model using an open boundary 
    system. Cars enter the leftmost cell when empty, and cars passing the rightmost 
    cell exit the system.

    Parameters:
        cars (int): The total number of cars in the system. Cannot be greater than the
            number of cells.
        **kwargs: Additional keyword arguments passed to the base TrafficModelNS class.
    """

    def __init__(self, cars, **kwargs):
        # Call the parent class's __init__ method
        super().__init__(cars, **kwargs)

    def next_state(self):
        """
        Output the next state of the system.
        """

        # to be continued ...

        raise NotImplementedError

