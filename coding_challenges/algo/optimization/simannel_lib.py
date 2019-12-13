import numpy as np
from simanneal import Annealer


class TravellingSalesmanProblem(Annealer):
    """Test annealer with a travelling salesman problem."""

    def __init__(self, state: np.ndarray, coords: np.ndarray) -> None:
        self.coords = coords
        super().__init__(state)

    def dist(self, i, j):
        a, b = self.state[i], self.state[j]
        return np.linalg.norm(a - b)

    def move(self):
        """Swaps two cities in the route."""
        a, b = np.random.randint(len(self.state), size=2)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self):
        """Calculates the length of the route."""
        l = len(self.state)
        return sum(
            self.dist(i, i + 1)
            for i in range(-1, l - 1))


if __name__ == '__main__':
    size = 10
    coords = np.random.rand(size, 2)
    init_state = np.arange(size)
    np.random.shuffle(init_state)

    tsp = TravellingSalesmanProblem(init_state, coords)
    tsp.set_schedule(tsp.auto(minutes=0.2))
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()



    print(state, e)
