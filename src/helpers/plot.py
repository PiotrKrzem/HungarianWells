import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from matplotlib.colors import ListedColormap

def exponential_cmap(base_cmap=None, colors_count = 256):
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, colors_count))

    # Normalize the RGB values to be in the [0, 1] range
    color_list[:, :3] = np.power(color_list[:, :3], 4)
    color_list[:, :3] /= color_list[:, :3].max()

    custom_cmap = ListedColormap(color_list)

    return custom_cmap

def log_tick_formatter(val, pos=None):
    return f"$10^{{{int(val)}}}$"

def display_time_complexity(n, k, measurements_grid, C = 1/100, logarithmic = False):
    # Make data
    N = np.arange(1, n + 1, 1) + 10e-5
    K = np.arange(1, k + 1, 1) + 10e-5
    N, K = np.meshgrid(N, K)

    T = np.multiply(N, K)
    T = C * np.power(T, 4)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    fig.suptitle('Time Complexity')

    ax.set_xlabel('N')
    ax.set_ylabel('K')
    ax.set_zlabel('Time')

    limit_proxy = plt.Line2D([0], [0], linestyle="none", c='red', marker='o', markersize=10, markerfacecolor='red', alpha=0.7)
    measurements_proxy = plt.Line2D([0], [0], linestyle="none", c='green', marker='o', markersize=10, markerfacecolor='green', alpha=0.7)
    ax.legend([limit_proxy, measurements_proxy], [f'O({C}(nk)^4)', 'Measurements'])

    colors_count = (n+1)*(k+1)
    colors_count = n*k

    if not logarithmic:
        limit_surface = ax.plot_surface(N, K, T, vmin=-1, cmap=exponential_cmap('Reds', colors_count))
        measurements_surface = ax.plot_surface(N, K, measurements_grid, vmin=-1, cmap=exponential_cmap('Greens', colors_count))
        
        ax.set_zlabel('Time (s)')
    else:
        limit_surface = ax.plot_surface(N, K, np.emath.logn(4, T), vmin=-1, cmap=exponential_cmap('Reds', colors_count))
        measurements_surface = ax.plot_surface(N, K, np.emath.logn(4, measurements_grid), vmin=-1, cmap=exponential_cmap('Greens', colors_count))

        ax.zaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
        ax.zaxis.set_major_locator(mticker.MaxNLocator(integer=True))

        ax.set_zlabel('Time, logarithmic (s)')

    plt.show()

def display_output(n, k, output_file):
    pattern_string = r'(\w+)\(([\d.]+),([\d.]+)\) -> ' + ','.join([r'(\w+)\(([\d.]+),([\d.]+)\)'] * k)
    pattern = re.compile(pattern_string)

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


if __name__ == "__main__":
    n = 5
    k = 5
    display_time_complexity(n, k, (np.arange(1, n*k + 1, 1) + 10e-5).reshape((n,k)), logarithmic=False)
    display_time_complexity(n, k, (np.arange(1, n*k + 1, 1) + 10e-5).reshape((n,k)), logarithmic=True)
