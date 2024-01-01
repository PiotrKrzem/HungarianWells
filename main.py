import re
import argparse
import subprocess
import numpy as np
import matplotlib.pyplot as plt


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", default=2, type=int)
    parser.add_argument("-k", default=2, type=int)
    parser.add_argument("-i", "--input_file", default="input.txt", type=str)
    parser.add_argument("-o", "--output_file", default="output.txt", type=str)

    return parser.parse_args()

def generate_input(N, K, input_file):
    x_well = np.random.uniform(low = 0.0, high = 10.0, size=(N))
    y_well = np.random.uniform(low = 0.0, high = 10.0, size=(N))

    x_house = np.random.uniform(low = 0.0, high = 10.0, size=K*N)
    y_house = np.random.uniform(low = 0.0, high = 10.0, size=K*N)

    with open(input_file, "w") as file:
        file.write(f"{N} {K}\n")
        for i in range(N):
            file.write(f"{round(x_well[i], 2)},{round(y_well[i], 2)}\n")
        for i in range(K*N):
            file.write(f"{round(x_house[i], 2)},{round(y_house[i], 2)}\n")

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

def generate_pattern(k):
    pattern_string = r'(\w+)\(([\d.]+),([\d.]+)\) -> ' + ','.join([r'(\w+)\(([\d.]+),([\d.]+)\)'] * k)
    pattern = re.compile(pattern_string)
    return pattern

def display_output(n, k, output_file):
    pattern = generate_pattern(k)

    wells = {}
    houses = {}
    house_well_map = []
    
    with open(output_file, "r") as file:
        output = file.readlines()

        total_cost = output[n]
        for line in output[:n]:
            for mapping in pattern.findall(line):
                well_name, well_x, well_y, *houses_values = mapping
                wells[well_name] = (float(well_x), float(well_y))

                for i in range(len(houses_values)//3):
                    house_name, house_x, house_y = houses_values[3*i:3*i+3]
                    houses[house_name] = (float(house_x), float(house_y))
                    house_well_map.append([house_name, well_name])

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(total_cost)

    # Left subplot
    axs[0].set_title("Input")
    axs[0].set_xlabel("X")
    axs[0].set_ylabel("Y")

    for well_name, (well_x, well_y) in wells.items():
        axs[0].scatter(well_x, well_y, color='blue')
        axs[0].text(well_x, well_y, well_name, ha='right', va='bottom')

    for house_name, (house_x, house_y) in houses.items():
        axs[0].scatter(house_x, house_y, color='red')
        axs[0].text(house_x, house_y, house_name, ha='right', va='bottom')

        # Connect each house to every well with a line and label the distance
        for _, (well_x, well_y) in wells.items():
            distance = ((house_x - well_x)**2 + (house_y - well_y)**2)**0.5
            axs[0].plot([house_x, well_x], [house_y, well_y], linestyle='--', color='black')
            axs[0].text((house_x + well_x) / 2, (house_y + well_y) / 2, f'{distance:.2f}', ha='center', va='center')

    # Right subplot
    axs[1].set_title("Output")
    axs[1].set_xlabel("X")
    axs[1].set_ylabel("Y")

    for well_name, (well_x, well_y) in wells.items():
        axs[1].scatter(well_x, well_y, color='blue')
        axs[1].text(well_x, well_y, well_name, ha='right', va='bottom')

    for house_name, (house_x, house_y) in houses.items():
        axs[1].scatter(house_x, house_y, color='red')
        axs[1].text(house_x, house_y, house_name, ha='right', va='bottom')

        # Connect each house to its corresponding well with a line and label the distance
        for house_well_pair in house_well_map:
            if house_well_pair[0] == house_name:
                well_x, well_y = wells[house_well_pair[1]]
                distance = ((house_x - well_x)**2 + (house_y - well_y)**2)**0.5
                axs[1].plot([house_x, well_x], [house_y, well_y], linestyle='-', color='red')
                axs[1].text((house_x + well_x) / 2, (house_y + well_y) / 2, f'{distance:.2f}', ha='center', va='center')
                break

    plt.tight_layout()
    plt.show()

def main():
    args = parse_arguments()
    generate_input(args.n, args.k, args.input_file)
    execute_hungarian(args.n, args.k, args.input_file, args.output_file)
    display_output(args.n, args.k, args.output_file)

if __name__ == "__main__":
    main()