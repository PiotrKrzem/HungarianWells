import argparse
from enum import Enum, auto

class ApplicationMode(str, Enum):
    GENERATE_INPUT = "GENERATE_INPUT"
    GENERATE_AND_RUN = "GENERATE_AND_RUN"
    READ_INPUT = "READ_INPUT"
    BENCHMARK = "BENCHMARK"

    @staticmethod
    def from_str(label):
        label_map = {
            ApplicationMode.GENERATE_INPUT.value: ApplicationMode.GENERATE_INPUT,
            ApplicationMode.GENERATE_AND_RUN.value: ApplicationMode.GENERATE_AND_RUN,
            ApplicationMode.READ_INPUT.value: ApplicationMode.READ_INPUT,
            ApplicationMode.BENCHMARK.value: ApplicationMode.BENCHMARK,
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
    parser.add_argument("-m", "--mode", default=ApplicationMode.GENERATE_AND_RUN.value, type=str)
    parser.add_argument("-n", default=5, type=int)
    parser.add_argument("-k", default=5, type=int)
    parser.add_argument("-i", "--input_file", default="input.txt", type=str)
    parser.add_argument("-o", "--output_file", default="output.txt", type=str)

    return parser.parse_args()