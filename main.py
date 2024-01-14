import timeit
import numpy as np

from src.hungryryan import run_hungryryan
from src.helpers.input_handler import generate_input
from src.helpers.output_handler import write_to_output
from src.helpers.plot import display_output, display_time_complexity
from src.helpers.arguments_parser import ApplicationMode, parse_arguments


def main():
    args = parse_arguments()
    selected_mode = ApplicationMode.from_str(args.mode)

    if selected_mode == ApplicationMode.GENERATE_INPUT:
        generate_input(args.n, args.k, args.input_file)
        print('[INFO] Input file generated.')

    elif selected_mode == ApplicationMode.GENERATE_AND_RUN:
        generate_input(args.n, args.k, args.input_file)
        print('[INFO] Input file generated.')
        print('[INFO] Starting Hungarian Algorithm...')
        graph, matching = run_hungryryan(args.input_file)
        print('[INFO] Finished. Saving output...')
        write_to_output(graph, matching, args.output_file)
        print('[INFO] Output saved. Rendering final image...')
        display_output(graph.n, graph.k, args.output_file)

    elif selected_mode == ApplicationMode.READ_INPUT:
        print('[INFO] Starting Hungarian Algorithm...')
        graph, matching = run_hungryryan(args.input_file)
        print('[INFO] Finished. Saving output...')
        write_to_output(graph, matching, args.output_file)
        print('[INFO] Output saved. Rendering final image...')
        display_output(graph.n, graph.k, args.output_file)

    elif selected_mode == ApplicationMode.BENCHMARK:
        measurements = np.zeros((args.n, args.k))
        print('[INFO] Starting Hungarian Algorithm Benchmarking...')
        for n in range(1, args.n + 1):
            for k in range(1, args.k + 1):
                input_file = f"./Tests/input_test_{n}_{k}.txt"
                output_file = f"./Tests/output_test_benchmark.txt"
                generate_input(n, k, input_file)
                print(f'[INFO] Input generated - {n} wells, {k} houses per well')
                print('[INFO] Measuring Hungarian Algorithm execution time...')
                measurement = timeit.timeit(
                    lambda: run_hungryryan(input_file),
                    number=1
                )
                measurements[n-1, k-1] = measurement
                print(f'Time measured: {round(measurement * 100, 2)} seconds.')
        print('[INFO] Benchmarking finished.  Rendering time complexity chart...')
        display_time_complexity(args.n, args.k, measurements, logarithmic=False)

if __name__ == "__main__":
    main()
