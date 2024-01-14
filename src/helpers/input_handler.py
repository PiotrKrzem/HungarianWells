
import numpy as np
from typing import Tuple

from src.models.graph import Graph
from src.models.graph import InitialGraph

def generate_input(N: int, K: int, input_file: str) -> None:
    '''
    Method generates sample input for N wells and K*N houses.

    Parameters:
    ----------
    N : int
        number of wells
    K : int
        number of houses
    input_file : str
        name of the input file in which input is to be stored
    '''
    x_well = np.random.rand(N) * 10
    y_well = np.random.rand(N) * 10

    x_house = np.random.rand(K*N) * 10
    y_house = np.random.rand(K*N) * 10

    with open(input_file, "w") as file:
        file.write(f"{N} {K}\n")
        for i in range(N):
            file.write(f"{round(x_well[i], 2)},{round(y_well[i], 2)}\n")
        for i in range(K*N):
            file.write(f"{round(x_house[i], 2)},{round(y_house[i], 2)}\n")


def read_input(input_file) -> InitialGraph:
    '''
    Method reads input file and returns graph data

    Parameters:
    ----------
    input_file : str
        name of the input file from which data is to be read
    '''
    with open(input_file, "r") as file:
        sizes = file.readline().split(' ')

        if len(sizes) != 2:
            raise ValueError("Incorrect parameters specify. \
                             Please give in the first line of the input file \
                             the number of wells ans houses per each well \
                             separated by whitespace -> e.g. 2 2")

        n = int(sizes[0])
        k = int(sizes[1])

        wells_coordinates = np.empty((n, 2))
        houses_coordinates = np.empty((n*k, 2))

        for i, line in enumerate(file):
            coordinates_str = line.split(",")
            x, y = round(float(coordinates_str[0]), 2), round(float(coordinates_str[1]), 2)
            if i < n:
                wells_coordinates[i, :] = x, y 
            else:
                houses_coordinates[i - n, :] = x, y  

        return InitialGraph(n, k, wells_coordinates, houses_coordinates)
