import argparse
from enum import Enum

class ApplicationMode(str, Enum):
    GENERATE_INPUT = "GENERATE"
    READ_INPUT = "READ"

    @staticmethod
    def from_str(label):
        if label == "GENERATE":
            return ApplicationMode.GENERATE_INPUT
        elif label == "READ":
            return ApplicationMode.READ_INPUT
        else:
            raise NotImplementedError

def parse_arguments():
    '''
    Method parse input arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", default="READ", type=str)
    parser.add_argument("-n", default=1, type=int)
    parser.add_argument("-k", default=1, type=int)
    parser.add_argument("-i", "--input_file", default="input.txt", type=str)
    parser.add_argument("-o", "--output_file", default="output.txt", type=str)

    return parser.parse_args()