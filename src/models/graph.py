import numpy as np

from typing import List

class Node():
    '''
    Class represents single graph node.
    '''

    def __init__(self, 
                 coordinates: np.ndarray, 
                 idx: int,
                 label: float = 0) -> None:
        '''
        Parameters:
        coordinates - x and y coordinates of a point
        idx - index of the node in the list of nodes in graph
        label - label assigned to the node (by default 0)
        '''
        self.idx = idx
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.label = label
        self.edges: List[Edge] = []

    def compute_distance(self, node) -> float:
        '''
        Method computes distance between two points.

        Parameters:
        node - node of a point with which the distance is to be computed

        Return: euclidean distance between two points
        '''
        return np.linalg.norm([self.x, self.y], [node.x, node.y])
    
    def get_weights_of_edges(self) -> List[float]:
        '''
        Method returns a list of weights of all edges that go from the given node.

        Returns: list of edges' weights
        '''
        return [edge.weight for edge in self.edges]

class Edge():
    '''
    Class describing edge in the graph.
    '''

    def __init__(self, src: Node, dst: Node, weight: float) -> None:
        '''
        Parameters:
        src - source node
        dst - destination done
        weight - weight of the edge
        '''
        self.src = src
        self.dst = dst
        self.weight = weight

class Graph():
    '''
    Class representing graph used in Hungarian algorithm.
    '''

    def __init__(self, 
                 n: int, 
                 k: int, 
                 wells: List[np.ndarray], 
                 houses: List[np.ndarray],
                 empty_edges: bool = False) -> None:
        '''
        Parameters:
        n - number of wells
        k - number of houses per well
        wells - list of coordinates of wells
        houses - list of coordinates of houses
        empty_edges - flag indicating if the graph should be initialized without edges
        '''
        self.n = n
        self.k = k
        self.wells = [Node(coordinates, idx) for idx, coordinates in enumerate(wells)]
        self.houses = [Node(coordinates, idx) for idx, coordinates in enumerate(houses)]

        if not empty_edges:
            self.edges = self.construct_edges(self.wells)

    @classmethod
    def create_from_nodes(cls,
                          n: int,
                          k: int,
                          wells: List[Node],
                          houses: List[Node],
                          empty_edges: bool = False):
        '''
        Parameters:
        n - number of wells
        k - number of houses per well
        wells - list of well nodes
        houses - list of house nodes
        empty_edges - flag indicating if the graph should be initialized without edges
        '''
        wells_coords = [[well.x, well.y] for well in wells]
        houses_coords = [[house.x, house.y] for house in houses]

        return cls(n, k, wells_coords, houses_coords, empty_edges)

    def construct_edges(self, wells: List[Node]) -> List[Edge]:
        '''
        Method constructs edges between each well and each house.
        The values of edges are assigned with the negative of the euclidean distance between each edge and well.

        Parameters:
        wells - set of wells based on which edges are to be constructed
        
        Returns: List of edges where each edge is described by the 3-element tuple (well_idx, house_idx, distance)
        '''
        edges = []
        for well in wells:
            for house in self.houses:
                distance = well.compute_distance(house)
                edge = Edge(house, well, -distance)
                edges.append(edge)
                house.edges.append(edge)
                well.edges.append(edge)
        return edges
    
    def duplicate_wells(self):
        '''
        Method duplicates a set of wells and adds corresponding edges.
        '''
        wells = self.wells

        for _ in range(0, self.k - 1):
            self.wells.append(wells)
            self.edges.append(self.construct_edges(wells))
