from typing import List
from src.models.graph import Edge, Node, NodeType

class Matching():
    '''
    Class represents a matching in the graph.

    Attributes:
    ----------
    edges : List[Edge]
        list of edges belonging to the mapping
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
        ----------
        edges : List[Edge]
            set of edges that are to be verified

        Returns:
        -------
        Boolean indicating if matching contains some edge
        '''
        matching_edges = [(edge.house.idx, edge.well.idx) for edge in self.edges]
        for edge in edges:
            if (edge.house.idx, edge.well.idx) in matching_edges:
                return True
            
        return False
    


    def contains_edge(self, new_edge: Edge) -> bool:
        '''
        Method verifies if the edge of the given house and well is in the set of edges.

        Parameters:
        ----------
        new_edge : Edge
            edge to be verified

        Returns:
        -------
        Boolean indicating if given edge is within matching
        '''
        for edge in self.edges:
            if edge.house.idx == new_edge.house.idx and edge.well.idx == new_edge.well.idx:
                return True
            
        return False
    

    
    def contains_node(self, node: Node) -> bool:
        '''
        Method verifies if the node is in the set of edges.

        Parameters:
        ----------
        node : Node
            source node

        Returns:
        -------
        Boolean indicating if given node is within matching.
        '''
        is_well = NodeType.WELL == node.type
        for edge in self.edges:
            if ((not is_well) and edge.house.idx == node.idx) or (is_well and edge.well.idx == node.idx):
                return True     
        return False
    

    
    def remove_edge(self, house: Node, well: Node) -> None:
        '''
        Method removes edge of given house and well.

        Parameters:
        ----------
        house : Node
            house node
        well : Node
            well node
        '''
        self.edges = [edge for edge in self.edges if not (edge.house.idx == house.idx and edge.well.idx == well.idx)]
