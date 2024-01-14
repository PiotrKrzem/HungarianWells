import numpy as np

from typing import List
from src.models.constants import *


class Matching():
    '''
    Class represents a matching in the graph.

    Attributes:
    ----------
    edges : List[Edge]
        list of edges belonging to the mapping
    '''

    def __init__(self, n) -> None:
        '''
        Constructor of empty matching.
        '''
        self.n = n

        self.matching_house = np.full(n, UNMATCHED_NODE, dtype=np.int32)
        self.matching_well = np.full(n, UNMATCHED_NODE, dtype=np.int32)
        self.matched_count = 0
