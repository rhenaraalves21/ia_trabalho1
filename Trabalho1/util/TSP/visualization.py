import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict
import os
from datetime import datetime


def create_output_dir():
    """Cria diretório de saída se não existir"""
    output_dir = "output_plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def plot_solution(problem, solution: List[str], title: str, save: bool = False):
    """Visualiza a solução com setas direcionais e ordem das cidades"""
    G = nx.DiGraph()  # Grafo direcionado

    # Adiciona nós e arestas do problema
    G.add_nodes_from(problem.cities)
    for city1 in problem.distances:
        for city2 in problem.distances[city1]:
            G.add_edge(city1, city2, weight=problem.distances[city1][city2])

    # Cria sequência da solução
    solution_edges = [(solution[i], solution[i + 1]) for i in range(len(solution) - 1)]
    solution_edges.append((solution[-1], solution[0]))  # Completa o ciclo

    # Layout
    pos = nx.spring_layout(G, seed=42)  # Layout consistente

    plt.figure(figsize=(14, 8))

    # Desenha todas as arestas do problema (cinza claro)
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', alpha=0.3, arrows=True,
                           arrowstyle='->', arrowsize=15)

    # Destaca arestas da solução (vermelho)
    nx.draw_networkx_edges(G, pos, edgelist=solution_edges, edge_color='red',
                           width=2, arrows=True, arrowstyle='->', arrowsize=20)

    # Desenha nós
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

    # Rótulos dos nós
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Rótulos das arestas da solução com distância e ordem
    edge_labels = {}
    for i, (city1, city2) in enumerate(solution_edges):
        distance = problem.get_direct_distance(city1, city2)
        edge_labels[(city1, city2)] = f"{distance:.1f} (#{i + 1})"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_color='red', font_size=9)

    # Legenda
    plt.title(f"{title}\nDistância Total: {problem.path_distance(solution):.2f}", fontsize=14)

    # Ordem das cidades em baixo
    city_order = " → ".join(f"{city}({i + 1})" for i, city in enumerate(solution))
    plt.figtext(0.5, 0.01, f"Ordem: {city_order} → {solution[0]}(1)",
                ha="center", fontsize=10, bbox={"facecolor": "white", "alpha": 0.8, "pad": 5})

    plt.axis('off')

    if save:
        os.makedirs("plots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"plots/{title.replace(' ', '_')}_{timestamp}.png"
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()


def plot_convergence(data, title, save=False):
    plt.figure(figsize=(10, 6))
    for algo, values in data.items():
        plt.plot(values, label=algo)

    plt.title(title)
    plt.xlabel('Iteração')
    plt.ylabel('Distância')
    plt.legend()
    plt.grid(True)

    if save:
        output_dir = create_output_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/convergence_{timestamp}.png"
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()


def plot_comparison(results, save=False):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico de distância
    names = list(results.keys())
    distances = [res['distance'] for res in results.values()]
    ax1.bar(names, distances, color='skyblue')
    ax1.set_title('Comparação de Qualidade da Solução')
    ax1.set_ylabel('Distância Total')

    # Gráfico de tempo
    times = [res['time'] for res in results.values()]
    ax2.bar(names, times, color='lightgreen')
    ax2.set_title('Comparação de Tempo de Execução')
    ax2.set_ylabel('Tempo (segundos)')

    plt.tight_layout()

    if save:
        output_dir = create_output_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/comparison_{timestamp}.png"
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()