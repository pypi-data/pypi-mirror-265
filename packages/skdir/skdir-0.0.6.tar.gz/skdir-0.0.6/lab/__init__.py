# __init__.py

# Import any modules or symbols needed for printing the AIML code files
import os
import numpy
import sklearn
import matplotlib

# Define the directory path where the AIML code files are located
AIML_CODE_DIR = 'Users/sharathchandrak/Desktop/avi_package-main/lab'

# Function to print the contents of AIML code files
def print_aiml_code_files():
    for filename in os.listdir():
        if filename.endswith('.aiml'):
            with open(os.path.join(AIML_CODE_DIR, filename), 'r') as file:
                print(f"AIML Code File: {filename}")
                print(file.read())
                print("=" * 50)

# Call the function to print the contents of AIML code files when the package is imported
print_aiml_code_files()
