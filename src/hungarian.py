from typing import List, Tuple

from src.helpers.input_handler import read_input
from src.models.graph import Graph, Node, Edge, NodeType
from src.models.matching import Matching

def duplicate_wells(graph: Graph) -> Graph:
    '''
    Method duplicates wells in the graph.

    Parameters:
    ----------
    graph : Graph
        graph with initial wells and houses nodes and edges

    Returns:
    -------
    Graph with duplicated wells.
    '''
    duplicate_wells = [Node([well.x, well.y], i * graph.k + j, NodeType.WELL, well.label) for i, well in enumerate(graph.wells) for j in range(graph.k)]
    duplicate_graph = Graph.create_from_nodes(graph.n * graph.k, graph.k, duplicate_wells, graph.houses)

    return duplicate_graph



def initial_labeling(duplicate_graph: Graph) -> Graph:
    '''
    Method performs initial labeling.

    Returns:
    -------
    Method returns graph with initialized labels.
    '''
    for i in range(duplicate_graph.n):
        duplicate_graph.wells[i].label = 0
        duplicate_graph.houses[i].label = max(duplicate_graph.houses[i].get_weights_of_edges())
    return duplicate_graph



def equality_graph(duplicate_graph: Graph) -> Graph:
    '''
    Method constructs the equality graph.

    Returns:
    -------
    Initialized equality graph.
    '''
    equality_graph: Graph = Graph.create_from_nodes(duplicate_graph.n, duplicate_graph.k, duplicate_graph.wells, duplicate_graph.houses, True)

    for i in range(0, duplicate_graph.n**2):
        edge = duplicate_graph.edges[i]
        if edge.weight == edge.house.label + edge.well.label:
            equality_graph.edges.append(edge)
            equality_graph.houses[edge.house.idx].add_edge(edge, equality_graph.wells[edge.well.idx])
            equality_graph.wells[edge.well.idx].add_edge(edge, equality_graph.houses[edge.house.idx])
    
    return equality_graph


def find_augmenting_paths(traversed_paths: List[List[Tuple[Node, Edge]]], 
                          starting_node: Node, 
                          matching: Matching) -> Tuple[List[Tuple[Node, Edge]], bool]:
    '''
    Method aims to find an augmenting path.
    If such path does not exists, it returns the last available alternating path.

    Parameters:
    ----------
    traversed_paths : List[List[Tuple[Node, Edge]]]
        list of paths which have been traversed and did not improve the matching
    starting_node : Node
        node from which the path search starts
    matching : Matching
        current matching in a graph
    
    Returns:
    -------
    Tuple (found path, flag if path is augmenting)
    '''
    queue = [(starting_node, [starting_node], [(starting_node, None)], False)]
    alternating_path = []

    while queue:
        current, path_nodes, path, should_be_in_matching = queue.pop(0)

        queue_extended = False
        for neighbor, edge in current.adj_nodes:
            if neighbor not in path_nodes and edge.in_matching == should_be_in_matching:
                queue.append((neighbor, path_nodes + [neighbor], path + [(neighbor, edge)], not should_be_in_matching))
                queue_extended = True

        if not queue_extended:
            if len(path) >= 2 and is_augmenting(path, matching):
                return path, True
            elif path not in traversed_paths and len(path) > len(alternating_path):
                alternating_path = path

    return alternating_path, False



def is_augmenting(path: List[Tuple[Node, Edge]], matching: Matching):
    '''
    Method verifies if alternating path is an augmenting path.

    Parameters:
    ----------
    path : List[Tuple[Node, Edge]]
        alternating path to be verified
    matching : Matching
        current matching in a graph

    Returns:
    -------
    Boolean indicating if path is augmenting.
    '''
    return (not matching.contains_node(path[0][0])) and (not matching.contains_node(path[-1][0])) 
    


def find_augmenting_path(traversed_paths: List[List[Tuple[Node, Edge]]], 
                         graph: Graph, 
                         matching: Matching) -> Tuple[List[Node], bool]:
    '''
    Method constructs augmenting path.

    Parameters:
    ----------
    traversed_paths : List[List[Tuple[Node, Edge]]]
        list of paths which have been traversed and did not improve the matching
    graph : Graph
        graph in which augmenting path is to be found
    matching : Matching
        current matching in a graph

    Returns:
    -------
    Tuple (alternating path, boolean indicating if path is augmenting).
    '''
    for i in range(graph.n):
        if not matching.contains_any(graph.houses[i].edges):
            starting_node = graph.houses[i]
            return find_augmenting_paths(traversed_paths, starting_node, matching)
    
    return [], False



def label_modification(graph: Graph, path: List[Tuple[Node, Edge]]) -> Graph:
    '''
    Method performs labels modification.

    Parameters:
    ----------
    graph : Graph
        graph which labels are to be modified
    path : List[Tuple[Node, Edge]]
        alternating path of the graph

    Returns:
    -------
    Graph with modified labels.
    '''
    path_indexes = [node.idx for node, _ in path]

    houses_in_path = path_indexes[::2]
    wells_in_path = path_indexes[1::2]

    S: List[int] = [h.idx for h in graph.houses if h.idx in houses_in_path]
    W_minus_T: List[int] = [w.idx for w in graph.wells if w.idx not in wells_in_path]

    deltas = []
    for edge in graph.edges:
        if edge.house.idx in S and edge.well.idx in W_minus_T and edge.house.label + edge.well.label - edge.weight != 0:
            deltas.append(edge.house.label + edge.well.label - edge.weight)

    min_delta = min(deltas)

    for house in graph.houses:
        if house.idx in S:
            house.label -= min_delta

    for well in graph.wells:
        if well.idx in wells_in_path:
            well.label += min_delta

    return (graph, min_delta)



def matching_modification(path: List[Tuple[Node, Edge]], matching: Matching) -> Matching:
    '''
    Method performs modification of current matching.
    
    Parameters:
    ----------
    path : List[Tuple[Node, Edge]]
        alternating path in graph 
    matching : Matching
        matching in graph

    Returns:
    -------
    Modified matching.
    '''
    for i in range(0, len(path) - 1):
        house = i if i % 2 == 0 else i + 1
        well = i + 1 if i % 2 == 0 else i

        house_node = path[house][0]
        well_node = path[well][0]

        if matching.contains_edge(path[i+1][1]):
            matching.remove_edge(house_node, well_node)
            path[i+1][1].in_matching = False
        else:
            distance = well_node.compute_weight(house_node)
            matching.edges.append(Edge(house_node, well_node, distance))
            path[i+1][1].in_matching = True
    
    return matching




def optimal_assignment_check(graph: Graph, matching: Matching) -> bool:
    '''
    Method verifies if the assignment is optimal.

    Parameters:
    ----------
    graph : Graph
        graph for which assignment is to be verified
    matching : Matching
        current matching

    Returns:
    -------
    Boolean indicating if the assignment is optimal.
    '''
    for house in graph.houses:
        if not matching.contains_any(house.edges):
            return False
    return True


def run_hungarian(input_file: str) -> Tuple[Graph, Matching]:
    '''
    Method runs full hungarian algorithm for given input file.

    Parameters:
    ----------
    input_file : str
        input file

    Returns:
    -------
    Optimal matching.
    '''
    # Step 0: Read and construct graph based on the input file
    graph = read_input(input_file)

    # Step 1: Initialize empty matching
    M = Matching()

    # Step 2: Duplicate wells
    duplicate_graph = duplicate_wells(graph)

    # Step 3: Initial feasible labeling
    duplicate_graph = initial_labeling(duplicate_graph)

    # Step 4: Construct equality graph
    graph_l = equality_graph(duplicate_graph)
    traversed_paths = []

    while True:
        # Step 5: Construct augmenting path
        path, is_augmenting = find_augmenting_path(traversed_paths, graph_l, M)

        if not is_augmenting:
            # Step 6: Label modification
            duplicate_graph, min_delta = label_modification(duplicate_graph, path)
            if min_delta == 0:
                traversed_paths.append(path)
            else:
                graph_l = equality_graph(duplicate_graph)
                traversed_paths.clear()
        else:   
            # Step 7: Matching modification
            M = matching_modification(path, M)

        # Step 8: Optimal assignment check
        if optimal_assignment_check(graph_l, M):
            break
    
    return graph, M
