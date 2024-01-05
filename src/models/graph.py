import numpy as np

from typing import List
from src.models.node import Node
from src.models.edge import Edge

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
    def create_from_coords(cls, 
                           n: int, 
                           k: int,
                           wells: List[Node], 
                           houses: List[Node]):
        '''
        Parameters:
        n - number of wells
        k - number of houses per well
        wells - list of well nodes
        houses - list of house nodes
        '''
        wells_coords = [[well.x, well.y] for well in wells]
        houses_coords = [[house.x, house.y] for house in houses]

        return cls(n, k, wells_coords, houses_coords, True)

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
        return edges
    
    def duplicate_wells(self):
        '''
        Method duplicates a set of wells and adds corresponding edges.
        '''
        wells = self.wells

        for _ in range(0, self.k - 1):
            self.wells.append(wells)
            self.edges.append(self.construct_edges(wells))
