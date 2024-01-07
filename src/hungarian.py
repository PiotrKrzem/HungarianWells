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
            edge_copy = Edge(equality_graph.houses[edge.house.idx], equality_graph.wells[edge.well.idx], edge.weight)
            equality_graph.edges.append(edge_copy)
            equality_graph.houses[edge.house.idx].edges.append(edge_copy)
            equality_graph.wells[edge.well.idx].edges.append(edge_copy)
    
    return equality_graph



def find_augmenting_paths(starting_node: Node, matching: Matching) -> Tuple[List[Node], bool]:
    '''
    Method aims to find an augmenting path.
    If such path does not exists, it returns the last available alternating path.

    Parameters:
    ----------
    starting_node : Node
        node from which the path search starts
    matching : Matching
        current matching in a graph
    
    Returns:
    -------
    Tuple (found path, flag if path is augmenting)
    '''
    queue = [(starting_node, [starting_node], False)]
    alternating_path = []

    while queue:
        current, path, should_be_in_matching = queue.pop(0)

        queue_extended = False
        for edge in current.edges:
            if edge.is_in_matching(matching) == should_be_in_matching:
                neighbor = edge.get_adj_node(current)

                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor], not should_be_in_matching))
                    queue_extended = True

        if not queue_extended:
            if len(path) >= 2 and len(path) % 2 == 0 and is_augmenting(path, matching):
                return path, True
            elif len(path) > len(alternating_path):
                alternating_path = path

    if len(alternating_path) == 0:
        print("!!!!Empty alternating path!!!!")

    return alternating_path, False

def find_augmenting_paths_dfs(starting_node: Node, matching: Matching) -> Tuple[List[Node], bool]:
    '''
    Method aims to find an augmenting path.
    If such path does not exist, it returns the last available alternating path.

    Parameters:
    ----------
    starting_node : Node
        node from which the path search starts
    matching : Matching
        current matching in a graph
    
    Returns:
    -------
    Tuple (found path, flag if path is augmenting)
    '''
    stack = [(starting_node, [starting_node], False)]
    visited = [starting_node]
    alternating_path = []

    while stack:
        current, path, should_be_in_matching = stack.pop()

        adj_nodes = [edge.get_adj_node(current) for edge in current.edges if edge.is_in_matching(matching) == should_be_in_matching]

        stack_extended = False
        for neighbor in adj_nodes:
            if neighbor not in path and neighbor not in visited:
                stack.append((neighbor, path + [neighbor], not should_be_in_matching))
                stack_extended = True

        if not stack_extended:
            if len(path) >= 2 and is_augmenting(path, matching):
                return path, True
            else:
                visited.append(current)
                alternating_path = path
        
        print(len(stack))

    return alternating_path, False

def find_augmenting_paths_dfs_quick(starting_node: Node, matching: Matching) -> Tuple[List[Node], bool]:
    '''
    Method aims to find an augmenting path.
    If such path does not exist, it returns the last available alternating path.

    Parameters:
    ----------
    starting_node : Node
        node from which the path search starts
    matching : Matching
        current matching in a graph
    
    Returns:
    -------
    Tuple (found path, flag if path is augmenting)
    '''
    stack = [(starting_node, [starting_node], False)]

    while stack:
        current, path, should_be_in_matching = stack.pop()

        adj_nodes = [edge.get_adj_node(current) for edge in current.edges if edge.is_in_matching(matching) == should_be_in_matching]

        stack_extended = False
        for neighbor in adj_nodes:
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor], not should_be_in_matching))
                stack_extended = True
                break

        if not stack_extended:
            if len(path) >= 2 and is_augmenting(path, matching):
                return path, True
            else:
                return path, False


def is_augmenting(path: List[Node], matching: Matching):
    '''
    Method verifies if alternating path is an augmenting path.

    Parameters:
    ----------
    path : List[Node]
        alternating path to be verified
    matching : Matching
        current matching in a graph

    Returns:
    -------
    Boolean indicating if path is augmenting.
    '''
    return (not matching.contains_node(path[0])) and (not matching.contains_node(path[-1])) 



def find_augmenting_path(graph: Graph, matching: Matching) -> Tuple[List[Node], bool]:
    '''
    Method constructs augmenting path.

    Parameters:
    ----------
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
            return find_augmenting_paths(starting_node, matching)
            return find_augmenting_paths_dfs(starting_node, matching)
            return find_augmenting_paths_dfs_quick(starting_node, matching)

    return [], False



def label_modification(graph: Graph, path: List[Node]) -> Graph:
    '''
    Method performs labels modification.

    Parameters:
    ----------
    graph : Graph
        graph which labels are to be modified
    path : List[Node]
        alternating path of the graph

    Returns:
    -------
    Graph with modified labels.
    '''
    path_indexes = [node.idx for node in path]

    houses_in_path = path_indexes[::2]
    wells_in_path = path_indexes[1::2]

    S: List[int] =         [h.idx for h in graph.houses if h.idx in houses_in_path]
    W_minus_T: List[int] = [w.idx for w in graph.wells  if w.idx not in wells_in_path]

    deltas = []
    for edge in graph.edges:
        if edge.house.idx in S and edge.well.idx in W_minus_T:
            deltas.append(edge.house.label + edge.well.label - edge.weight)

    min_delta = min(deltas)

    for house in graph.houses:
        if house.idx in S:
            house.label -= min_delta

    for well in graph.wells:
        if well.idx in wells_in_path:
            well.label += min_delta

    return graph



def matching_modification(path: List[Node], matching: Matching) -> Matching:
    '''
    Method performs modification of current matching.
    
    Parameters:
    ----------
    path : List[Node]
        alternating path in graph 
    matching : Matching
        matching in graph

    Returns:
    -------
    Modified matching.
    '''
    for i in range(0, len(path) - 1):
        house = i     if i % 2 == 0 else i + 1
        well  = i + 1 if i % 2 == 0 else i

        house_node = path[house]
        well_node  = path[well]

        if matching.contains_edge(house_node, well_node):
            matching.remove_edge(house_node, well_node)
        else:
            distance = well_node.compute_weight(house_node)
            matching.edges.append(Edge(house_node, well_node, distance))
    
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

    while True:
        # Step 5: Construct augmenting path
        path, is_augmenting = find_augmenting_path(graph_l, M)

        if not is_augmenting:
            # Step 6: Label modification
            duplicate_graph = label_modification(duplicate_graph, path)
            graph_l = equality_graph(duplicate_graph)
        else:   
            # Step 7: Matching modification
            M = matching_modification(path, M)

        # Step 8: Optimal assignment check
        if optimal_assignment_check(graph_l, M):
            break
    
    return graph, M

def test_hungarian(input_file: str) -> Tuple[Graph, Matching]:
    '''
    Method test full hungarian algorithm for given input file, with added security for infinite iterations.

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

    i = 0
    edges = duplicate_graph.n * duplicate_graph.k
    threshold = edges * edges

    while True:
        # Step 5: Construct augmenting path
        path, is_augmenting = find_augmenting_path(graph_l, M)

        print(f"Augm: {is_augmenting}")
        if not is_augmenting:
            # Step 6: Label modification
            duplicate_graph = label_modification(duplicate_graph, path)
            print(f"label_modification {len(graph_l.edges)}", end = '')
            graph_l = equality_graph(duplicate_graph)
            print(f"-> {len(graph_l.edges)}")

        else:   
            # Step 7: Matching modification
            print(f"matching_modification p{(len(path))} e{len(M.edges)}", end='')
            M = matching_modification(path, M)
            print(f"->{len(M.edges)}/{len(graph.houses)}")

        # Step 8: Optimal assignment check
        if optimal_assignment_check(graph_l, M):
            break

        # Security check
        if i == threshold:
            print(f"{i//edges}/{edges}")
            raise InterruptedError(f"Threshold reached for {graph.n}x{graph.k}")
        else:
            i += 1
            if i % edges == 0:
                print(f"{i//edges}/{edges}")

    return graph, M
