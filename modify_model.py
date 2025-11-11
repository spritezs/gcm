import re
import sys

param_name = sys.argv[1]
output_dir = sys.argv[2]
model = sys.argv[3]

keywords = ["find", "letting", "such that"]

with open(f"./{output_dir}/model000001.eprime", 'r') as file:
    lines = file.readlines()

# Now find the first line that contains any of the keywords
start_index = 0
for i, line in enumerate(lines):
    if any(word in line for word in keywords):
        start_index = i
        break

with open(f"./Params/{param_name}.eprime-param", 'r') as file2:
    additional_lines = file2.readlines()

new_lines = additional_lines + lines[start_index:]
new_lines = [line for line in new_lines if not line.startswith(("$","branching","minimising"))]

# Create a dictionary to store the values of finX
fin_values = {}

# Capture the values of fin1, fin2, etc.
for line in new_lines:
    match = re.match(r'letting fin(\d+) be (\d+)', line)
    if match:
        fin_key = match.group(1)
        fin_value = match.group(2)
        fin_values[fin_key] = fin_value

# Replace the line 'letting nbObservations be fin1' with the value of fin1
new_lines = [
    re.sub(r'letting nbObservations be fin1', 
           lambda m: f'letting nbObservations be {fin_values.get("1", "fin1")}', 
           line) 
    for line in new_lines
]


# Now, remove the block starting with 'letting n be' and ending with 'letting nbObservations be fin4'
n_block_started = False
n_block_ended = False
final_lines = []

for line in new_lines:
    if not n_block_started:
        # Check if the line starts with 'letting n be'
        if line.startswith("letting n be"):
            # Replace it with the correct value of fin4 and start removing the block
            final_lines.append(f"letting n be {fin_values.get('4', 'fin4')} \n")
            n_block_started = True
        else:
            final_lines.append(line)
    else:
        # Keep removing lines until we encounter 'letting nbObservations be '
        if line.startswith("letting nbObservations be "):
            n_block_ended = True
        # Skip lines in the 'letting n be' block
        if not n_block_ended:
            continue
        else:
            final_lines.append(line)

fl1 = []

# Assuming final_lines is a list of lines
for line in final_lines:
    if "find" in line:  # Check if the line contains the keyword
        break  # Exit the loop when the keyword is found
    fl1.append(line)  # Use append() instead of add()

with open(f"./{model}-final/{model}.eprime", 'r') as file:
    lines = file.readlines()
    fl1.extend(lines)

# Now write the modified lines back to the file
with open(f"./{output_dir}/{model}.eprime", 'w') as file:
    file.writelines(fl1) 










