import timeit
import subprocess
import numpy as np

from src.helpers.input_handler import generate_input, read_input
from src.helpers.plot import display_output, display_time_complexity
from src.helpers.arguments_parser import ApplicationMode, parse_arguments

def execute_hungarian(N, K, input_file, output_file):
    try:
        subprocess.run(f"Hungarian_64.exe {input_file} {output_file}")
        return
    except Exception as e:
        print(f"{e}")

    try:
        subprocess.run(f"Hungarian_32.exe {input_file} {output_file}")
        return
    except Exception as e:
        print(f"{e}")

    print("Both Hungarian executables failed.")


def main():
    args = parse_arguments()
    selected_mode = ApplicationMode.from_str(args.mode)

    if selected_mode == ApplicationMode.GENERATE_INPUT:
        graph = generate_input(args.n, args.k, args.input_file)
        execute_hungarian(args.n, args.k, args.input_file, args.output_file)
        display_output(args.n, args.k, args.output_file)

    elif selected_mode == ApplicationMode.READ_INPUT:
        graph = read_input(args.input_file)
        execute_hungarian(args.n, args.k, args.input_file, args.output_file)
        display_output(args.n, args.k, args.output_file)

    elif selected_mode == ApplicationMode.BENCHMARK:
        measurements = np.zeros((args.n, args.k))
        for n in range(1, args.n + 1):
            for k in range(1, args.k + 1):
                graph = generate_input(args.n, args.k, args.input_file)
                measurement = timeit.timeit(
                    lambda: execute_hungarian(args.n, args.k, args.input_file, args.output_file),
                    number=1
                )
                measurements[n-1, k-1] = measurement * 100
        
        print(measurements)
        display_time_complexity(args.n, args.k, measurements, logarithmic=True)

if __name__ == "__main__":
    main()