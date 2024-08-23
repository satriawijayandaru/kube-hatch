import os

def convert_yml(input_file):
    # Generate the output filename by appending "delimit-changer" before the file extension
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}-delimit-changer{ext}"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Find the first occurrence of '=' and replace it with ': '
            if '=' in line:
                key, value = line.split('=', 1)
                line = f"{key}: {value}"
            outfile.write(line)

    print(f"Conversion complete. Output saved to: {output_file}")

# Prompting the user for input file name
input_file = input("Enter the path to the input YAML file: ")

# Call the function with the user-provided file name
convert_yml(input_file)
