import matplotlib.pyplot as plt
import numpy as np
import itertools
import os
import glob

def plot(file_path, parameter_names):
    """
    Plots specified parameters from a given file.
    
    Args:
    - file_path: Path to the data file.
    - parameter_names: List of parameter names to plot.
    """
    data = []
    axis_names = []
    selected_columns = []
    
    # Open the file and read data
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("#"):
                # Extracting axis names
                axis_names = line.strip().split('\t')
                # Determine which columns to plot based on parameter_names
                selected_columns = [axis_names.index(name) for name in parameter_names if name in axis_names]
            else:
                values = [float(value) for value in line.split("\t")]
                data.append(values)
    
    if not selected_columns:  # Check if selected_columns is empty
        print("None of the specified parameters were found in the file.")
        return
    
    # Convert the list of lists into a NumPy array for easier slicing
    data = np.array(data)
    
    # Adjust the number of subplots based on selected parameters
    num_parameters = len(selected_columns)
    
    # Creating subplots
    fig, axs = plt.subplots(num_parameters, 1, figsize=(10, num_parameters * 3), squeeze=False)
    
    # Loop over each selected parameter to create a subplot
    for i, column_index in enumerate(selected_columns):
        axs[i, 0].plot(data[:, 0], data[:, column_index], label=f"${axis_names[column_index]}$")
        axs[i, 0].set_xlabel(axis_names[0])
        axs[i, 0].set_ylabel(axis_names[column_index])
        axs[i, 0].legend()
    
    # Adjust layout to prevent overlapping
    plt.tight_layout()
    plt.show()


def float_range(start, stop, step):
    """
    Generates a list of numbers from start to stop with a given step increment, works with floats.
    """
    while start < stop:
        yield round(start, 10)  # Round to avoid floating-point arithmetic issues
        start += step

def m3_commands(base_folder, filename_pattern, ranges):
    """
    Prints mumax3 commands for files based on a pattern with multiple 'cng' placeholders,
    each having different start, end values, and increments, and then prints 'mumax3' at the end.
    This version supports fractional increments and adjusts the base_folder path for Windows compatibility.
    
    Args:
    - base_folder: The base folder address where the files are located or will be saved.
    - filename_pattern: The pattern of the filename with 'cng' as placeholders.
    - ranges: A list of tuples, each tuple contains (start_value, end_value, increment) for each 'cng'.
    """
    # Adjust the base_folder path for Windows compatibility
    base_folder = base_folder.replace('/', '\\')
    
    # Generate all combinations of replacements for 'cng' with support for fractional increments
    replacement_lists = [list(float_range(start, end + increment, increment)) for start, end, increment in ranges]
    all_combinations = list(itertools.product(*replacement_lists))
    
    for combination in all_combinations:
        # Start with the initial pattern for each combination
        filename = filename_pattern
        
        # Replace each 'cng' with the corresponding value from the combination
        for value in combination:
            filename = filename.replace('cng', str(value), 1)  # Replace the first occurrence
        
        full_command = f"mumax3 {base_folder}\\{filename}"
        print(full_command)
    
    # Print the final 'mumax3' command
    print('mumax3')


def rename_tables(base_dir):
    """
    Renames all 'table.txt' files to match their parent folder names (without the '.out' extension) with '.txt' extension,
    within folders ending with '.out' found anywhere under the specified base directory.
    Automatically converts backslashes in the base directory path to forward slashes to avoid Unicode errors.
    
    Args:
    - base_dir: The base directory to recursively search for '.out' folders.
    """
    # Automatically convert backslashes to forward slashes to avoid Unicode errors
    base_dir = base_dir.replace("\\", "/")

    # Pattern to match all '.out' folders within the base directory, recursively
    out_folders_pattern = os.path.join(base_dir, "**", "*.out")
    
    # Find all folders matching the pattern, recursively
    out_folders = glob.glob(out_folders_pattern, recursive=True)
    
    for folder in out_folders:
        old_file_path = os.path.join(folder, "table.txt")
        if os.path.exists(old_file_path):  # Check if 'table.txt' exists in the folder
            # Extract the folder name without the path and remove '.out' extension
            base_name = os.path.basename(folder).replace(".out", "")
            new_file_name = f"{base_name}.txt"
            new_file_path = os.path.join(folder, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{old_file_path}' to '{new_file_path}'")

def plot_list(file_path):
    """
    Lists the parameters available for plotting from a given file, excluding the independent variable.
    
    Args:
    - file_path: Path to the data file.
    
    Returns:
    - A list of parameter names that can be plotted, excluding the independent variable.
    """
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("#"):
                    # Assuming the first line that starts with "#" contains the headers
                    parameters = line.strip("#").strip().split('\t')
                    # Exclude the first parameter (independent variable) and return the rest
                    return [param for param in parameters[1:] if param]  # Skip the first element
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    # In case no parameters were found or the file couldn't be read
    print("No parameters found or unable to read the file.")
    return []


def dlt_ovf(folder_path):
    # Count of deleted files for reporting
    deleted_files_count = 0
    
    # Walk through all directories and files in the specified folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".ovf"):
                file_path = os.path.join(root, file)
                print(f"Deleting: {file_path}")
                os.remove(file_path)  # Delete the file
                deleted_files_count += 1
    
    print(f"Total .ovf files deleted: {deleted_files_count}")

import subprocess

def start_learing():
    repo_urls = [
        "https://github.com/ITCPR/learning.git",
        "https://github.com/ITCPR/mumax3.git",
        "https://github.com/ITCPR/python-codes.git"
    ]
    # Prompt the user for the third repository URL
    third_repo_url = input("Please enter your name ID: ")
    repo_urls.append("https://github.com/ITCPR/"+third_repo_url+".git")
    
    for url in repo_urls:
        try:
            # Run the git clone command
            subprocess.run(["git", "clone", url], check=True)
            print(f"Successfully cloned {url}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {url}. Error: {e}")

    