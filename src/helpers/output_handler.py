from src.models.graph import Node
from src.models.matching import Matching
from typing import List

def write_to_output(matching: Matching, wells: List[Node], output_file: str):
    '''
    Method writes results of matching to indicated output file.

    Parameters:
    ----------
    matching : Matching
        resulting matching
    wells : List[Node]
        list of wells
    output_file : str
        name of the file to which the results are to be stores
    '''
    try:
        output = open(output_file, 'w')
    except IOError:
        raise FileNotFoundError(f"Error: Unable to open output file {output_file}")
    
    matching_houses = []

    for well in wells:
        matching_houses.append([edge.house for edge in matching.edges if (edge.well.x, edge.well.y) == (well.x, well.y)])

    for i in range(len(wells)):
        output.write(f"W{wells[i].idx + 1}({wells[i].x},{wells[i].y}) -> ")
        for j in range(len(matching_houses[i])):
            output.write(f"H{matching_houses[i][j].idx + 1}({matching_houses[i][j].x},{matching_houses[i][j].y})")
            if j < len(matching_houses[i]) - 1:
                output.write(",")
        output.write("\n")

    total_cost = -sum([edge.weight for edge in matching.edges])
    output.write(f"Total Cost: {total_cost}\n")

    output.close()
