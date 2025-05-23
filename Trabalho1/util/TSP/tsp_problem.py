from typing import List, Dict, Set


class TSPProblem:
    def __init__(self, filename: str):
        self.cities: List[str] = []
        self.distances: Dict[str, Dict[str, float]] = {}
        self.start_city: str = None
        self.city_index: Dict[str, int] = {}
        self.adjacency_list: Dict[str, Set[str]] = {}  # Lista de adjacência para conexões diretas

        self._load_from_file(filename)
        self._build_adjacency_list()
        self._validate_graph()

    def _load_from_file(self, filename: str):
        """Carrega o grafo a partir do arquivo"""
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]

            # Processa primeira linha (cidades)
            first_line = lines[0].split()
            self.cities = list(dict.fromkeys(first_line))  # Remove duplicatas
            self.start_city = first_line[-1]

            # Processa arestas
            for line in lines[1:]:
                parts = line.split()
                if len(parts) != 3:
                    continue  # Ignora linhas mal formatadas

                city1, dist_str, city2 = parts
                try:
                    distance = float(dist_str)
                except ValueError:
                    continue  # Ignora linhas com distância inválida

                # Adiciona conexão direta (ida e volta)
                self._add_connection(city1, city2, distance)
                self._add_connection(city2, city1, distance)

    def _add_connection(self, city1: str, city2: str, distance: float):
        """Adiciona uma conexão direta ao grafo"""
        if city1 not in self.distances:
            self.distances[city1] = {}
        self.distances[city1][city2] = distance

    def _build_adjacency_list(self):
        """Constrói lista de adjacência para conexões diretas"""
        self.adjacency_list = {city: set() for city in self.cities}
        for city1 in self.distances:
            for city2 in self.distances[city1]:
                self.adjacency_list[city1].add(city2)

    def _validate_graph(self):
        """Valida se o grafo está adequado para TSP"""
        if not self.cities:
            raise ValueError("Nenhuma cidade definida")

        if self.start_city not in self.cities:
            raise ValueError(f"Cidade inicial {self.start_city} não encontrada na lista de cidades")

        # Verifica se todas as cidades têm pelo menos uma conexão
        for city in self.cities:
            if not self.adjacency_list.get(city):
                raise ValueError(f"Cidade {city} não tem conexões de saída")

    def get_neighbors(self, city: str) -> List[str]:
        """Retorna lista de cidades diretamente conectadas"""
        return list(self.distances.get(city, {}).keys())

    def get_direct_distance(self, city1: str, city2: str) -> float:
        """Retorna distância direta ou infinito se não conectar"""
        return self.distances.get(city1, {}).get(city2, float('inf'))

    def is_valid_route(self, route: List[str]) -> bool:
        """Verifica se uma rota é válida"""
        return (
                len(route) == len(self.cities) and
                set(route) == set(self.cities) and
                route[0] == route[-1] == self.start_city and
                all(self.are_connected(route[i], route[i + 1])
                    for i in range(len(route) - 1)) and
                self.are_connected(route[-1], route[0])
        )

    def are_connected(self, city1: str, city2: str) -> bool:
        """Verifica conexão direta entre cidades"""
        return city2 in self.distances.get(city1, {})

    def path_distance(self, path: List[str]) -> float:
        """
        Calcula a distância total de um caminho, considerando APENAS conexões diretas.
        Retorna infinito se o caminho contiver conexões inválidas.
        """
        total = 0.0
        n = len(path)

        for i in range(n):
            current = path[i]
            next_city = path[(i + 1) % n]  # Conecta o último ao primeiro

            dist = self.get_direct_distance(current, next_city)
            if dist == float('inf'):
                return float('inf')  # Rota inválida
            total += dist

        return total

    def is_valid_route(self, route: List[str]) -> bool:
        """Verifica se uma rota é válida (visita todas as cidades sem conexões inválidas)"""
        return (len(route) == len(self.cities) and
                set(route) == set(self.cities) and
                route[0] == self.start_city and
                self.path_distance(route) != float('inf'))

    def get_neighbors(self, city: str) -> Set[str]:
        """Retorna todas as cidades diretamente conectadas à cidade especificada"""
        return self.adjacency_list.get(city, set())

    def visualize_graph(self):
        """Método auxiliar para visualizar o grafo (útil para depuração)"""
        print("\nGrafo de Conexões Diretas:")
        for city in sorted(self.cities):
            connections = sorted(self.adjacency_list[city])
            print(f"{city}: {', '.join(connections) or 'Nenhuma'}")

        print("\nMatriz de Distâncias Diretas:")
        cities_sorted = sorted(self.cities)
        print("     " + " ".join(f"{c:>5}" for c in cities_sorted))
        for city1 in cities_sorted:
            row = [f"{self.get_direct_distance(city1, city2):5.1f}"
                   if city2 in self.adjacency_list[city1] else "   - "
                   for city2 in cities_sorted]
            print(f"{city1:5} " + " ".join(row))