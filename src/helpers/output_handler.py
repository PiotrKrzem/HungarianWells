from src.models.matching import Matching
from src.models.graph import InitialGraph


def write_to_output(graph: InitialGraph, matching: Matching, output_file: str):
    '''
    Method writes results of matching to indicated output file.

    Parameters:
    ----------
    matching : Matching
        resulting matching
    output_file : str
        name of the file to which the results are to be stores
    '''
    try:
        output = open(output_file, 'w')
    except IOError:
        raise FileNotFoundError(f"Error: Unable to open output file {output_file}")

    total_cost = 0
    for well in range(graph.n):
        well_x, well_y = graph.wells_coordinates[well]

        well_duplicate_start = well * graph.k
        well_duplicate_end = well_duplicate_start + graph.k
        
        
        output.write(f"W{well + 1}({well_x},{well_y}) -> ")

        for well_duplicate in range(well_duplicate_start, well_duplicate_end):
            house =  matching.matching_house[well_duplicate]
            house_x, house_y = graph.houses_coordinates[house]
            output.write(f"H{house + 1}({house_x},{house_y})")

            total_cost += InitialGraph.distance(well_x, well_y, house_x, house_y)

            if well_duplicate < well_duplicate_end - 1:
                output.write(",")

        output.write("\n")


    total_cost = -total_cost
    output.write(f"Total Cost: {total_cost / 100}\n")

    output.close()
