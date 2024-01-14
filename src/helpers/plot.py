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

def create_time_complexity_plot(n, k, measurements_grid, logarithmic = False, smoothed = False):
    if smoothed:
        try:
            from scipy.signal import convolve2d
            kernel = np.ones((3, 3))
            measurements_grid = convolve2d(measurements_grid, kernel, mode='same', boundary='symm')
        except:
            print("[WARN] Smoothing requires scipy module. No smoothing applied.")

    # Make data
    N = np.arange(1, n + 1, 1)
    K = np.arange(1, k + 1, 1)
    N, K = np.meshgrid(N, K)

    T = np.multiply(N, K)
    T = np.power(T, 3)

    A = np.max(measurements_grid[3*n//4:,3*n//4:] / T[3*n//4:,3*n//4:])
    B = np.max(measurements_grid - A * T)

    T = A * T + B

    fig, axs = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={"projection": "3d"})

    axs[0].set_xlabel('N')
    axs[0].set_ylabel('K')
    axs[0].set_zlabel('Time')

    axs[1].set_xlabel('N')
    axs[1].set_ylabel('K')
    axs[1].set_zlabel('Time')

    axs[2].set_xlabel('N')
    axs[2].set_ylabel('K')
    axs[2].set_zlabel('Time')

    limit_proxy = plt.Line2D([0], [0], linestyle="none", c='red', marker='o', markersize=10, markerfacecolor='red', alpha=0.7)
    measurements_proxy = plt.Line2D([0], [0], linestyle="none", c='green', marker='o', markersize=10, markerfacecolor='green', alpha=0.7)
    axs[2].legend([limit_proxy, measurements_proxy], [f'O((nk)^3)', f'Measurements'])

    axs[0].set_title(f'O((nk)^3)')
    axs[1].set_title(f'Measurements')
    axs[2].set_title(f'Comparison')

    if not logarithmic:
        zlim_min = 0
        zlim_max = max(T.max(), measurements_grid.max())

        axs[0].set_zlim([zlim_min, zlim_max])
        axs[1].set_zlim([zlim_min, zlim_max])
        axs[2].set_zlim([zlim_min, zlim_max])

        axs[0].set_zlabel('Time (s)')
        axs[1].set_zlabel('Time (s)')
        axs[2].set_zlabel('Time (s)')

        limit_surface = axs[0].plot_surface(N, K, T, vmin=0, color='firebrick', shade=True)
        measurements_surface = axs[1].plot_surface(N, K, measurements_grid, vmin=0, color = 'green', shade=True)

        limit_surface_compare = axs[2].plot_surface(N, K, T, vmin=0, color = 'firebrick', shade=True)
        measurements_surface_compare = axs[2].plot_surface(N, K, measurements_grid, vmin=0, color = 'green', shade=True)

    else:
        zlim_min = min(np.emath.logn(4, measurements_grid.min()), np.emath.logn(4, T.min()))
        zlim_max = max(np.emath.logn(4, measurements_grid.max()), np.emath.logn(4, T.max()))

        axs[0].set_zlim([zlim_min, zlim_max])
        axs[1].set_zlim([zlim_min, zlim_max])
        axs[2].set_zlim([zlim_min, zlim_max])

        axs[0].set_zlabel('Time, logarithmic (s)')
        axs[1].set_zlabel('Time, logarithmic (s)')
        axs[2].set_zlabel('Time (s)')


        limit_surface = axs[0].plot_surface(N, K, np.emath.logn(4, T), vmin=0, color='firebrick', shade=True)
        measurements_surface = axs[1].plot_surface(N, K, np.emath.logn(4, measurements_grid), color = 'green', shade=True)

        limit_surface_compare = axs[2].plot_surface(N, K, np.emath.logn(4, T), vmin=0, color='firebrick', shade=True)
        measurements_surface_compare = axs[2].plot_surface(N, K, np.emath.logn(4, measurements_grid), color = 'green', shade=True)

        # axs[0].zaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
        # axs[0].zaxis.set_major_locator(mticker.MaxNLocator(integer=True))

        # axs[1].zaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
        # axs[1].zaxis.set_major_locator(mticker.MaxNLocator(integer=True))

        # axs[2].zaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
        # axs[2].zaxis.set_major_locator(mticker.MaxNLocator(integer=True))

def create_input_plot(input_file):

    wells = {}
    houses = {}
    
    with open(input_file, "r") as file:
        input = file.readlines()
        n, k = input[0].split()
        n, k = int(n), int(k)

        for i,line in enumerate(input[1:n+1]):
            well_x, well_y = line.split(',')
            wells[f"W{i+1}"] = (float(well_x), float(well_y[:-1]))

        for i, line in enumerate(input[n+1:n+k*n + 1]):
            house_x, house_y = line.split(',')
            houses[f"H{i+1}"] = (float(house_x), float(house_y))

    # Plotting
    fig, axis = plt.subplots(figsize=(12, 6))
    fig.suptitle("Input Visualization")

    # Left subplot
    axis.set_title("Input")
    axis.set_xlabel("X")
    axis.set_ylabel("Y")

    for well_name, (well_x, well_y) in wells.items():
        axis.scatter(well_x, well_y, color='blue', s = 100)
        axis.text(well_x, well_y, well_name, ha='right', va='bottom')

    for house_name, (house_x, house_y) in houses.items():
        axis.scatter(house_x, house_y, color='red', s = 100)
        axis.text(house_x, house_y, house_name, ha='right', va='bottom')

        # Connect each house to every well with a line and label the distance
        for _, (well_x, well_y) in wells.items():
            distance = ((house_x - well_x)**2 + (house_y - well_y)**2)**0.5
            axis.plot([house_x, well_x], [house_y, well_y], linestyle='--', color='black')
            axis.text((house_x + well_x) / 2, (house_y + well_y) / 2, f'{distance:.2f}', ha='center', va='center')

    plt.tight_layout()

def create_output_plot(n, k, output_file):
    pattern_string = r'(\w+)\(([\d.]+),([\d.]+)\) -> ' + ','.join([r'(\w+)\(([\d.]+),([\d.]+)\)'] * k)
    pattern = re.compile(pattern_string)

    wells = {}
    houses = {}
    house_well_map = []
    
    with open(output_file, "r") as file:
        output = file.readlines()

        total_cost = output[len(output)-1]
        for line in output[:len(output)-1]:
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

def display_time_complexity(n, k, measurements_grid, logarithmic = False, smoothed = False):
    create_time_complexity_plot(n, k, measurements_grid, logarithmic, smoothed)
    plt.show()

def save_time_complexity(n, k, measurements_grid, output_plot, logarithmic, smoothed = False):
    create_time_complexity_plot(n, k, measurements_grid, logarithmic, smoothed)
    plt.savefig(output_plot, format='png')
    plt.close()

def save_output(n, k, output_file, output_plot):
    create_output_plot(n, k, output_file)
    plt.savefig(output_plot, format='png')
    plt.close()

def display_output(n, k, output_file):
    create_output_plot(n, k, output_file)
    plt.show()
