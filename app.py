#cd into the ui and run "streamlit run main_ui.py"
import os
import sys
import subprocess

# Define the target folder and command
folder = "ui"
command = "streamlit run login.py"

# Run the command in the target folder
subprocess.run(command, cwd=folder, shell=True)