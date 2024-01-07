import numpy as np
import math

from typing import List
from enum import Enum, auto

class Matching: pass # defined to avoid circularity in dependencies

class NodeType(Enum):
    '''
    An enum with possible node types.

    Available types:
    ---------------
    WELL, HOUSE
    '''
    WELL = auto()
    HOUSE = auto()

class Node():
    '''
    Class represents single graph node.

    Attributes:
    ----------
    idx : int
        index of the given node in graph's array
    x : float
        x coordinate of the given node
    y : float
        y coordinate of the given node
    label : int
        label assigned to the given node
    edges : List[Edge]
        list of edges to which a node belongs
    type : NodeType
        type of the node
    '''

    def __init__(self, 
                 coordinates: np.ndarray, 
                 idx: int,
                 node_type: NodeType,
                 label: int = 0) -> None:
        '''
        Parameters:
        ----------
        coordinates : np.ndarray
            x and y coordinates of a point
        idx : int
            index of the node in the list of nodes in graph
        node_type : NodeType
            type of the node (HOUSE or WELL)
        label : int, optional (default = 0)
            label assigned to the node
        '''
        self.idx = idx
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.label = label
        self.edges: List[Edge] = []
        self.type = node_type



    def compute_weight(self, node) -> int:
        '''
        Method computes weight of edge connecting two points.

        Parameters:
        ----------
        node : Node
            node of a point with which the edge's weight is to be computed

        Return
        ------
        Negative of euclidean distance between two points.
        '''
        return -int(round(math.dist([self.x, self.y], [node.x, node.y]), 2) * 100)


    
    def get_weights_of_edges(self) -> List[int]:
        '''
        Method returns a list of weights of all edges that go from the given node.

        Returns:
        -------
        List of edges' weights.
        '''
        return [edge.weight for edge in self.edges]

class Edge():
    '''
    Class describing edge in the graph.

    Attributes:
    ----------
    house : Node
        house node of the given edge
    well : Node
        well node of the given edge
    weight : int
        weight of the given edge
    '''

    def __init__(self, house: Node, well: Node, weight: int) -> None:
        '''
        Parameters:
        ----------
        house : Node
            house node
        well : Node
            well node
        weight : int
            weight of the edge
        '''
        self.house = house
        self.well = well
        self.weight = weight


    
    def get_adj_node(self, node: Node) -> Node:
        '''
        Method retrieves adjacent node (i.e. node on the other side of the edge).

        Parameters:
        ----------
        node : Node
            first node

        Returns:
        -------
        Second node of the edge.
        '''
        return self.house if node.type == NodeType.WELL else self.well
    

    
    def is_in_matching(self, matching: Matching) -> bool:
        '''
        Method verifies if the edge is contained within the matching.

        Parameters:
        ----------
        matching : Matching
            matching that is considered

        Returns:
        --------
        Boolean indicating if the edge is within the matching
        '''
        return matching.contains_edge(self.house, self.well)

class Graph():
    '''
    Class representing graph used in Hungarian algorithm.

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
    edges : List[Edge]
        edges belonging to the given graph
    '''

    def __init__(self, 
                 n: int, 
                 k: int, 
                 wells_coords: List[np.ndarray], 
                 houses_coords: List[np.ndarray],
                 wells_labels: List[int] = None,
                 houses_labels: List[int] = None,
                 empty_edges: bool = False) -> None:
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
        wells_labels : List[int], optional
            list of labels of wells
        houses_labels : List[int], optional
            list of labels of houses
        empty_edges : bool, optional
            flag indicating if the graph should be initialized without edges
        '''
        self.n = n
        self.k = k
        self.wells = [Node(coordinates, idx, NodeType.WELL) if wells_labels == None else 
                      Node(coordinates, idx, NodeType.WELL, wells_labels[idx]) for idx, coordinates in enumerate(wells_coords)]
        self.houses = [Node(coordinates, idx, NodeType.HOUSE) if houses_labels == None else 
                      Node(coordinates, idx, NodeType.HOUSE, houses_labels[idx]) for idx, coordinates in enumerate(houses_coords)]
        self.edges: List[Edge] = self.construct_edges(self.wells) if not empty_edges else []



    @classmethod
    def create_from_nodes(cls,
                          n: int,
                          k: int,
                          wells: List[Node],
                          houses: List[Node],
                          empty_edges: bool = False):
        '''
        Method allows constructing graph from predefined nodes and not only coordinates.

        Parameters:
        ----------
        n : int
            number of wells
        k : int
            number of houses per well
        wells : List[Node]
            wells that create a graph
        houses : List[Node]
            houses that create a graph
        empty_edges : bool, optional
            flag indicating if the graph should be initialized without edges
        '''
        wells_coords = [[well.x, well.y] for well in wells]
        houses_coords = [[house.x, house.y] for house in houses]

        wells_labels = [well.label for well in wells]
        houses_labels = [house.label for house in houses]

        return cls(n, k, wells_coords, houses_coords, wells_labels, houses_labels, empty_edges)



    def construct_edges(self, wells: List[Node]) -> List[Edge]:
        '''
        Method constructs edges between each well and each house.
        The values of edges are assigned with the negative of the euclidean distance between each house and well.

        Parameters:
        ----------
        wells : List[Node]
            set of wells based on which edges are to be constructed
        
        Returns:
        -------
        List of edges where each edge is described by the 3-element tuple (well_idx, house_idx, distance).
        '''
        edges = []

        for well in wells:
            for house in self.houses:
                distance = well.compute_weight(house)
                edge = Edge(house, well, distance)
                edges.append(edge)
                house.edges.append(edge)
                well.edges.append(edge)
        return edges


from src.models.matching import Matching