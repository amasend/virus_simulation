from typing import List

import numpy as np

LAT_RANGE = [50.0, 50.1]
LON_RANGE = [19.77, 20.02]


class Individual:
    def __init__(self, start_infection_probability: float = 0.01, infection_probability: float = 0.8) -> None:
        # note: start individual position
        # self.x = np.random.randint(1, 1000)
        # self.y = np.random.randint(1, 1000)

        # 250x100
        self.lat = np.random.uniform(LAT_RANGE[0], LAT_RANGE[1])
        self.lon = np.random.uniform(LON_RANGE[0], LON_RANGE[1])
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

        #################

        if LAT_RANGE[1] <= self.lat <= LAT_RANGE[1] + 0.005:
            self.lat += np.random.uniform(-0.00002, -0.00001)

        elif LAT_RANGE[0] - 0.005 <= self.lat <= LAT_RANGE[0]:
            self.lat += np.random.uniform(0.00001, 0.00002)

        else:
            self.lat += np.random.uniform(-0.00002, 0.00002)

        if LON_RANGE[1] <= self.lon <= LON_RANGE[1] + 0.005:
            self.lon += np.random.uniform(-0.00002, 0.00001)

        elif LON_RANGE[0] - 0.005 <= self.lon <= LON_RANGE[0]:
            self.lon += np.random.uniform(0.00001, 0.00002)

        else:
            self.lon += np.random.uniform(-0.00002, 0.00002)

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
            if (individual.infected and abs(individual.lat - self.lat) <= 0.000018 and abs(
                    individual.lat - self.lat) <= 0.000018 and
                    np.random.choice([True, False], p=[self.infection_probability, 1 - self.infection_probability])):
                self.infected = True
                break

    @staticmethod
    def meter_to_lat(meter: float) -> float:
        return meter * 8.9831117e-06

    @staticmethod
    def meter_to_lon(meter: float, lat: float) -> float:
        return meter / (40075000 * np.cos(lat) / 360)
