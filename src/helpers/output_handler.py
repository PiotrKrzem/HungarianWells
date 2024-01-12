from src.models.matching import Matching

def write_to_output(matching: Matching, output_file: str):
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
    
    matching_wells_coords = list(set([(edge.well.x, edge.well.y) for edge in matching.edges]))
    matching_wells = []
    matching_houses = []

    for edge in matching.edges:
        if (edge.well.x, edge.well.y) in matching_wells_coords:
            matching_wells.append(edge.well)
            matching_wells_coords.remove((edge.well.x, edge.well.y))

    for well in matching_wells:
        matching_houses.append([edge.house for edge in matching.edges if (edge.well.x, edge.well.y) == (well.x, well.y)])

    well_idx, house_idx = 1, 1
    for i in range(len(matching_wells)):
        output.write(f"W{well_idx}({matching_wells[i].x},{matching_wells[i].y}) -> ")
        well_idx += 1
        for j in range(len(matching_houses[i])):
            output.write(f"H{house_idx}({matching_houses[i][j].x},{matching_houses[i][j].y})")
            house_idx += 1
            if j < len(matching_houses[i]) - 1:
                output.write(",")
        output.write("\n")

    total_cost = -sum([edge.weight for edge in matching.edges])
    output.write(f"Total Cost: {total_cost / 100}\n")

    output.close()
