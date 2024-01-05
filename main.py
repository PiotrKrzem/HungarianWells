import timeit
import numpy as np

from src.hungarian import run_hungarian
from src.helpers.input_handler import generate_input, read_input
from src.helpers.plot import display_output, display_time_complexity
from src.helpers.arguments_parser import ApplicationMode, parse_arguments


def main():
    args = parse_arguments()
    selected_mode = ApplicationMode.from_str(args.mode)

    # selected_mode = ApplicationMode.GENERATE_AND_RUN

    if selected_mode == ApplicationMode.GENERATE_INPUT:
        generate_input(args.n, args.k, args.input_file)

    elif selected_mode == ApplicationMode.GENERATE_AND_RUN:
        generate_input(args.n, args.k, args.input_file)
        graph, matching = run_hungarian(args.input_file)
        display_output(graph.n, graph.k, args.output_file)

    elif selected_mode == ApplicationMode.READ_INPUT:
        graph, matching = run_hungarian(args.input_file)
        display_output(graph.n, graph.k, args.output_file)

    elif selected_mode == ApplicationMode.BENCHMARK:
        measurements = np.zeros((args.n, args.k))
        for n in range(1, args.n + 1):
            for k in range(1, args.k + 1):
                generate_input(args.n, args.k, args.input_file)
                measurement = timeit.timeit(
                    lambda: run_hungarian(args.input_file),
                    number=1
                )
                measurements[n-1, k-1] = measurement * 100

        display_time_complexity(args.n, args.k, measurements, 1/2000, logarithmic=False)
        display_time_complexity(args.n, args.k, measurements, 1/2000, logarithmic=True)

if __name__ == "__main__":
    main()