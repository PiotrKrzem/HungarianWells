#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <iostream>

struct Coordinates {
	float x, y;
};

int main(int argc, char* argv[]) {
	// Check if the number of arguments is correct
	if (argc != 3) {
		std::cerr << "Usage: " << argv[0] << " input_file output_file" << std::endl;
		return EXIT_FAILURE;
	}

	const char* input_file = argv[1];
	const char* output_file = argv[2];
	// const char* input_file = "input.txt";
	// const char* output_file = "output.txt";

	std::ifstream input(input_file);

	if (!input.is_open()) {
		std::cerr << "Error: Unable to open input file " << input_file << std::endl;
		return EXIT_FAILURE;
	}

	size_t num_wells, num_houses_per_well, num_houses;
	input >> num_wells >> num_houses_per_well;
	num_houses = num_wells * num_houses_per_well;

	std::vector<Coordinates> wells;
	wells.reserve(num_wells);
	std::vector<Coordinates> houses;
	houses.reserve(num_houses);

	// Read well coordinates
	for (size_t i = 0; i < num_wells; ++i) {
		Coordinates well;
		char comma;
		input >> well.x >> comma >> well.y;
		wells.push_back(well);
	}

	// Read house coordinates
	for (size_t i = 0; i < num_houses; ++i) {
		Coordinates house;
		char comma;
		input >> house.x >> comma >> house.y;
		houses.push_back(house);
	}

	input.close();

	std::ofstream output(output_file);

	if (!output.is_open()) {
		std::cerr << "Error: Unable to open output file " << output_file << std::endl;
		return EXIT_FAILURE;
	}

	for (size_t i = 0; i < num_wells; ++i) {
		output << "W" << i + 1 << "(" << wells[i].x << "," << wells[i].y << ") -> ";
		for (size_t j = 0; j < num_houses_per_well; ++j) {
			output << "H" << i * num_houses_per_well + j + 1 << "(" << houses[i*num_houses_per_well + j].x << "," << houses[i * num_houses_per_well + j].y << ")";
			if (j < num_houses_per_well - 1) {
				output << ",";
			}
		}
		output << std::endl;
	}
	float total_cost = 12345.6789;
	output << "Total Cost: " << total_cost << std::endl;

	return EXIT_SUCCESS;
}