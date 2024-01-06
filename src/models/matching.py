from typing import List
from src.models.graph import Edge, Node

class Matching():
    '''
    Class represents matching in the graph.
    '''

    def __init__(self) -> None:
        '''
        Constructor of empty matching.
        '''
        self.edges: List[Edge] = []

    def contains_any(self, edges: List[Edge]) -> bool:
        '''
        Method verifies if the matching contains any of the edges.

        Parameters:
        edges - set of edges that are to be verified

        Returns: boolean indicating if matching contains some edge
        '''
        matching_edges = [(edge.house.idx, edge.well.idx) for edge in self.edges]
        for edge in edges:
            if (edge.house.idx, edge.well.idx) in matching_edges:
                return True
            
        return False
    
    def contains_edge(self, src: Node, dst: Node) -> bool:
        '''
        Method verifies if the edge of the given source and destination is in the set of edges.

        Parameters:
        src - source node
        dst - destination node

        Returns: boolean indicating if given edge is within matching
        '''
        for edge in self.edges:
            if edge.house == src and edge.well == dst:
                return True
            
        return False
    
    def contains_node(self, node: Node, is_house: bool) -> bool:
        '''
        Method verifies if the node is in the set of edges.

        Parameters:
        node - source node
        is_house - flag indicating if the node is a house

        Returns: boolean indicating if given node is within matching
        '''
        for edge in self.edges:
            if (is_house and edge.house == node) or ((not is_house) and edge.well == node):
                return True
            
        return False
    
    def remove_edge(self, src: Node, dst: Node) -> None:
        '''
        Method removes edge of given source and destination.

        Parameters:
        src - source node
        dst - destination node
        '''
        edges = self.edges
        for edge in edges:
            if edge.house == src and edge.well == dst:
                self.edges.remove(edge)
                return
            
            