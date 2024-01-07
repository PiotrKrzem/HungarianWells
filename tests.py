import os
import timeit
import numpy as np

from src.helpers.input_handler import generate_input
from src.helpers.output_handler import write_to_output
from src.helpers.plot import save_output, save_time_complexity

EXE = False

def test_hungarian(n, k, input_file, output_file):
    if EXE:
        import subprocess
        class Tmp:
            def __init__(self, n, k) -> None:
                self.n = n
                self.k = k

        subprocess.run(f"Hungarian_64.exe {input_file} {output_file}")
        return Tmp(n, k), None
    else:
        from src.hungarian import run_hungarian
        return run_hungarian(input_file)

def main():
    input_file = "./Tests/input_test_1.txt"
    output_file = "./Tests/output_test_1.txt"
    pictures = "./Pictures/"
    tests = "./Tests/"

    if not os.path.exists(pictures):
        os.mkdir(pictures)

    if not os.path.exists(tests):
        os.mkdir(tests)

    # 2x1
    n, k = 2, 1
    # generate_input(n, k, input_file)
    graph, matching = test_hungarian(n, k, input_file, output_file)
    write_to_output(matching, output_file)
    save_output(graph.n, graph.k, output_file, f"{pictures}n_{n}_k_{k}.png")

    # Example from inintial documentation
    with open("input.txt", 'w') as f:
        f.writelines([
            "2 2\n"
            "2.5,1.5\n"
            "0.8,1.5\n"
            "1,1\n"
            "2,1\n"
            "2,2\n"
            "1,2"
        ])
    n, k = 2, 2
    graph, matching = test_hungarian(n, k, input_file, output_file)
    write_to_output(matching, output_file)
    save_output(graph.n, graph.k, output_file, f"{pictures}n_{n}_k_{k}.png")

    input_file = "./Tests/input_test_2.txt"
    output_file = "./Tests/output_test_2.txt"

    # 3x2
    n, k = 3, 2
    print(f'N: {n}, K: {k}')
    # generate_input(n, k, input_file)
    graph, matching = test_hungarian(n, k, input_file, output_file)
    write_to_output(matching, output_file)
    save_output(n, k, output_file, f"{pictures}n_{n}_k_{k}.png")

    input_file = "./Tests/input_test_3.txt"
    output_file = "./Tests/output_test_3.txt"

    # 2x4
    n, k = 2, 4
    print(f'N: {n}, K: {k}')
    # generate_input(n, k, input_file)
    graph, matching = test_hungarian(n, k, input_file, output_file)
    write_to_output(matching, output_file)
    save_output(graph.n, graph.k, output_file, f"{pictures}n_{n}_k_{k}.png")

    input_file = "./Tests/input_test_4.txt"
    output_file = "./Tests/output_test_4.txt"

    # 4x3
    n, k = 4, 3
    print(f'N: {n}, K: {k}')
    # generate_input(n, k, input_file)
    graph, matching = test_hungarian(n, k, input_file, output_file)
    write_to_output(matching, output_file)
    save_output(graph.n, graph.k, output_file, f"{pictures}n_{n}_k_{k}.png")
    # return

    input_file = "./Tests/input_test_5.txt"
    output_file = "./Tests/output_test_5.txt"

    # 4x4
    n, k = 4, 4
    print(f'N: {n}, K: {k}')
    # generate_input(n, k, input_file)
    graph, matching = test_hungarian(n, k, input_file, output_file)
    write_to_output(matching, output_file)
    save_output(graph.n, graph.k, output_file, f"{pictures}n_{n}_k_{k}.png")
    # return

    input_file = "./Tests/input_test_benchmark.txt"
    output_file = "./Tests/output_test_benchmark.txt"

    # benchmarking
    n, k = 4, 4 
    print(f'N: {n}, K: {k}')
    measurements = np.zeros((n, k))
    for n in range(1, n + 1):
        for k in range(1, k + 1):
            print(f'Benchmark -> N: {n}, K: {k}')
            generate_input(n, k, input_file)
            measurement = timeit.timeit(
                lambda: test_hungarian(n, k, input_file, output_file),
                number=1
            )
            measurements[n-1, k-1] = measurement * 100

    save_time_complexity(n, k, measurements, f"{pictures}standard_benchmark.png", 1/2000, logarithmic=False)
    save_time_complexity(n, k, measurements, f"{pictures}log_benchmark.png", 1/2000, logarithmic=True)

if __name__ == "__main__":
    main()
