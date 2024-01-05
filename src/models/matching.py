from typing import List
from src.models.edge import Edge

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
        for edge in edges:
            if edge in self.edges:
                return True
            
        return False