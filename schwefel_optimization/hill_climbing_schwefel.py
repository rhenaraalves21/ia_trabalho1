# -*- coding: utf-8 -*-
"""
Implementação do Hill Climbing com Reinício Aleatório para otimização da função Schwefel.
"""

import numpy as np
import time

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

class HillClimbingSchwefel:
    """Classe para Hill Climbing com Reinício Aleatório aplicado à função Schwefel."""
    def __init__(self, dimensions=5, max_iterations_per_climb=100, 
                 num_restarts=50, step_size=1.0):
        self.dimensions = dimensions
        self.max_iterations_per_climb = max_iterations_per_climb
        self.num_restarts = num_restarts
        self.step_size = step_size # Tamanho do passo para gerar vizinhos
        self.bounds = (-500, 500)
        
        self.overall_best_solution = None
        self.overall_best_fitness = float("inf")
        self.convergence_data = [] # Armazena (restart #, melhor_fitness_restart)

    def _generate_neighbor(self, current_solution):
        """Gera um vizinho adicionando um pequeno ruído gaussiano."""
        neighbor = current_solution + np.random.normal(0, self.step_size, self.dimensions)
        # Garante que o vizinho esteja dentro dos limites
        neighbor = np.clip(neighbor, self.bounds[0], self.bounds[1])
        return neighbor

    def _climb(self, start_solution):
        """Executa uma única subida de encosta a partir de uma solução inicial."""
        current_solution = start_solution
        current_fitness = schwefel_function(current_solution)
        
        for _ in range(self.max_iterations_per_climb):
            neighbor = self._generate_neighbor(current_solution)
            neighbor_fitness = schwefel_function(neighbor)
            
            # Move para o vizinho se for melhor
            if neighbor_fitness < current_fitness:
                current_solution = neighbor
                current_fitness = neighbor_fitness
            # Poderia adicionar uma condição de parada se não houver melhora por X iterações
            
        return current_solution, current_fitness

    def solve(self):
        """Executa o Hill Climbing com múltiplos reinícios aleatórios."""
        start_time = time.time()

        for restart in range(self.num_restarts):
            # Gera uma solução inicial aleatória para este reinício
            initial_solution = np.random.uniform(self.bounds[0], self.bounds[1], self.dimensions)
            
            # Executa a subida de encosta
            best_solution_restart, best_fitness_restart = self._climb(initial_solution)
            
            # Atualiza a melhor solução geral encontrada
            if best_fitness_restart < self.overall_best_fitness:
                self.overall_best_fitness = best_fitness_restart
                self.overall_best_solution = best_solution_restart.copy()
            
            self.convergence_data.append((restart, self.overall_best_fitness))

            # Log de progresso (opcional)
            # if (restart + 1) % 5 == 0:
            #     print(f"Restart {restart+1}/{self.num_restarts}, Current Best Fitness: {self.overall_best_fitness:.4f}")

        exec_time = time.time() - start_time
        self.convergence_data.append((self.num_restarts, self.overall_best_fitness))

        # Calcula a precisão
        if self.overall_best_solution is None:
             # Caso nenhum reinício produza uma solução válida (muito improvável)
             self.overall_best_solution = np.random.uniform(self.bounds[0], self.bounds[1], self.dimensions)
             self.overall_best_fitness = schwefel_function(self.overall_best_solution)
             precision = float('inf') # Ou recalcular
        else:
            precision = np.linalg.norm(self.overall_best_solution - GLOBAL_MINIMUM_POS)

        print(f"HC Final Best Fitness: {self.overall_best_fitness:.4f}")
        print(f"HC Best Solution Found: {self.overall_best_solution}")
        print(f"HC Precision (Distance to Global Minimum): {precision:.4f}")
        print(f"HC Execution Time: {exec_time:.2f}s")

        return {
            'solution': self.overall_best_solution,
            'fitness': self.overall_best_fitness,
            'precision': precision,
            'time': exec_time,
            'convergence': self.convergence_data
        }

# Exemplo de uso
if __name__ == '__main__':
    print("Running Hill Climbing with Random Restarts for Schwefel Function...")
    hc_solver = HillClimbingSchwefel(dimensions=5, max_iterations_per_climb=200, num_restarts=100, step_size=5.0)
    hc_results = hc_solver.solve()

