from .individual import Individual, np


class Student(Individual):
    def __init__(self, start_infection_probability: float = 0.01, infection_probability: float = 0.8):
        super().__init__(start_infection_probability=start_infection_probability,
                         infection_probability=infection_probability)
        self.LAT_RANGE = [50.0621, 50.0675]
        self.LON_RANGE = [19.905, 19.9226]
        self.INFECTION_RADIUS = 0.0004

        self.lat = np.random.uniform(self.LAT_RANGE[0], self.LAT_RANGE[1])
        self.lon = np.random.uniform(self.LON_RANGE[0], self.LON_RANGE[1])
