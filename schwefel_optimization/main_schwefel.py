# -*- coding: utf-8 -*-
"""
Script principal para executar e comparar os algoritmos de otimização
na função Schwefel.
"""

import numpy as np
import time
import os

# Importa as implementações dos algoritmos
from genetic_algorithm_schwefel import GeneticAlgorithmSchwefel, schwefel_function, GLOBAL_MINIMUM_POS
from ant_colony_schwefel import AntColonySchwefel
from hill_climbing_schwefel import HillClimbingSchwefel

# Cria diretório para gráficos se não existir
output_dir = "schwefel_plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def run_schwefel_optimization():
    """Executa os algoritmos e compara os resultados."""
    dimensions = 5
    bounds = (-500, 500)
    print(f"Otimizando a função Schwefel para {dimensions} dimensões.")
    print(f"Mínimo Global Conhecido em: {GLOBAL_MINIMUM_POS}, Valor: {schwefel_function(GLOBAL_MINIMUM_POS)}")

    # Configurações dos algoritmos (ajustar conforme necessário)
    configs = {
        "Genetic Algorithm": {
            "class": GeneticAlgorithmSchwefel,
            "params": {"dimensions": dimensions, "population_size": 100, "generations": 300, "mutation_rate": 0.1, "crossover_rate": 0.8, "tournament_size": 5}
        },
        "Ant Colony (ACO_R)": {
            "class": AntColonySchwefel,
            "params": {"dimensions": dimensions, "num_ants": 50, "iterations": 200, "archive_size": 20, "q": 0.5, "xi": 0.85}
        },
        "Hill Climbing (Restarts)": {
            "class": HillClimbingSchwefel,
            "params": {"dimensions": dimensions, "max_iterations_per_climb": 150, "num_restarts": 100, "step_size": 5.0}
        }
    }

    results = {}

    # Executa cada algoritmo
    for name, config in configs.items():
        print(f"\n--- Executando {name} ---")
        solver_class = config["class"]
        params = config["params"]
        solver = solver_class(**params)
        
        try:
            result = solver.solve() # solve() já imprime seus resultados individuais
            results[name] = result
        except Exception as e:
            print(f"Erro ao executar {name}: {e}")
            results[name] = None # Marca como falha

    # Compila e imprime a tabela de comparação
    print("\n--- Comparação Final dos Algoritmos (Função Schwefel) ---")
    print("{:<25} {:<20} {:<20} {:<15}".format("Algoritmo", "Melhor Fitness", "Precisão (Dist. Mín)", "Tempo (s)"))
    print("-"*80)
    
    valid_results = {name: res for name, res in results.items() if res is not None}

    # Ordena por melhor fitness (menor é melhor)
    sorted_results = sorted(valid_results.items(), key=lambda item: item[1]["fitness"])

    for name, result in sorted_results:
         print("{:<25} {:<20.4f} {:<20.4f} {:<15.2f}".format(
             name, 
             result["fitness"],
             result["precision"],
             result["time"]
         ))
    
    print("-"*80)
    
    # Retorna os resultados para possível uso posterior (geração de gráficos)
    return results

if __name__ == "__main__":
    all_results = run_schwefel_optimization()
    # Aqui poderíamos salvar os 'all_results' em um arquivo se necessário
    # para o próximo passo (geração de gráficos), mas por enquanto, 
    # a execução sequencial no plano manterá os dados disponíveis implicitamente
    # ou podemos passar 'all_results' para a função de plotagem.

