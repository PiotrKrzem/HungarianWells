from src.models.node import Node

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