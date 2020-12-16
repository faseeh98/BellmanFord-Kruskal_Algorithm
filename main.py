# INFR2820 Final Project - Winter 2020

# By: Faseeh Ahmed(100730111) & Neroshan Manoharan(100581847)
# April 9th, 2020

from collections import defaultdict


class Graph:
    def __init__(self, fname):
        self.vertices, self.graph = self.create_graph(fname)

    def update_weight(self, src, dest, value):  # Function to update weight on a edge
        self.graph[src][dest] = value

    def remove_edge(self, src, dest):           # Function to remove one edge from the graph
        del self.graph[src][dest]

    def remove_node(self, node):                # Function to remove one node from the graph
        del self.graph[node]

        for src in self.graph:
            for dest in self.graph[src]:
                if dest == node:
                    del self.graph[src][dest]
                    break

    def create_graph(self, fname):               # fName: Name of the file containing the graph data; Returns a set of vertices and the adjacency list for the graph

        vertices = set()
        # Dictionary of dictionaries in order to do 2D mapping to represent the edges in the graph.
        graph = defaultdict(dict)

        with open(fname) as f:
            lines = f.readlines()
            for line in lines:
                src, dest, edge = line.split(' ')
                # Since it's a directed graph, only 1 direction is considered
                graph[src][dest] = int(edge)
                # Add the vertex to thee set of vertices
                vertices.add(dest)

        # Add all the sources to set of vertices
        for src in graph.keys():
            vertices.add(src)

        # set of vertices, and the adjacency list for the graph
        return vertices, graph

    def bellman_ford(self, src):
        # Distance vector from the source vertex
        # Initialized to infinity to begin with
        distance = {node: float("inf") for node in self.vertices}
        # Distance of source to itself
        distance[src] = 0

        # Bellman ford involves V - 1 iterations.
        for i in range(len(self.vertices) - 1):
            # Iterating over all the u, v edges and relaxing them
            for u in self.graph:
                for v, w in self.graph[u].items():
                    # Relax if a shorter distance to v is found
                    if distance[u] != float("inf") and distance[u] + w < distance[v]:
                        distance[v] = distance[u] + w

        # Optionally, check for negative cycle
        for u in self.graph:
            for v, w in self.graph[u].items():
                # If after V-1 iteration, relaxation is still possible, -ve cycle is present!
                if distance[u] != float("inf") and distance[u] + w < distance[v]:
                    print("Negative cycle detected!")
                    return

        # Print out the shortest distances to all the nodes from source node
        print("Shortest distance value from {}".format(src))
        print(distance)
        return distance

    # Typical find union
    def find(self, parent, i):                      ##Parent: Map of parent nodes for all the nodes; i: Node for which you've to find the parent; Returns the parent vertex of node i
        # Base case, a node which is it's own parent
        if parent[i] == i:
            return i
        # Recursively
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        # Find the parents of both the nodes.
        root_x = self.find(parent, x)
        root_y = self.find(parent, y)

        # The idea of weighted find union is to add the parent
        # such that the height is lowest. Rank keeps track of the height from leaves to root of the parent chain.
        if rank[root_x] < rank[root_y]:
            # Rank of x is less than y, so make y the parent of y (so that the height/rank of the tree doesn't grow)
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            # Rank if equal, pick any node as parent, rank / height gets increased by 1
            parent[root_y] = root_x
            rank[root_x] += 1

    def mst_kruskal(self):
        # Stores the MST edges found so far
        mst = []
        # Flatten the graph to a list
        all_edges = [(u, v, w) for u in self.graph for v, w in self.graph[u].items()]
        # Sort all edges by edge weight, ascending order
        all_edges.sort(key=lambda x: x[2])

        # Parent and rank, maintained for weighted find-union
        parent = {v: v for v in self.vertices}
        rank = {p: 0 for p in parent}

        for u, v, w in all_edges:
            parent_u = self.find(parent, u)
            parent_v = self.find(parent, v)

            # Disjoint edge, combine
            if parent_u != parent_v:
                mst.append((u, v, w))
                self.union(parent, rank, parent_u, parent_v)

            # Since it's a MST, it can only contain V - 1 edges
            if len(mst) == len(self.vertices) - 1:
                break

        print()
        print("Edges in the minimum spanning tree are")
        print(mst)
        return mst


g = Graph('network.txt')
g.bellman_ford('Vancouver')
g.mst_kruskal()
