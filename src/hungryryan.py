import numpy as np
from typing import List, Tuple

from src.helpers.input_handler import read_input
from src.models.graph import Graph, InitialGraph
from src.models.matching import Matching
from src.models.constants import *

import warnings
warnings.filterwarnings('error')


def duplicate_wells(initial_graph: InitialGraph) -> Graph:
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
    n = initial_graph.n * initial_graph.k
    wells_coordinates = np.repeat(initial_graph.wells_coordinates, initial_graph.k, axis=0)
    houses_coordinates = initial_graph.houses_coordinates

    duplicate_graph = Graph(n, wells_coordinates, houses_coordinates)

    return duplicate_graph



def initial_labeling(duplicate_graph: Graph) -> Graph:
    '''
    Method performs initial labeling.

    Returns:
    -------
    Method returns graph with initialized labels.
    '''
    duplicate_graph.initial_labeling()
    return duplicate_graph


def equality_graph(duplicate_graph: Graph, root: int) -> Graph:
    '''
    Method constructs the equality graph.

    Returns:
    -------
    Initialized equality graph.
    '''
    duplicate_graph.compute_slack(root)
    
    return duplicate_graph



def find_root_of_alternating_path(graph: Graph, M: Matching):
    root: int
    for well in range(graph.n):
        if M.matching_house[well] == UNMATCHED_NODE:
            graph.queue[graph.write] = well
            root = well
            graph.write = graph.write + 1

            graph.previous_well[well] = ROOT_NODE
            graph.S[well] = TRUE

            break

    return root


def find_augmenting_path(graph: Graph, matching: Matching) -> Tuple[int, int, bool]:
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
    while graph.read < graph.write:
        well = graph.queue[graph.read]
        graph.read = graph.read + 1

        for house in range(graph.n):
            if graph.cost_matrix[well][house] == graph.label_well[well] + graph.label_house[house] and graph.T[house] == FALSE:
                if matching.matching_well[house] == UNMATCHED_NODE: # Path found
                    return well, house, True 
                graph.T[house] = TRUE
                graph.queue[graph.write] = matching.matching_well[house]
                graph.write = graph.write + 1
                graph.add_to_alternating_tree(matching.matching_well[house], well)

    return UNKNOWN_NODE, UNKNOWN_NODE, False



def label_modification(graph: Graph) -> Graph:
    '''
    Method performs labels modification.

    Parameters:
    ----------
    graph : Graph
        graph which labels are to be modified
    path_nodes : List[Tuple[int, NodeType]]
        alternating path of the graph

    Returns:
    -------
    Graph with modified labels.
    '''
    delta = float('inf')
    for house in range(graph.n):
        if graph.T[house] == FALSE:
            delta = min(delta, graph.slack[house])

    for well in range(graph.n):
        if graph.S[well] == TRUE:
            graph.label_well[well] -= delta

    for house in range(graph.n):
        if graph.T[house] == TRUE:
            graph.label_house[house] += delta

    for house in range(graph.n):
        if graph.T[house] == FALSE:
            graph.slack[house] -= delta

    return graph


def matching_modification(well:int, house:int, graph:Graph, matching: Matching) -> Matching:
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
    matching.matched_count += 1

    # in this cycle, we inverse edges along the augmenting path
    current_well, current_house = well, house
    while current_well != ROOT_NODE:
        target_house = matching.matching_house[current_well]
        matching.matching_well[current_house] = current_well
        matching.matching_house[current_well] = current_house
        current_well, current_house = graph.previous_well[current_well], target_house

    return matching


def optimal_assignment_check(matching: Matching) -> bool:
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
    return matching.matched_count == matching.n

def refine_augmenting_tree_with_new_edges(graph: Graph, matching: Matching) -> Tuple[int, int, bool]:
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
    graph.write = 0
    graph.read = 0
    for house in range(graph.n):
        # in this cycle, we add edges that were added to the equality graph as a
        # result of improving the labeling, we add edge (slackx[y], y) to the tree if
        # and only if not T[y] and slack[y] == 0, also with this edge we add another one
        # (y, yx[y]) or augment the matching, if y was exposed
        if graph.T[house] == FALSE and graph.slack[house] == 0:
            if matching.matching_well[house] == UNKNOWN_NODE:  # exposed vertex in Y found - augmenting path exists!
                well = graph.slack_matching_well[house]
                return well, house, True
            else:
                graph.T[house] = TRUE  # else just add y to T
                if graph.S[matching.matching_well[house]] == FALSE:
                    graph.queue[graph.write] = matching.matching_well[house]
                    graph.write += 1
                    graph.add_to_alternating_tree(matching.matching_well[house], graph.slack_matching_well[house])  # and add edges (x, y) and (y, yx[y]) to the tree

    return UNKNOWN_NODE, UNKNOWN_NODE, False



def run_hungryryan(input_file: str) -> Tuple[Graph, Matching]:
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
    ret = 0
    # Step 0: Read and construct graph based on the input file
    initial_graph = read_input(input_file)

    # Step 1: Duplicate wells
    duplicate_graph = duplicate_wells(initial_graph)

    # Step 2: Initialize empty matching
    M = Matching(duplicate_graph.n)

    # Step 3: Initial feasible labeling
    duplicate_graph = initial_labeling(duplicate_graph)

    # Step 4: Optimal assignment check
    while not optimal_assignment_check(M):

        # Step 5: Reset alternating tree
        duplicate_graph.clean_alternating_tree()

        # Step 6: Find the starting well for the search of augmenting path
        well_root = find_root_of_alternating_path(duplicate_graph, M)

        # Step 7: Construct equality graph (initialize slack)
        graph_l = equality_graph(duplicate_graph, well_root)

        while True:
            # Step 8: Construct augmenting path
            last_well_in_path, last_house_in_path, found_augmenting_path = find_augmenting_path(graph_l, M)

            if not found_augmenting_path:
                # Step 9: Label modification
                duplicate_graph = label_modification(duplicate_graph)
                last_well_in_path, last_house_in_path, found_augmenting_path = refine_augmenting_tree_with_new_edges(duplicate_graph, M)

            if found_augmenting_path: # Goto matching modification
                break

        if found_augmenting_path:
            # Step 10: Matching modification
            M = matching_modification(last_well_in_path, last_house_in_path, duplicate_graph, M)

    for x in range(graph_l.n):
        ret += graph_l.cost_matrix[x][M.matching_house[x]]
    print(ret)
    return initial_graph, M
