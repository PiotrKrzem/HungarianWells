import numpy as np
from typing import List

class Edge: pass # to avoid circular dependency

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

from src.models.edge import Edge