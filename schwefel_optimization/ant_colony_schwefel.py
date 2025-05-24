# -*- coding: utf-8 -*-
"""
Implementação da Otimização por Colônia de Formigas (ACO_R) para otimização da função Schwefel.
Adaptado para domínios contínuos.
"""

import numpy as np
import time
from scipy.stats import norm

# Definição da Função Schwefel (reutilizada)
def schwefel_function(x):
    """Calcula o valor da função Schwefel para um vetor x."""
    n = len(x)
    if not np.all((x >= -500) & (x <= 500)):
        return float("inf")
    term1 = 418.9829 * n
    term2 = np.sum(x * np.sin(np.sqrt(np.abs(x))))
    return term1 - term2

# Mínimo global conhecido para n=5
GLOBAL_MINIMUM_VALUE = 0
GLOBAL_MINIMUM_POS = np.array([420.9687] * 5)

class AntColonySchwefel:
    """Classe para ACO_R aplicado à função Schwefel."""
    def __init__(self, dimensions=5, num_ants=50, iterations=100, 
                 archive_size=10, q=0.1, xi=0.85):
        self.dimensions = dimensions
        self.num_ants = num_ants
        self.iterations = iterations
        self.archive_size = archive_size # Tamanho do arquivo de soluções (k)
        self.q = q # Parâmetro de exploração vs explotação (similar a q0 em ACS)
        self.xi = xi # Velocidade de convergência (influencia a std dev)
        self.bounds = (-500, 500)
        
        self.solution_archive = [] # Lista de tuplas (fitness, solution)
        self.best_solution = None
        self.best_fitness = float("inf")
        self.convergence_data = [] # Armazena (iteração, melhor_fitness)

    def _initialize_archive(self):
        """Inicializa o arquivo de soluções com formigas aleatórias."""
        initial_solutions = np.random.uniform(self.bounds[0], self.bounds[1],
                                              (self.num_ants, self.dimensions))
        for sol in initial_solutions:
            fitness = schwefel_function(sol)
            self.solution_archive.append((fitness, sol))
        
        # Ordena o arquivo pela qualidade (menor fitness é melhor)
        self.solution_archive.sort(key=lambda x: x[0])
        # Mantém apenas os k melhores
        self.solution_archive = self.solution_archive[:self.archive_size]
        
        if self.solution_archive:
            self.best_fitness, self.best_solution = self.solution_archive[0]
        else:
             # Caso inicialização não gere soluções válidas (raro)
             self.best_solution = np.random.uniform(self.bounds[0], self.bounds[1], self.dimensions)
             self.best_fitness = schwefel_function(self.best_solution)


    def _calculate_weights(self):
        """Calcula os pesos para cada solução no arquivo (baseado no rank)."""
        weights = np.zeros(len(self.solution_archive))
        rank_inv_sum = sum(1.0 / (i + 1) for i in range(len(self.solution_archive)))
        for i in range(len(self.solution_archive)):
            weights[i] = (1.0 / (self.q * self.archive_size * np.sqrt(2 * np.pi))) * \
                         np.exp(- (i**2) / (2 * (self.q**2) * (self.archive_size**2))) / rank_inv_sum
        # Normaliza os pesos para somarem 1
        return weights / np.sum(weights)

    def _sample_solution(self, weights):
        """Gera uma nova solução amostrando do arquivo com base nos pesos."""
        # Seleciona uma solução do arquivo com base nos pesos
        selected_idx = np.random.choice(len(self.solution_archive), p=weights)
        selected_solution = self.solution_archive[selected_idx][1]
        
        # Calcula o desvio padrão para cada dimensão baseado na média das distâncias
        std_devs = np.zeros(self.dimensions)
        for dim in range(self.dimensions):
            avg_dist = sum(abs(selected_solution[dim] - sol[1][dim]) for sol in self.solution_archive)
            std_devs[dim] = self.xi * avg_dist / (len(self.solution_archive) -1 + 1e-9) # Evita divisão por zero

        # Gera a nova solução amostrando de uma gaussiana para cada dimensão
        new_solution = np.zeros(self.dimensions)
        for dim in range(self.dimensions):
            new_solution[dim] = np.random.normal(loc=selected_solution[dim], scale=std_devs[dim])
            
        # Garante que a nova solução esteja dentro dos limites
        new_solution = np.clip(new_solution, self.bounds[0], self.bounds[1])
        return new_solution

    def solve(self):
        """Executa o algoritmo ACO_R."""
        self._initialize_archive()
        start_time = time.time()

        for iteration in range(self.iterations):
            weights = self._calculate_weights()
            new_solutions = []
            
            # Gera novas soluções (posições das formigas)
            for _ in range(self.num_ants):
                ant_solution = self._sample_solution(weights)
                ant_fitness = schwefel_function(ant_solution)
                new_solutions.append((ant_fitness, ant_solution))
            
            # Adiciona as novas soluções ao arquivo
            self.solution_archive.extend(new_solutions)
            
            # Ordena e mantém o tamanho do arquivo
            self.solution_archive.sort(key=lambda x: x[0])
            self.solution_archive = self.solution_archive[:self.archive_size]
            
            # Atualiza a melhor solução encontrada
            current_best_fitness, current_best_solution = self.solution_archive[0]
            if current_best_fitness < self.best_fitness:
                self.best_fitness = current_best_fitness
                self.best_solution = current_best_solution.copy()
                
            self.convergence_data.append((iteration, self.best_fitness))

            # Log de progresso (opcional)
            # if (iteration + 1) % 10 == 0:
            #     print(f"Iteration {iteration+1}/{self.iterations}, Best Fitness: {self.best_fitness:.4f}")

        exec_time = time.time() - start_time
        self.convergence_data.append((self.iterations, self.best_fitness))

        # Calcula a precisão
        precision = np.linalg.norm(self.best_solution - GLOBAL_MINIMUM_POS)

        print(f"ACO Final Best Fitness: {self.best_fitness:.4f}")
        print(f"ACO Best Solution Found: {self.best_solution}")
        print(f"ACO Precision (Distance to Global Minimum): {precision:.4f}")
        print(f"ACO Execution Time: {exec_time:.2f}s")

        return {
            'solution': self.best_solution,
            'fitness': self.best_fitness,
            'precision': precision,
            'time': exec_time,
            'convergence': self.convergence_data
        }

# Exemplo de uso
if __name__ == '__main__':
    print("Running Ant Colony Optimization (ACO_R) for Schwefel Function...")
    aco_solver = AntColonySchwefel(dimensions=5, num_ants=50, iterations=200, archive_size=20, q=0.5, xi=0.85)
    aco_results = aco_solver.solve()

