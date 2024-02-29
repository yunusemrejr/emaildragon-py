import os
import tkinter as tk
import mailaction

# Global variables for file paths
file_path = "multipletarget.txt"
to_txt_file = "inputFolder/to.txt"
name_txt_file = "inputFolder/name.txt"

# List to store multiple targets
multiple_targets_list = []

# Store initial contents of the files
initial_to_content = ""
initial_name_content = ""

def read_initial_contents():
    """
    Function to read initial contents of the files.
    """
    global initial_to_content, initial_name_content
    initial_to_content = read_file(to_txt_file)
    initial_name_content = read_file(name_txt_file)

def read_file(file_path):
    """
    Function to read content from a file.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_file(file_path, content):
    """
    Function to write content to a file.
    """
    with open(file_path, 'w') as file:
        file.write(content)

def restore_initial_contents():
    """
    Function to restore initial contents of the files.
    """
    write_file(to_txt_file, initial_to_content)
    write_file(name_txt_file, initial_name_content)

try:
    if __name__ == "__main__":
        # Read initial contents of the files
        read_initial_contents()
        
        # Open the file containing multiple targets
        with open(file_path, "r") as f:
            # Read each line and split by comma
            for line in f:
                elements = line.strip().split(',')
                multiple_targets_list.extend(elements)
            
            # Iterate through the list in pairs
            for i in range(0, len(multiple_targets_list), 2):
                name = multiple_targets_list[i]
                email = multiple_targets_list[i + 1]

                # Write name to name_txt_file
                write_file(name_txt_file, name + "\n")
                # Write email to to_txt_file
                write_file(to_txt_file, email + "\n")
                
                # Perform action when every pair is processed
                root = tk.Tk()   
                mailaction.main(root)

except FileNotFoundError:
    # Initialize Tkinter if the file is not found
    root = tk.Tk()
    mailaction.main(root)

finally:
    # Restore initial contents of the files
    restore_initial_contents()
