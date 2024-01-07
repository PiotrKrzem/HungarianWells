import timeit
import numpy as np

from src.hungarian import run_hungarian
from src.helpers.input_handler import generate_input
from src.helpers.output_handler import write_to_output
from src.helpers.plot import display_output, display_time_complexity
from src.helpers.arguments_parser import ApplicationMode, parse_arguments


def main():
    args = parse_arguments()
    selected_mode = ApplicationMode.from_str(args.mode)

    if args.n >= 5 and args.k >= 5:
        print('[WARNING] The runtime for n >= 5 and k >= 5 is expected to be up to an hour for complex cases.')
    elif args.n >= 4 and args.k >= 4:
        print('[WARNING] The runtime for n >= 4 and k >= 4 is expected to be up to two minutes for complex cases.')

    if selected_mode == ApplicationMode.GENERATE_INPUT:
        generate_input(args.n, args.k, args.input_file)
        print('[INFO] Input file generated.')

    elif selected_mode == ApplicationMode.GENERATE_AND_RUN:
        generate_input(args.n, args.k, args.input_file)
        print('[INFO] Input file generated.')
        print('[INFO] Starting Hungarian Algorithm...')
        graph, matching = run_hungarian(args.input_file)
        write_to_output(matching, args.output_file)
        print('[INFO] Output saved.')
        display_output(graph.n, graph.k, args.output_file)

    elif selected_mode == ApplicationMode.READ_INPUT:
        print('[INFO] Starting Hungarian Algorithm...')
        graph, matching = run_hungarian(args.input_file)
        write_to_output(matching, args.output_file)
        print('[INFO] Output saved.')
        display_output(graph.n, graph.k, args.output_file)

    elif selected_mode == ApplicationMode.BENCHMARK:
        measurements = np.zeros((args.n, args.k))
        print('[INFO] Starting Hungarian Algorithm...')
        for n in range(1, args.n + 1):
            for k in range(1, args.k + 1):
                generate_input(n, k, args.input_file)
                print(f'[INFO] Input generated - {n} wells, {k} houses per well')
                print('[INFO] Measuring Hungarian Algorithm execution time...')
                measurement = timeit.timeit(
                    lambda: run_hungarian(args.input_file),
                    number=1
                )
                measurements[n-1, k-1] = measurement * 100
                print(f'Time measured: {round(measurement * 100, 2)} seconds.')

        display_time_complexity(args.n, args.k, measurements, 1/2000, logarithmic=False)
        display_time_complexity(args.n, args.k, measurements, 1/2000, logarithmic=True)

if __name__ == "__main__":
    main()