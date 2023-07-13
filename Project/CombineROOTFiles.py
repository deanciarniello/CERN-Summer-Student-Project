import uproot
import os

# Input directory containing the ROOT files
input_directory = "output"

# Output ROOT file
output_file = "file.root"

# Get a list of all ROOT files in the input directory
root_files = [file for file in os.listdir(input_directory) if file.endswith(".root")]

# Create lists to store the TTree objects from each input file
tree_list_1 = []
tree_list_2 = []

# Loop over each ROOT file and extract the TTrees
for root_file in root_files:
    file_path = os.path.join(input_directory, root_file)
    with uproot.open(file_path) as infile:
        tree_1 = infile["PrimaryEvents"]  # Modify "tree_name_1" with the name of the first TTree in your ROOT files
        tree_2 = infile["AllEvents"]  # Modify "tree_name_2" with the name of the second TTree in your ROOT files
        tree_list_1.append(tree_1)
        tree_list_2.append(tree_2)

# Merge all the TTree objects into a single TTree
merged_tree_1 = uproot.concatenate(tree_list_1)
merged_tree_2 = uproot.concatenate(tree_list_2)

# Remove the output file if it already exists
if os.path.exists(output_file):
    os.remove(output_file)

# Write the merged TTrees to the output ROOT file
with uproot.recreate(output_file) as outfile:
    outfile["PrimaryEvents"] = merged_tree_1  # Modify "merged_tree_1" with the desired name for the merged first TTree
    outfile["AllEvents"] = merged_tree_2  # Modify "merged_tree_2" with the desired name for the merged second TTree
