from typing import List

import numpy as np


class Individual:
    def __init__(self, start_infection_probability: float = 0.01, infection_probability: float = 0.8) -> None:
        self.LAT_RANGE = [50.031, 50.091]
        self.LON_RANGE = [19.858, 20.008]
        self.INFECTION_RADIUS = 0.0002

        # note: start individual position
        # 250x100
        self.lat = np.random.uniform(self.LAT_RANGE[0], self.LAT_RANGE[1])
        self.lon = np.random.uniform(self.LON_RANGE[0], self.LON_RANGE[1])
        # --- end note

        # note: infection probability part
        self.start_infection_probability = start_infection_probability
        self.infection_probability = infection_probability
        self.infected = np.random.choice([True, False],
                                         p=[self.start_infection_probability, 1 - self.start_infection_probability])
        # --- end note

    def move(self) -> None:
        """
        Make a move with individual. Moves are generated with some probability.
        This should be a standard move. Some could implement other moves for specific scenario.
        """
        if self.LAT_RANGE[1] <= self.lat <= self.LAT_RANGE[1] + 0.005:
            self.lat += np.random.uniform(-0.0002, -0.0001)

        elif self.LAT_RANGE[0] - 0.005 <= self.lat <= self.LAT_RANGE[0]:
            self.lat += np.random.uniform(0.0001, 0.0002)

        else:
            self.lat += np.random.uniform(-0.0002, 0.0002)

        if self.LON_RANGE[1] <= self.lon <= self.LON_RANGE[1] + 0.005:
            self.lon += np.random.uniform(-0.0002, 0.0001)

        elif self.LON_RANGE[0] - 0.005 <= self.lon <= self.LON_RANGE[0]:
            self.lon += np.random.uniform(0.0001, 0.0002)

        else:
            self.lon += np.random.uniform(-0.0002, 0.0002)

    def check_infection(self, individuals: List['Individual']) -> None:
        """
        Check if this individual is in infection range, if it is,
        apply some probability (self.infection_probability) to get infection.

        Parameters
        ----------
        individuals: List[Individual], required
            List with all other individuals that are alive. We will be searching for individuals in range and infected.

        """
        for individual in individuals:
            if (individual.infected and np.sqrt((self.lat - individual.lat)**2 + (self.lon - individual.lon)**2) - self.INFECTION_RADIUS <= 0 and
                    np.random.choice([True, False], p=[self.infection_probability, 1 - self.infection_probability])):
                self.infected = True
                break
