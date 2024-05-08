"""
Task 1.4: (25%) cheapest train tickets

The requirements of the task are as follows:
1. Import the csv file.
2. Input two station names for departure and destination.
3. Return the cheapest cost of the two stations and all the station names on
the route.

"""

import os
import csv
import typing
import time


def get_graph(file_name) -> typing.List[typing.List]:
    """
    Return a graph, G, of source S, target and weights.
    """

    graph = {}
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)

        # Read the file and convert the columns into
        # dictionary of s, t and cost (weight).
        # according to the algorithm.
        for row in csv_reader:
            source, target, weight = row
            weight = int(weight)
            if source not in graph:
                graph[source] = {}
            if target not in graph:
                graph[target] = {}
            graph[source][target] = weight
            graph[target][source] = weight
    return graph


class CheapestTrainTickets:
    """
    In a train ticket search system, users require the
    cheapest train tickets between their departure and destination.

    This object contains functions and attributes about their journey,
    price, start or end points, and more.
    """

    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__name__))
        self.current_directory = current_directory + "\\"
        self.task_directory = self.current_directory + "\\tasks\\Task 1_4\\"

    def __str__(self):
        s = input("Enter your Departure Location: ")
        t = input("Enter your Destination Location: ")
        route, start_time, end_time = self.get_route(s, t)
        cheapest_route = "The cheapest cost to the destination is: "

        updated_routes = {}
        s_idx = list(route.keys()).index(s)
        for i, (k, v) in enumerate(route.items()):
            if i >= s_idx:
                updated_routes[k] = v

        idx = 0
        print("\nIndex | Station | Cost")
        for k, v in updated_routes.items():
            print(idx, k, v)
            idx += 1

        return "%s\nTook %s seconds." % (
            cheapest_route,
            end_time - start_time
        )

    def get_shortest_distance(self, s: str):
        """
        Pass in source (starting node) to return the shortest
        distances on the network.
        """

        g = get_graph(
            self.task_directory +
            "task1_4_railway_network.csv"
        )

        distances = {node: float('inf') for node in g}
        distances[s] = 0
        visited = set()

        while len(visited) < len(g):

            min_distance = float('inf')
            min_node = None

            for node in g:
                if node not in visited and distances[node] < min_distance:
                    min_distance = distances[node]
                    min_node = node

            if min_node is None:
                break

            visited.add(min_node)

            # For all unvisited neighbour nodes
            for next_node, weight in g[min_node].items():
                distance = distances[min_node] + weight

                if distance < distances[next_node]:
                    distances[next_node] = distance

        return distances

    def get_route(self, s, t):
        """
        Input two station names for departure and destination
        to return all stations for that particular route,
        if available.
        """

        dist = {}
        start_time = time.time()
        shortest_dist = self.get_shortest_distance(s)
        end_time = time.time()
        for next_node in shortest_dist:
            dist[next_node] = shortest_dist[next_node]
            if isinstance(shortest_dist[next_node], float):
                break

            if next_node == t:
                break

        return dist, start_time, end_time


if __name__ == '__main__':
    ctt = CheapestTrainTickets()
    print(ctt)
