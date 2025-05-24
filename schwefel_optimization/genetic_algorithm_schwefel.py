# -*- coding: utf-8 -*-
"""
Implementação do Algoritmo Genético para otimização da função Schwefel.
"""

import numpy as np
import time

# Definição da Função Schwefel
def schwefel_function(x):
    """Calcula o valor da função Schwefel para um vetor x."""
    n = len(x)
    # Verifica se os valores estão dentro do limite [-500, 500]
    if not np.all((x >= -500) & (x <= 500)):
        # Penalidade alta para valores fora do domínio
        return float('inf')
    term1 = 418.9829 * n
    term2 = np.sum(x * np.sin(np.sqrt(np.abs(x))))
    return term1 - term2

# Mínimo global conhecido para n=5
GLOBAL_MINIMUM_VALUE = 0
GLOBAL_MINIMUM_POS = np.array([420.9687] * 5)

class GeneticAlgorithmSchwefel:
    """Classe para o Algoritmo Genético aplicado à função Schwefel."""
    def __init__(self, dimensions=5, population_size=100, generations=200, 
                 mutation_rate=0.1, crossover_rate=0.8, tournament_size=5):
        self.dimensions = dimensions
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.bounds = (-500, 500)
        self.population = None
        self.best_solution = None
        self.best_fitness = float('inf')
        self.convergence_data = [] # Armazena (geração, melhor_fitness)

    def _initialize_population(self):
        """Inicializa a população com valores aleatórios dentro dos limites."""
        self.population = np.random.uniform(self.bounds[0], self.bounds[1], 
                                            (self.population_size, self.dimensions))
        self.best_solution = self.population[0]
        self.best_fitness = schwefel_function(self.best_solution)

    def _evaluate_population(self):
        """Avalia o fitness de cada indivíduo na população."""
        fitness_values = np.array([schwefel_function(ind) for ind in self.population])
        best_gen_idx = np.argmin(fitness_values)
        if fitness_values[best_gen_idx] < self.best_fitness:
            self.best_fitness = fitness_values[best_gen_idx]
            self.best_solution = self.population[best_gen_idx].copy()
        return fitness_values

    def _tournament_selection(self, fitness_values):
        """Seleciona um indivíduo usando seleção por torneio."""
        selected_indices = np.random.choice(self.population_size, self.tournament_size, replace=False)
        tournament_fitness = fitness_values[selected_indices]
        winner_index = selected_indices[np.argmin(tournament_fitness)]
        return self.population[winner_index]

    def _crossover(self, parent1, parent2):
        """Realiza crossover aritmético entre dois pais."""
        if np.random.rand() < self.crossover_rate:
            alpha = np.random.rand()
            child1 = alpha * parent1 + (1 - alpha) * parent2
            child2 = alpha * parent2 + (1 - alpha) * parent1
            # Garante que os filhos estejam dentro dos limites
            child1 = np.clip(child1, self.bounds[0], self.bounds[1])
            child2 = np.clip(child2, self.bounds[0], self.bounds[1])
            return child1, child2
        return parent1.copy(), parent2.copy()

    def _mutate(self, individual):
        """Aplica mutação gaussiana a um indivíduo."""
        for i in range(self.dimensions):
            if np.random.rand() < self.mutation_rate:
                # Adiciona ruído gaussiano, escala pode ser ajustada
                mutation_value = np.random.normal(0, (self.bounds[1] - self.bounds[0]) * 0.1) 
                individual[i] += mutation_value
        # Garante que o indivíduo mutado esteja dentro dos limites
        individual = np.clip(individual, self.bounds[0], self.bounds[1])
        return individual

    def solve(self):
        """Executa o algoritmo genético."""
        self._initialize_population()
        start_time = time.time()

        for generation in range(self.generations):
            fitness_values = self._evaluate_population()
            self.convergence_data.append((generation, self.best_fitness))

            new_population = []
            # Mantém o melhor indivíduo (elitismo)
            best_idx = np.argmin(fitness_values)
            new_population.append(self.population[best_idx].copy())

            while len(new_population) < self.population_size:
                parent1 = self._tournament_selection(fitness_values)
                parent2 = self._tournament_selection(fitness_values)
                
                child1, child2 = self._crossover(parent1, parent2)
                
                mutated_child1 = self._mutate(child1)
                mutated_child2 = self._mutate(child2)
                
                new_population.append(mutated_child1)
                if len(new_population) < self.population_size:
                    new_population.append(mutated_child2)
            
            self.population = np.array(new_population)

            # Log de progresso (opcional)
            # if (generation + 1) % 10 == 0:
            #     print(f"Generation {generation+1}/{self.generations}, Best Fitness: {self.best_fitness:.4f}")

        # Avaliação final para garantir que o best_fitness reflete a população final
        final_fitness = self._evaluate_population()
        self.convergence_data.append((self.generations, self.best_fitness))
        
        exec_time = time.time() - start_time
        
        # Calcula a precisão (distância euclidiana ao mínimo global conhecido)
        precision = np.linalg.norm(self.best_solution - GLOBAL_MINIMUM_POS)

        print(f"GA Final Best Fitness: {self.best_fitness:.4f}")
        print(f"GA Best Solution Found: {self.best_solution}")
        print(f"GA Precision (Distance to Global Minimum): {precision:.4f}")
        print(f"GA Execution Time: {exec_time:.2f}s")

        return {
            'solution': self.best_solution,
            'fitness': self.best_fitness,
            'precision': precision,
            'time': exec_time,
            'convergence': self.convergence_data
        }

# Exemplo de uso (pode ser movido para um script principal depois)
if __name__ == '__main__':
    print("Running Genetic Algorithm for Schwefel Function Optimization...")
    ga_solver = GeneticAlgorithmSchwefel(dimensions=5, population_size=100, generations=500, mutation_rate=0.1, crossover_rate=0.8)
    ga_results = ga_solver.solve()

