import json
import os

def split_json_file(input_file, output_folder, output_prefix, objects_per_file):
    # create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    with open(input_file, 'r') as file:
        data = json.load(file)

    # calculate the number of output files needed
    total_objects = len(data)
    num_files = (total_objects // objects_per_file) + (1 if total_objects % objects_per_file != 0 else 0)

    for i in range(num_files):
        start_index = i * objects_per_file
        end_index = start_index + objects_per_file
        split_data = data[start_index:end_index]

        # write each split data into a new JSON file in the output folder
        output_file = os.path.join(output_folder, f"{output_prefix}_{i+1}.json")
        with open(output_file, 'w') as output:
            json.dump(split_data, output, indent=4)

        print(f"Created file: {output_file} with {len(split_data)} objects.")

input_file = 'mnml/mnml_still_missing.json'
output_folder = 'mnml/split_still_missing'  # folder to store the split files
output_prefix = 'mnml_split_still_missing'
objects_per_file = 2

split_json_file(input_file, output_folder, output_prefix, objects_per_file)
