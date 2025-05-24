# -*- coding: utf-8 -*-
"""
Script para gerar gráficos de comparação e convergência para os algoritmos
de otimização da função Schwefel.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Importa a função principal que executa os algoritmos e retorna os resultados
from main_schwefel import run_schwefel_optimization

# Diretório para salvar os gráficos
output_dir = "schwefel_plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def plot_schwefel_convergence(results, filename="schwefel_convergence.png"):
    """Plota a convergência do melhor fitness para cada algoritmo."""
    plt.figure(figsize=(12, 7))
    
    for name, result in results.items():
        if result and result.get("convergence"):
            convergence = result["convergence"]
            # Extrai iterações/gerações e fitness
            iterations = [item[0] for item in convergence]
            fitness_values = [item[1] for item in convergence]
            # Garante que os valores de fitness não sejam infinitos para plotagem
            fitness_values = [f if np.isfinite(f) else np.nan for f in fitness_values] 
            plt.plot(iterations, fitness_values, label=name, marker=".", linestyle="-", markersize=4)
            
    plt.title("Convergência dos Algoritmos na Função Schwefel")
    plt.xlabel("Iteração / Geração / Reinício")
    plt.ylabel("Melhor Fitness Encontrado")
    plt.yscale("symlog") # Usar escala logarítmica simétrica pode ajudar com grandes variações
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    print(f"Gráfico de convergência salvo em: {filepath}")
    plt.close()

def plot_schwefel_comparison(results, filename="schwefel_comparison.png"):
    """Plota gráficos de barras comparando fitness, precisão e tempo."""
    valid_results = {name: res for name, res in results.items() if res is not None}
    names = list(valid_results.keys())
    fitness = [valid_results[name]["fitness"] for name in names]
    precision = [valid_results[name]["precision"] for name in names]
    times = [valid_results[name]["time"] for name in names]

    x = np.arange(len(names))  # Posições das labels
    width = 0.25  # Largura das barras

    fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

    # Gráfico de Fitness
    rects1 = axs[0].bar(x, fitness, width, label="Fitness Final") # Corrigido: Parêntese fechado
    axs[0].set_ylabel("Fitness (Menor é Melhor)")
    axs[0].set_title("Comparação de Fitness Final")
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(names, rotation=15, ha="right")
    axs[0].bar_label(rects1, padding=3, fmt="%.2f")
    axs[0].grid(axis="y", linestyle="--", linewidth=0.5) # Corrigido: Aspas

    # Gráfico de Precisão
    rects2 = axs[1].bar(x, precision, width, label="Precisão (Dist. Mín Global)", color="orange")
    axs[1].set_ylabel("Distância Euclidiana (Menor é Melhor)") # Corrigido: Adicionado de volta
    axs[1].set_title("Comparação de Precisão")
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(names, rotation=15, ha="right")
    axs[1].bar_label(rects2, padding=3, fmt="%.2f")
    axs[1].grid(axis="y", linestyle="--", linewidth=0.5) # Corrigido: Aspas

    # Gráfico de Tempo
    rects3 = axs[2].bar(x, times, width, label="Tempo de Execução", color="green") # Corrigido: Aspas
    axs[2].set_ylabel("Tempo (s)")
    axs[2].set_title("Comparação de Tempo de Execução")
    axs[2].set_xticks(x)
    axs[2].set_xticklabels(names, rotation=15, ha="right")
    axs[2].bar_label(rects3, padding=3, fmt="%.2f")
    axs[2].grid(axis="y", linestyle="--", linewidth=0.5) # Corrigido: Aspas

    fig.suptitle("Comparação de Desempenho dos Algoritmos na Função Schwefel", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajusta para o título principal
    
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    print(f"Gráfico de comparação salvo em: {filepath}")
    plt.close()

if __name__ == "__main__":
    print("Executando algoritmos para coletar dados...")
    # Executa a otimização para obter os resultados mais recentes
    results_data = run_schwefel_optimization()
    
    print("\nGerando gráficos...")
    # Gera os gráficos com base nos resultados obtidos
    plot_schwefel_convergence(results_data)
    plot_schwefel_comparison(results_data)
    print("Geração de gráficos concluída.")

