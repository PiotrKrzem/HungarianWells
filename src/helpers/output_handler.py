import numpy as np

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
    
    matching_wells = list(set([edge.well for edge in matching.edges]))
    matching_houses = []

    for well in matching_wells:
        matching_houses.append([edge.house for edge in matching.edges if edge.well.idx == well.idx])

    for i in range(len(matching_wells)):
        output.write(f"W{i + 1}({matching_wells[i].x},{matching_wells[i].y}) -> ")
        for j in range(len(matching_houses[i])):
            output.write(f"H{i * graph.k + j + 1}({matching_houses[i][j].x},{matching_houses[i][j].y})")
            if j < graph.k - 1:
                output.write(",")
        output.write("\n")

    total_cost = -sum([edge.weight for edge in matching.edges])
    output.write(f"Total Cost: {total_cost}\n")

    output.close()