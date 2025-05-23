import random
from typing import List
from util.TSP.tsp_problem import TSPProblem


class AntColony:
    def __init__(self, problem: TSPProblem, num_ants: int = 10,
                 evaporation_rate: float = 0.5, alpha: float = 1,
                 beta: float = 2, iterations: int = 50):
        self.problem = problem
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations
        self.convergence_data = []

        # Initialize pheromones
        self.pheromones = {}
        for city1 in self.problem.cities:
            self.pheromones[city1] = {}
            for city2 in self.problem.cities:
                if city1 != city2 and self.problem.get_direct_distance(city1, city2) != float('inf'):
                    self.pheromones[city1][city2] = 1.0

    def _construct_solution(self) -> List[str]:
        """Construct solution using pheromone-guided exploration"""
        visited = {self.problem.start_city}
        solution = [self.problem.start_city]

        while len(visited) < len(self.problem.cities):
            current = solution[-1]
            unvisited = set(self.problem.cities) - visited
            reachable = [city for city in unvisited
                         if self.problem.get_direct_distance(current, city) != float('inf')]

            if not reachable:
                # Find closest unvisited city through shortest path
                closest = min(unvisited,
                              key=lambda x: self.problem.get_direct_distance(current, x))
                # Reconstruct path to closest city
                path = self._find_path_between(current, closest)
                solution.extend(path[1:])  # Skip first as it's current
                visited.update(path)
            else:
                # Select next city probabilistically
                next_city = self._select_next_city(current, reachable)
                solution.append(next_city)
                visited.add(next_city)

        return solution

    def _find_path_between(self, start: str, end: str) -> List[str]:
        """Reconstruct path using shortest path matrix"""
        # This is a simplified version - in practice you'd need to store paths
        # For now just return [start, end] as we're using shortest paths
        return [start, end]

    def _select_next_city(self, current: str, candidates: List[str]) -> str:
        """Probabilistic city selection"""
        total = 0.0
        probabilities = []

        for city in candidates:
            tau = self.pheromones[current].get(city, 1e-10) ** self.alpha
            eta = (1.0 / self.problem.get_direct_distance(current, city)) ** self.beta
            probabilities.append((city, tau * eta))
            total += tau * eta

        if total <= 0:
            return random.choice(candidates)

        # Normalize and select
        r = random.uniform(0, total)
        upto = 0.0
        for city, prob in probabilities:
            if upto + prob >= r:
                return city
            upto += prob

        return candidates[-1]

    def _update_pheromones(self, solutions: List[List[str]]):
        """Update pheromone trails"""
        # Evaporation
        for city1 in self.pheromones:
            for city2 in self.pheromones[city1]:
                self.pheromones[city1][city2] *= (1 - self.evaporation_rate)

        # Add new pheromones
        for solution in solutions:
            distance = self.problem.path_distance(solution)
            if distance == float('inf'):
                continue

            pheromone_amount = 1.0 / distance
            for i in range(len(solution)):
                city1 = solution[i]
                city2 = solution[(i + 1) % len(solution)]
                if city2 in self.pheromones[city1]:
                    self.pheromones[city1][city2] += pheromone_amount

    def solve(self) -> List[str]:
        best_solution = None
        best_distance = float('inf')

        for _ in range(self.iterations):
            solutions = []
            for _ in range(self.num_ants):
                solution = self._construct_solution()
                distance = self.problem.path_distance(solution)
                solutions.append(solution)

                if distance < best_distance:
                    best_solution = solution
                    best_distance = distance

            self._update_pheromones(solutions)
            self.convergence_data.append(best_distance)

        return best_solution