from src.models.matching import Matching
from src.models.graph import Graph

def write_to_output(graph: Graph, matching: Matching, output_file: str):
    '''
    Method writes results of matching to indicated output file.

    Parameters:
    matching - resulting matching
    output_file - name of the file to which the results are to be stores
    '''

    try:
        output = open(output_file, 'w')  # Open the file in write mode
    except IOError:
        raise FileNotFoundError(f"Error: Unable to open output file {output_file}")

    for i in range(graph.n):
        output.write(f"W{i + 1}({graph.wells[i]['x']},{graph.wells[i]['y']}) -> ")
        for j in range(graph.k):
            output.write(f"H{i * graph.k + j + 1}({graph.houses[i * graph.k + j]['x']},{graph.houses[i * graph.k + j]['y']})")
            if j < graph.k - 1:
                output.write(",")
    output.write("\n")

    total_cost = -sum([graph.edges[graph.edges.index(edge)].weight for edge in matching.edges])
    output.write(f"Total Cost: {total_cost}\n")

    output.close()