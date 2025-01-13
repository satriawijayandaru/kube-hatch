import os
import yaml
from pathlib import Path
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Transform Rancher YAML files for redeployment to another cluster.")
parser.add_argument(
    "--remove-annotations", action="store_true", help="Remove all annotations from YAML files."
)
parser.add_argument(
    "--keep-labels", action="store_true", help="Keep labels in the YAML files (default is to remove)."
)
args = parser.parse_args()

# Directory to scan for YAML files
directory = Path(".")
output_folder = directory / "transformed_files"
output_folder.mkdir(exist_ok=True)

def transform_yaml(data):
    if isinstance(data, dict):
        # Remove metadata fields that can cause conflicts
        metadata_fields_to_remove = [
            "resourceVersion", "uid", "creationTimestamp"
        ]
        if "metadata" in data:
            for field in metadata_fields_to_remove:
                data["metadata"].pop(field, None)

            # Optionally remove annotations
            if args.remove_annotations:
                data["metadata"].pop("annotations", None)

            # Remove labels unless explicitly kept
            if not args.keep_labels:
                data["metadata"].pop("labels", None)

        # Remove status sections
        data.pop("status", None)

        # Remove or reset nodeName
        if "spec" in data and isinstance(data["spec"], dict):
            data["spec"].pop("nodeName", None)

        # Recursively process nested dictionaries
        for key, value in data.items():
            data[key] = transform_yaml(value)

    elif isinstance(data, list):
        # Process each item in a list
        data = [transform_yaml(item) for item in data]

    return data

# Get all .yaml and .yml files in the directory
yaml_files = list(directory.glob("*.yml")) + list(directory.glob("*.yaml"))

for file_path in yaml_files:
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        if data:
            data = transform_yaml(data)

        output_file_path = output_folder / file_path.name
        with open(output_file_path, "w") as output_file:
            yaml.dump(data, output_file, default_flow_style=False)

        print(f"Processed: {file_path} -> {output_file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"All YAML files have been processed and saved to: {output_folder}")
