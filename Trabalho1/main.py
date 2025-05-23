import argparse
from util import TSPProblem
from util.TSP.visualization import plot_solution, plot_convergence, plot_comparison
from algoritimos import GeneticAlgorithm, AntColony, HillClimbing
import time
import os


def run_algorithm(problem, algorithm_class, **kwargs):
    start_time = time.time()
    solver = algorithm_class(problem, **kwargs)
    solution = solver.solve()
    exec_time = time.time() - start_time
    distance = problem.path_distance(solution)

    return {
        'solution': solution,
        'distance': distance,
        'time': exec_time,
        'convergence': getattr(solver, 'convergence_data', None)
    }


def main():
    parser = argparse.ArgumentParser(description="TSP Solver for Non-Complete Graphs")
    args = parser.parse_args()

    # Load problem
    try:
        problem = TSPProblem('distancias.txt')
    except Exception as e:
        print(f"Error loading problem: {str(e)}")
        return

    print(f"\nSolving TSP with {len(problem.cities)} cities starting at {problem.start_city}")
    print(f"Cities: {', '.join(problem.cities)}")

    # Algorithm configurations
    algorithms = {
        'Hill Climbing': (HillClimbing, {'max_iterations': 1000}),
        'Genetic Algorithm': (GeneticAlgorithm, {'population_size': 50, 'generations': 100}),
        'Ant Colony': (AntColony, {'num_ants': 10, 'iterations': 50})
    }

    results = {}
    convergence_data = {}

    # Run all algorithms
    for name, (algo_class, params) in algorithms.items():
        print(f"\nRunning {name}...")
        try:
            result = run_algorithm(problem, algo_class, **params)
            results[name] = result

            if result['convergence']:
                convergence_data[name] = result['convergence']

            print(f"Solution: {' -> '.join(result['solution'])} -> {result['solution'][0]}")
            print(f"Distance: {result['distance']:.2f}")
            print(f"Time: {result['time']:.2f}s")

            plot_solution(problem, result['solution'], f"{name} Solution", True)
        except Exception as e:
            print(f"Error running {name}: {str(e)}")
            continue

    # Show comparisons

    if convergence_data:
        plot_convergence(convergence_data, "Algorithm Convergence", save=True)
    plot_comparison(results, save=True)

    # Print summary
    print("\nAlgorithm Comparison:")
    print("{:<20} {:<15} {:<15}".format("Algorithm", "Distance", "Time (s)"))
    for name, result in results.items():
        print("{:<20} {:<15.2f} {:<15.2f}".format(name, result['distance'], result['time']))


if __name__ == "__main__":
    main()