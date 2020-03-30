from typing import List

import numpy as np


class Individual:
    """
    50.097,19.822       50.097,20.033
    49.885,19.822       49.885,20.033
    """
    def __init__(self, start_infection_probability: float = 0.01, infection_probability: float = 0.8) -> None:
        # note: start individual position
        # self.x = np.random.randint(1, 1000)
        # self.y = np.random.randint(1, 1000)

        self.x = np.random.uniform(19.822, 20.033)
        self.y = np.random.uniform(49.885, 50.097)
        # --- end note

        # note: infection probability part
        self.start_infection_probability = start_infection_probability
        self.infection_probability = infection_probability
        self.infected = np.random.choice([True, False],
                                         p=[self.start_infection_probability, 1-self.start_infection_probability])
        # --- end note

    def move(self) -> None:
        """
        Make a move with individual. Moves are generated with some probability.
        This should be a standard move. Some could implement other moves for specific scenario.
        """
        # if 980 <= self.x <= 1100:
        #     self.x += np.random.randint(-20, -10)
        #
        # elif -100 <= self.x <= 20:
        #     self.x += np.random.randint(10, 20)
        #
        # else:
        #     self.x += np.random.randint(-15, 15)
        #
        # if 980 <= self.y <= 1100:
        #     self.y += np.random.randint(-20, -10)
        #
        # elif -100 <= self.y <= 20:
        #     self.y += np.random.randint(10, 20)
        #
        # else:
        #     self.y += np.random.randint(-15, 15)

        if 20.01 <= self.x <= 20.055:
            self.x += np.random.uniform(-0.02, -0.01)

        elif 19.792 <= self.x <= 19.842:
            self.x += np.random.uniform(0.01, 0.02)

        else:
            self.x += np.random.uniform(-0.1, 0.1)

        if 50.077 <= self.y <= 50.117:
            self.y += np.random.uniform(-0.02, -0.01)

        elif 49.865 <= self.y <= 49.905:
            self.y += np.random.uniform(0.01, 0.02)

        else:
            self.y += np.random.uniform(-0.1, 0.1)

    def check_infection(self, individuals: List['Individual']) -> None:
        """
        Check if this individual is in infection range, if it is,
        apply some probability (self.infection_probability) to get infection.

        Parameters
        ----------
        individuals: List[Individual], required
            List with all other individuals that are alive. We will be searching for individuals in range and infected.

        """
        # for individual in individuals:
        #     if (individual.infected and abs(individual.x - self.x) <= 10 and abs(individual.y - self.y) <= 10 and
        #             np.random.choice([True, False], p=[self.infection_probability, 1-self.infection_probability])):
        #         self.infected = True
        #         break

        for individual in individuals:
            if (individual.infected and abs(individual.x - self.x) <= 0.05 and abs(individual.y - self.y) <= 0.05 and
                    np.random.choice([True, False], p=[self.infection_probability, 1-self.infection_probability])):
                self.infected = True
                break