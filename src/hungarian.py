import subprocess

from src.models.graph import Graph
from src.models.matching import Matching

def duplicate_wells(graph: Graph) -> Graph:
    '''
    Method duplicates wells in the graph.

    Parameters:
    graph - graph with initial wells and houses nodes and edges

    Returns: graph with duplicated wells
    '''
    graph_copy = Graph(graph.n, graph.k, graph.wells, graph.houses)
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
    
    return equality_graph

def find_augmenting_path(equality_graph: Graph, matching: Matching) -> Graph:
    '''
    Method constructs augmenting path.

    Parameters:
    equality_graph - equality graph
    matching - current matching

    Returns: 
    '''
    kn = equality_graph.k * equality_graph.n
    new_graph = Graph()
    
    for i in range(0, kn):
        if not matching.contains_any(equality_graph.houses[i].edges):
            starting_node = equality_graph.houses[i]

    
    return equality_graph

def execute_exe_hungarian(N, K, input_file, output_file):
    try:
        subprocess.run(f"Hungarian_64.exe {input_file} {output_file}")
        return
    except Exception as e:
        print(f"{e}")

    try:
        subprocess.run(f"Hungarian_32.exe {input_file} {output_file}")
        return
    except Exception as e:
        print(f"{e}")

    print("Both Hungarian executables failed.")