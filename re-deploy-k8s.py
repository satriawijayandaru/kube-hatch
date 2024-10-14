import os
import yaml
from pathlib import Path

# Directory to scan for YAML files
directory = Path(".")

# Create a new folder to store the modified files
output_folder = directory / "modified_files"
output_folder.mkdir(exist_ok=True)

# Function to recursively remove specified keys from a nested dictionary
def remove_keys(data, keys_to_remove):
    if isinstance(data, dict):
        # Remove the specified keys if they exist
        for key in keys_to_remove:
            data.pop(key, None)
        # Recursively call the function on nested dictionaries
        for key, value in data.items():
            data[key] = remove_keys(value, keys_to_remove)
    elif isinstance(data, list):
        # If the data is a list, apply the function to each item
        data = [remove_keys(item, keys_to_remove) for item in data]
    return data

# Get all .yaml and .yml files in the directory
yaml_files = list(directory.glob("*.yml")) + list(directory.glob("*.yaml"))

# Process each file
for file_path in yaml_files:
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    # Remove the 'resourceVersion' and 'uid' keys recursively
    if data:
        data = remove_keys(data, ["resourceVersion", "uid"])

    # Save the updated file to the new folder
    output_file_path = output_folder / file_path.name
    with open(output_file_path, "w") as output_file:
        yaml.dump(data, output_file, default_flow_style=False)

    print(f"Processed: {file_path} -> {output_file_path}")

print(f"All YAML files have been processed and saved to: {output_folder}")
