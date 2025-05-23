import random
from typing import List, Dict, Tuple
from util.TSP.tsp_problem import TSPProblem


class GeneticAlgorithm:
    def __init__(self, problem: TSPProblem, population_size: int = 50,
                 mutation_rate: float = 0.01, generations: int = 100):
        self.problem = problem
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.convergence_data = []

    def _initialize_population(self) -> List[List[str]]:
        """Gera população inicial usando DFS aleatório para garantir rotas válidas"""
        population = []
        for _ in range(self.population_size):
            route = self._generate_valid_route()
            population.append(route)
        return population

    def _generate_valid_route(self) -> List[str]:
        """Gera uma rota válida usando DFS com conexões diretas"""

        def dfs(current: str, path: List[str], visited: set) -> List[str]:
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

        # Tenta no máximo 10 vezes
        for _ in range(10):
            route = dfs(self.problem.start_city, [self.problem.start_city], {self.problem.start_city})
            if route is not None:
                return route
        raise ValueError("Não foi possível gerar rota válida")

    def _fitness(self, individual: List[str]) -> float:
        """Função de fitness baseada na distância inversa"""
        distance = self.problem.path_distance(individual)
        return 1.0 / (distance + 1e-10)  # Evita divisão por zero

    def _select_parents(self, population: List[List[str]],
                        fitnesses: List[float]) -> Tuple[List[str], List[str]]:
        """Seleção por torneio com tamanho 3"""
        tournament_size = 3
        parent1 = max(random.sample(population, tournament_size),
                      key=lambda x: self._fitness(x))
        parent2 = max(random.sample(population, tournament_size),
                      key=lambda x: self._fitness(x))
        return parent1, parent2

    def _crossover(self, parent1: List[str], parent2: List[str]) -> List[str]:
        """Edge Recombination Crossover (ERX) adaptado para conexões diretas"""
        # Cria mapa de adjacências combinando ambos os pais
        adjacency: Dict[str, List[str]] = {city: [] for city in self.problem.cities}

        for i in range(len(parent1)):
            city = parent1[i]
            left = parent1[i - 1] if i > 0 else parent1[-1]
            right = parent1[i + 1] if i < len(parent1) - 1 else parent1[0]
            adjacency[city].extend([left, right])

        for i in range(len(parent2)):
            city = parent2[i]
            left = parent2[i - 1] if i > 0 else parent2[-1]
            right = parent2[i + 1] if i < len(parent2) - 1 else parent2[0]
            adjacency[city].extend([left, right])

        # Remove duplicatas e conexões inexistentes
        for city in adjacency:
            adjacency[city] = [c for c in set(adjacency[city])
                               if c in self.problem.get_neighbors(city)]
            random.shuffle(adjacency[city])  # Para variedade

        # Constrói o filho
        child = [self.problem.start_city]
        current = self.problem.start_city
        available = set(self.problem.cities) - {current}

        while available:
            # Pega vizinhos disponíveis
            neighbors = [city for city in adjacency[current] if city in available]

            if not neighbors:
                # Fallback: cidade mais próxima disponível
                next_city = min(available,
                                key=lambda x: self.problem.get_direct_distance(current, x))
            else:
                # Escolhe o vizinho com menos conexões disponíveis (heurística)
                next_city = min(neighbors, key=lambda x: len(adjacency[x]))

            child.append(next_city)
            available.remove(next_city)
            current = next_city

        return child

    def _mutate(self, individual: List[str]) -> List[str]:
        """Mutação por inversão de segmento com conexões válidas"""
        if random.random() < self.mutation_rate and len(individual) > 3:
            size = len(individual)
            for _ in range(100):  # Tenta no máximo 100 inversões
                i, j = sorted(random.sample(range(1, size - 1), 2))

                # Verifica conexões antes/depois da inversão
                valid_inversion = (
                        self.problem.get_direct_distance(individual[i - 1], individual[j]) != float('inf') and
                        self.problem.get_direct_distance(individual[i], individual[(j + 1) % size]) != float('inf')
                )

                if valid_inversion:
                    individual[i:j + 1] = individual[i:j + 1][::-1]
                    break

        return individual

    def solve(self) -> List[str]:
        population = self._initialize_population()
        best_individual = min(population, key=lambda x: self.problem.path_distance(x))
        best_distance = self.problem.path_distance(best_individual)
        self.convergence_data.append(best_distance)

        for _ in range(self.generations):
            fitnesses = [self._fitness(ind) for ind in population]
            new_population = []

            for _ in range(self.population_size // 2):
                parent1, parent2 = self._select_parents(population, fitnesses)
                child1 = self._crossover(parent1, parent2)
                child2 = self._crossover(parent2, parent1)
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)

                # Garante que os filhos são válidos
                if self.problem.is_valid_route(child1):
                    new_population.append(child1)
                if self.problem.is_valid_route(child2):
                    new_population.append(child2)

            # Elitismo: mantém a melhor solução
            population = sorted(
                new_population + [best_individual],
                key=lambda x: self.problem.path_distance(x)
            )[:self.population_size]

            # Atualiza melhor solução
            current_best = population[0]
            current_dist = self.problem.path_distance(current_best)
            if current_dist < best_distance:
                best_individual = current_best
                best_distance = current_dist

            self.convergence_data.append(best_distance)

        return best_individual