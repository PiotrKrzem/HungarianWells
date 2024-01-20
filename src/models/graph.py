import numpy as np
import math

from typing import List, Tuple
from enum import Enum, auto

from src.models.constants import *

class InitialGraph:
    '''
    Class representing initial graph.

    Attributes:
    ----------
    n : int
        number of wells in a graph
    k : int
        number of houses per well in a graph
    wells : List[Node]
        wells belonging to the given graph
    houses : List[Node]
        houses belonging to the given graph
    '''

    def __init__(self, 
                 n: int, 
                 k: int, 
                 wells_coordinates: np.ndarray, 
                 houses_coordinates: np.ndarray) -> None:
        '''
        Parameters:
        ----------
        n : int
            number of wells
        k : int
            number of houses per well
        wells_coords : List[np.ndarray]
            list of coordinates of wells
        houses_coords : List[np.ndarray]
            list of coordinates of houses
        wells_labels : List[float], optional
            list of labels of wells
        houses_labels : List[float], optional
            list of labels of houses
        empty_edges : bool, optional
            flag indicating if the graph should be initialized without edges
        '''
        self.n = n
        self.k = k

        self.wells_coordinates = wells_coordinates
        self.houses_coordinates = houses_coordinates

    @staticmethod
    def distance(well_x, well_y, house_x, house_y) -> int:
        return int(round(math.dist([well_x, well_y], [house_x, house_y]), 2) * 100)
    
    @staticmethod
    def precise_distance(well_x, well_y, house_x, house_y) -> float:
        return round(math.dist([well_x, well_y], [house_x, house_y]), 6)

class Graph(InitialGraph):
    '''
    Class representing graph used throughout Hungarian algorithm.

    Attributes:
    ----------
    n : int
        number of wells in a graph. Must be equal to k.
    k : int
        number of houses per well in a graph. Must be equal to n.
    wells : List[Node]
        wells belonging to the given graph
    houses : List[Node]
        houses belonging to the given graph
    '''

    def __init__(self, 
                 n: int, 
                 wells_coordinates: np.ndarray, 
                 houses_coordinates: np.ndarray
                 ) -> None:
        '''
        Parameters:
        ----------
        n : int
            number of wells
        k : int
            number of houses per well
        wells_coords : List[np.ndarray]
            list of coordinates of wells
        houses_coords : List[np.ndarray]
            list of coordinates of houses
        '''
        self.n = n

        self.wells_coordinates = wells_coordinates
        self.houses_coordinates = houses_coordinates

        self.label_well = np.zeros(self.n, dtype=np.int32)
        self.label_house = np.zeros(self.n, dtype=np.int32)

        self.cost_matrix = np.empty((self.n, self.n), dtype=np.int32)

        self.compute_distances()
        self.clean_alternating_tree()

    def compute_distances(self):
        for well in range(self.n):
            for house in range(self.n):
                well_x, well_y = self.wells_coordinates[well]
                house_x, house_y = self.houses_coordinates[house]
                self.cost_matrix[well][house] = InitialGraph.distance(well_x, well_y, house_x, house_y)

        self.cost_matrix = self.cost_matrix.max() - self.cost_matrix

    def initial_labeling(self):
        for well in range(self.n):
            for house in range(self.n):
                self.label_well[well] = max(self.label_well[well], self.cost_matrix[well][house])

    def compute_slack(self, root):
        for house in range(self.n):
            self.slack[house] = self.label_well[root] + self.label_house[house] - self.cost_matrix[root][house]
            self.slack_matching_well[house] = root

    def add_to_alternating_tree(self, well, previous_well):
        self.S[well] = TRUE
        self.previous_well[well] = previous_well

        for house in range(self.n):
            difference = self.label_well[well] + self.label_house[house] - self.cost_matrix[well][house]
            if difference < self.slack[house]:
                self.slack[house] = difference
                self.slack_matching_well[house] = well

    def clean_alternating_tree(self):
        # Augment first part
        self.queue = np.empty(self.n, dtype=np.int32)
        self.previous_well = np.full(self.n, UNKNOWN_NODE, dtype=np.int32)
        self.write = 0
        self.read = 0

        self.S = np.full(self.n, FALSE, dtype=np.int32)
        self.T = np.full(self.n, FALSE, dtype=np.int32)

        self.slack = np.empty(self.n, dtype=np.int32)
        self.slack_matching_well = np.empty(self.n, dtype=np.int32)
