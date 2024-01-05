
import numpy as np

from src.models.graph import Graph

def generate_input(N, K, input_file, save_to_file = True) -> Graph:
    '''
    Method generates sample input for N wells and K*N houses

    Parameters:
    N - number of wells
    K - number of houses
    input_file - name of the input file in which input is to be stored
    '''
    x_well = np.random.uniform(low = 0.0, high = 10.0, size=(N))
    y_well = np.random.uniform(low = 0.0, high = 10.0, size=(N))

    x_house = np.random.uniform(low = 0.0, high = 10.0, size=K*N)
    y_house = np.random.uniform(low = 0.0, high = 10.0, size=K*N)

    if save_to_file:
        with open(input_file, "w") as file:
            file.write(f"{N} {K}\n")
            for i in range(N):
                file.write(f"{round(x_well[i], 2)},{round(y_well[i], 2)}\n")
            for i in range(K*N):
                file.write(f"{round(x_house[i], 2)},{round(y_house[i], 2)}\n")

    wells = np.column_stack((x_well, y_well))
    houses = np.column_stack((x_house, y_house))

    return Graph(N, K, wells, houses)

def read_input(input_file) -> Graph:
    '''
    Method reads input file and returns graph data

    Parameters:
    N - number of wells
    K - number of houses
    input_file - name of the input file in which input is to be stored
    '''
    with open(input_file, "r") as file:
        sizes = file.readline().split(" ")

        if len(sizes) != 2:
            raise ValueError("Incorrect parameters specify. \
                             Please give in the first line of the input file \
                             the number of wells ans houses per each well \
                             separated by whitespace -> e.g. 2 2")

        n = int(sizes[0])
        k = int(sizes[1])

        wells_coordinates = []
        houses_coordinates = []

        idx = 0
        for line in file:
            coordinates_str = line.split(",")
            node_coordinates = [float(coordinates_str[0]), float(coordinates_str[1])]
            if idx < n:
                wells_coordinates.append(node_coordinates)
            else:
                houses_coordinates.append(node_coordinates) 
            idx += 1

        return Graph(n, k, np.array(wells_coordinates), np.array(houses_coordinates))
