import random
from typing import List, Optional, Tuple
from util.TSP.tsp_problem import TSPProblem


class HillClimbing:
    def __init__(self, problem: TSPProblem, max_iterations: int = 1000):
        self.problem = problem
        self.max_iterations = max_iterations
        self.convergence_data = []

    def _generate_valid_route(self) -> List[str]:
        """Gera uma rota válida usando Depth-First Search (DFS)"""

        def dfs(current: str, path: List[str], visited: set) -> Optional[List[str]]:
            if len(visited) == len(self.problem.cities):
                if self.problem.get_direct_distance(path[-1], path[0]) != float('inf'):
                    return path
                return None

            neighbors = [city for city in self.problem.get_neighbors(current)
                         if city not in visited]
            random.shuffle(neighbors)

            for neighbor in neighbors:
                result = dfs(neighbor, path + [neighbor], visited | {neighbor})
                if result is not None:
                    return result
            return None

        # Tenta no máximo 10 vezes gerar uma rota válida
        for _ in range(10):
            route = dfs(self.problem.start_city, [self.problem.start_city], {self.problem.start_city})
            if route is not None:
                return route
        raise ValueError("Não foi possível gerar rota inicial válida")

    def _get_valid_neighbor(self, current: List[str]) -> Optional[List[str]]:
        """Gera um vizinho válido através de inversões de segmentos conectados"""
        size = len(current)

        for _ in range(100):  # Tenta no máximo 100 inversões diferentes
            i, j = sorted(random.sample(range(1, size - 1), 2))

            # Verifica se a inversão mantém as conexões
            valid_inversion = (
                # Conexão antes do segmento
                    self.problem.get_direct_distance(current[i - 1], current[j]) != float('inf') and
                    # Conexão depois do segmento
                    self.problem.get_direct_distance(current[i], current[(j + 1) % size]) != float('inf')
            )

            if valid_inversion:
                neighbor = current.copy()
                neighbor[i:j + 1] = neighbor[i:j + 1][::-1]  # Inverte o segmento
                return neighbor

        return None  # Não encontrou vizinho válido

    def solve(self) -> List[str]:
        current_solution = self._generate_valid_route()
        current_distance = self.problem.path_distance(current_solution)
        self.convergence_data.append(current_distance)

        for _ in range(self.max_iterations):
            neighbor = self._get_valid_neighbor(current_solution)

            if neighbor is None:
                continue  # Não encontrou vizinhos válidos

            neighbor_distance = self.problem.path_distance(neighbor)

            if neighbor_distance < current_distance:
                current_solution = neighbor
                current_distance = neighbor_distance
                self.convergence_data.append(current_distance)

        return current_solution