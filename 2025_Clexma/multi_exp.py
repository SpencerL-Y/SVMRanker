import os
import sys
import time
import subprocess
from datetime import datetime

PROJECT_ROOT = os.getcwd()
CLEXMA_PATH = os.path.join(PROJECT_ROOT, "2025_Clexma")
BOOGIE_PROGRAM_FOLDER = os.path.join(PROJECT_ROOT, "Program_non")
C_BOOGIE_PROGRAM_FOLDER = os.path.join(PROJECT_ROOT, "C_Boogies")
RUNNING_TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, "src", "template")

if __name__ == "__main__":
    # Prepare result directories with timestamp
    time_str = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    folder_name = "result_" + time_str.strip().replace(" ", "")
    template_folder_name = "templates"
    RESULT_FOLDER = os.path.join(CLEXMA_PATH, "Multi", folder_name)
    TEMPLATE_FOLDER = os.path.join(RESULT_FOLDER, template_folder_name)
    os.makedirs(RESULT_FOLDER, exist_ok=True)

    # Helper to run a command with a 900-second timeout
    def run_with_timeout(cmd_list, output_file):
        with open(output_file, 'a') as f:
            start = time.time()
            try:
                subprocess.run(cmd_list, stdout=f, stderr=subprocess.STDOUT, timeout=300)
            except subprocess.TimeoutExpired:
                f.write(f"\nERROR: Command timed out after 300 seconds\n")
            end = time.time()
            f.write(f"\nRunning time: {end - start:.6f} s\n")
            print(f"\nRunning time: {end - start:.6f} s")
    
    # Process Boogie programs
    for folder in [C_BOOGIE_PROGRAM_FOLDER, BOOGIE_PROGRAM_FOLDER]:
        for file in os.listdir(folder):
            if file.endswith(".bpl"):
                input_path = os.path.join(folder, file)
                output_path = os.path.join(RESULT_FOLDER, f"output_{file}.txt")
                cmd = ["python3", os.path.join(PROJECT_ROOT, "src", "CLIMain.py"),
                       "lmulti", "--depth_bound", "4", input_path]
                print("Running:", " ".join(cmd))
                run_with_timeout(cmd, output_path)

    # Move generated templates
    os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
    for item in os.listdir(RUNNING_TEMPLATE_FOLDER):
        os.rename(os.path.join(RUNNING_TEMPLATE_FOLDER, item), os.path.join(TEMPLATE_FOLDER, item))
