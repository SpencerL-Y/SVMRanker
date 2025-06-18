import os
import subprocess
from datetime import datetime
import time

PROJECT_ROOT = os.getcwd()
CLEXMA_PATH = os.path.join(PROJECT_ROOT, "2025_Clexma")
BOOGIE_PROGRAM_FOLDER = os.path.join(PROJECT_ROOT, "Program_non")
RUNNING_TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, "src", "template")

if __name__ == "__main__":
    # Prepare result directory with timestamp
    time_str = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    folder_name = "result_" + time_str.strip().replace(" ", "")
    template_folder_name = "templates"
    RESULT_FOLDER = os.path.join(CLEXMA_PATH, "Nested", folder_name)
    TEMPLATE_FOLDER = os.path.join(RESULT_FOLDER, template_folder_name)
    os.makedirs(RESULT_FOLDER, exist_ok=True)

    # Helper: run command with 300s timeout and log output
    def run_with_timeout(cmd_list, output_file):
        with open(output_file, 'a') as f:
            start = time.time()
            try:
                subprocess.run(cmd_list, stdout=f, stderr=subprocess.STDOUT, timeout=300)
            except subprocess.TimeoutExpired:
                f.write("\nERROR: Command timed out after 300 seconds\n")
            end = time.time()
            f.write(f"\nRunning time: {end - start:.6f} s\n")

    # Iterate and run nested analysis
    for file in os.listdir(BOOGIE_PROGRAM_FOLDER):
        if file.endswith(".bpl"):
            input_path = os.path.join(BOOGIE_PROGRAM_FOLDER, file)
            output_path = os.path.join(RESULT_FOLDER, f"output_{file}.txt")
            cmd = ["python3", os.path.join(PROJECT_ROOT, "src", "CLIMain.py"),
                   "lnested", "--depth_bound", "4", input_path]
            print("Running:", " ".join(cmd))
            run_with_timeout(cmd, output_path)

    # Move templates
    os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
    for item in os.listdir(RUNNING_TEMPLATE_FOLDER):
        os.replace(os.path.join(RUNNING_TEMPLATE_FOLDER, item), os.path.join(TEMPLATE_FOLDER, item))
