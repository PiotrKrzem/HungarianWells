import subprocess

from typing import List, Tuple

from src.helpers.input_handler import read_input
from src.models.graph import Graph, Node, Edge
from src.models.matching import Matching

def duplicate_wells(graph: Graph) -> Graph:
    '''
    Method duplicates wells in the graph.

    Parameters:
    graph - graph with initial wells and houses nodes and edges

    Returns: graph with duplicated wells
    '''
    graph_copy = Graph.create_from_nodes(graph.n, graph.k, graph.wells, graph.houses)
    graph_copy.duplicate_wells()

    return graph_copy

def initial_labeling(graph: Graph) -> Graph:
    '''
    Method performs initial labeling.

    Returns: method returns graph with initialized labels.
    '''
    kn = graph.k * graph.n

    for i in range(0, kn):
        graph.houses[i].label = max(graph.houses[i].get_weights_of_edges())
        graph.wells[i].label = 0
    
    return graph

def equality_graph(graph: Graph) -> Graph:
    '''
    Method constructs the equality graph.

    Returns: initialized equality graph.
    '''
    kn = graph.k * graph.n
    equality_graph: Graph = Graph.create_from_coords(graph.n, graph.k, graph.wells, graph.houses)

    for i in range(0, kn**2):
        edge = graph.edges[i]
        if edge.weight == edge.src.label + edge.dst.label:
            equality_graph.edges.append(edge)
            equality_graph.houses[edge.src.idx].edges.append(edge)
            equality_graph.wells[edge.dst.idx].edges.append(edge)
    
    return equality_graph

def find_alternating_paths(graph: Graph, starting_node: Node):
    '''
    Method finds all alternating paths in a graph that start at a given node.

    Parameters:
    graph - graph in which path are to be found
    starting_node - node from which the search starts

    Returns: list of alternating paths
    '''
    visited = {node: False for node in graph.wells + graph.houses}
    queue = [(starting_node, [starting_node])]
    alternating_paths = []

    while queue:
        current, path = queue.pop(0)
        visited[current] = True

        if len(path) >= 2:
            alternating_paths.append(path)
        
        adj_nodes = [edge.dst if current in graph.wells else edge.src for edge in current.edges]
        for neighbor in adj_nodes:
            if not visited[neighbor]:
                queue.append((neighbor, path + [neighbor]))
                visited[neighbor] = True
    
    return alternating_paths

def is_augmenting(path: List[Node], matching: Matching):
    '''
    Method verifies if alternating path is an augmenting path.

    Parameters:
    path - alternating path to be verified
    matching - current matching

    Returns: boolean indicating if path is augmenting
    '''
    return not (matching.edges[0].src == path[0] or matching.edges[-1].dst == path[-1])
    

def find_augmenting_path(graph: Graph, matching: Matching) -> Tuple[List[Node], bool]:
    '''
    Method constructs augmenting path.

    Parameters:
    graph - graph in which augmenting path is to be found
    matching - current matching

    Returns: (alternating path, boolean indicating if path is augmenting)
    '''
    kn = graph.k * graph.n
    
    for i in range(0, kn):
        if not matching.contains_any(graph.houses[i].edges):
            starting_node = graph.houses[i]
            for p in find_alternating_paths(graph, starting_node):
                if is_augmenting(p):
                    return p, True
            return p, False
    
    return [], False

def label_modification(graph: Graph, path: List[Node]) -> Graph:
    '''
    Method performs labels modification.

    Parameters:
    graph - graph which labels are to be modified
    path - alternating path of the graph

    Returns: graph with modified labels
    '''
    S: List[Node] = []
    W_minus_T = graph.wells

    houses_in_path = path[::2]
    wells_in_path = path[1::2]

    for house in houses_in_path:
        S.append(house)
    for well in wells_in_path:
        W_minus_T.remove(well)

    deltas = []
    for edge in graph.edges:
        if edge.src in S and edge.dst in W_minus_T:
            deltas.append(edge.src.label + edge.dst.label - edge.weight)

    min_delta = min(deltas)

# TU SPRAWDZ
    for house in graph.houses:
        if house in S:
            edge.weight += min_delta

    for well in graph.wells:
        if well in wells_in_path:
            edge.weight -= min_delta

    return graph

def matching_modification(path: List[Node], matching: Matching) -> Matching:
    '''
    Method performs modification of current matching.
    
    Parameters:
    path - alternating path in graph 
    matching - matching in graph

    Returns: modified matching
    '''
    for i in range(0, len(path) - 1):
        src = i if i % 2 == 0 else i + 1
        dst = i + 1 if i % 2 == 0 else i

        src_node = path[src]
        dst_node = path[dst]

        if matching.contains_edge(src_node, dst_node):
            matching.remove_edge(src_node, dst_node)
        else:
            distance = dst_node.compute_distance(src_node)
            matching.edges.append(Edge(src_node, dst_node, distance))
    
    return matching

def optimal_assignment_check(graph: Graph, matching: Matching) -> bool:
    '''
    Method verifies if the assignment is optimal.

    Parameters:
    graph - graph for which assignment is to be verified
    matching - current matching

    Returns: boolean indicating if the assignment is optimal
    '''
    for house in graph.houses:
        if not matching.contains_any(house.edges):
            return False
        
    return True


def run_hungarian(input_file) -> Tuple[Graph, Matching]:
    '''
    Method runs full hungarian algorithm for given input file.

    Parameters:
    input_file - input file

    Returns: optimal matching
    '''
    # Step 0: Read and construct graph based on the input file
    graph = read_input(input_file)

    # Step 1: Initialize empty matching
    M = Matching()

    # Step 2: Duplicate wells
    graph = duplicate_wells(graph)

    # Step 3: Initial feasible labeling
    graph = initial_labeling(graph)

    while True:
        # Step 4: Construct equality graph
        graph_l = equality_graph(graph)

        # Step 5: Construct augmenting path
        path, is_augmenting = find_alternating_paths(graph_l, M)

        if not is_augmenting:
            # Step 6: Label modification
            graph = label_modification(equality_graph, path)
            continue

        # Step 7: Matching modification
        M = matching_modification(path, M)

        # Step 8: Optimal assignment check
        if optimal_assignment_check(graph_l, M):
            break
    
    return graph, M
