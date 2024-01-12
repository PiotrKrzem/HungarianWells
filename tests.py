import os
import timeit
import numpy as np

from src.helpers.input_handler import generate_input
from src.helpers.output_handler import write_to_output
from src.helpers.plot import save_output, save_time_complexity
from src.helpers.plot import display_output, display_time_complexity

RUN_SAFE = False
DISPLAY_OUTPUT_INSTEAD_OF_SAVE = False
DISPLAY_COMPLEXITY_INSTEAD_OF_SAVE = False

MAX_N, MAX_K = 5, 5
REGENERATE = [
    # (2,2)
]
RUN_ONLY = [
    # (5,5)
]

def test_hungarian(input_file):
    if RUN_SAFE:
        from src.hungarian import test_hungarian as _test_hungarian
        return _test_hungarian(input_file)
    else:
        from src.hungarian import run_hungarian
        return run_hungarian(input_file)
    
def process_output(n, k, output_file, output_plot):
    if DISPLAY_OUTPUT_INSTEAD_OF_SAVE:
        return display_output(n, k, output_file)
    else:
        return save_output(n, k, output_file, output_plot)

def process_time_complexity(n, k, measurements_grid, output_plot, C1 = 1/4000, C2 = 1, logarithmic = False):
    if DISPLAY_COMPLEXITY_INSTEAD_OF_SAVE:
        return display_time_complexity(n, k, measurements_grid, C1, C2, logarithmic)
    else:
        return save_time_complexity(n, k, measurements_grid, output_plot, C1, C2, logarithmic)

def main():
    
    pictures = "./Pictures/"
    tests = "./Tests/"

    if not os.path.exists(pictures):
        os.mkdir(pictures)

    if not os.path.exists(tests):
        os.mkdir(tests)

    # Custom input for debugging
    """
    input_file = "./Tests/input_custom.txt"
    output_file = "./Tests/output_custom.txt"
    print(f"Custom")

    graph, matching = test_hungarian(input_file)
    write_to_output(matching, output_file)
    process_output(graph.n, graph.k, output_file, f"{pictures}custom.png")
    """

    # example from inintial documentation
    """
    n, k = 2, 2
    input_file = f"./Tests/input_example.txt"
    output_file = f"./Tests/output_example.txt"
    print(f'(Example) N: {n}, K: {k}')

    with open(input_file, 'w') as f:
        f.writelines([
            "2 2\n"
            "2.5,1.5\n"
            "0.8,1.5\n"
            "1,1\n"
            "2,1\n"
            "2,2\n"
            "1,2"
        ])
    graph, matching = test_hungarian(input_file)
    write_to_output(matching, output_file)
    process_output(graph.n, graph.k, output_file, f"{pictures}n_{n}_k_{k}.png")
    """
    

    # TESTS
    # 5x5
    for n in range(1, MAX_N + 1):
        for k in range(1, MAX_K + 1):
            if (len(RUN_ONLY) and RUN_ONLY.count((n, k))) or not len(RUN_ONLY):
                input_file = f"./Tests/input_test_{n}_{k}.txt"
                output_file = f"./Tests/output_test_{n}_{k}.txt"
                print(f'N: {n}, K: {k}')
                
                if REGENERATE.count((n, k)) or not os.path.exists(input_file):
                    generate_input(n, k, input_file)

                graph, matching = test_hungarian(input_file)
                write_to_output(matching, output_file)
                process_output(graph.n, graph.k, output_file, f"{pictures}n_{n}_k_{k}.png")


    # while True:
    #     try:
    #         n, k = 5, 5
    #         input_file = f"./Tests/input_test_{n}_{k}.txt"
    #         output_file = f"./Tests/output_test_{n}_{k}.txt"
    #         print(f'N: {n}, K: {k}')
            
    #         if REGENERATE.count((n, k)) or not os.path.exists(input_file):
    #             generate_input(n, k, input_file)

    #         graph, matching = test_hungarian(input_file)
    #         write_to_output(matching, output_file)
    #         process_output(graph.n, graph.k, output_file, f"{pictures}n_{n}_k_{k}.png")
    #         break
    #     except InterruptedError as e:
    #         print(f"{str(e)}")

    # BENCHMARKING
    print(f'Benchmark N: {MAX_N}, K: {MAX_K}')
    measurements = np.zeros((MAX_N, MAX_K))
    for n in range(1, MAX_N + 1):
        for k in range(1, MAX_K + 1):
            print(f'Benchmark -> N: {n}, K: {k}')
            input_file = f"./Tests/input_test_{n}_{k}.txt"
            output_file = f"./Tests/output_test_benchmark.txt"
            measurement = timeit.timeit(
                lambda: test_hungarian(input_file),
                number=1
            )
            measurements[n-1, k-1] = measurement * 100
    measurements[MAX_N-1, MAX_K-1] = measurements.max() * n * k

    process_time_complexity(n, k, measurements, f"{pictures}standard_benchmark.png", logarithmic=False)
    process_time_complexity(n, k, measurements, f"{pictures}log_benchmark.png", logarithmic=True)

if __name__ == "__main__":
    main()
