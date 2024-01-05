import argparse
from enum import Enum, auto

class ApplicationMode(str, Enum):
    GENERATE_INPUT = auto()
    READ_INPUT = auto()
    BENCHMARK = auto()

    @staticmethod
    def from_str(label):
        label_map = {
            "GENERATE": ApplicationMode.GENERATE_INPUT,
            "READ": ApplicationMode.READ_INPUT,
            "BENCHMARK": ApplicationMode.BENCHMARK,
        }
        if label in label_map:
            return label_map[label]
        else:
            raise NotImplementedError(f"{label} not implemented")

def parse_arguments():
    '''
    Method parse input arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", default="READ", type=str)
    parser.add_argument("-n", default=5, type=int)
    parser.add_argument("-k", default=5, type=int)
    parser.add_argument("-i", "--input_file", default="input.txt", type=str)
    parser.add_argument("-o", "--output_file", default="output.txt", type=str)

    return parser.parse_args()