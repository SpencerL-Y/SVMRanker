import os
import sys
import time
PROJECT_ROOT = os.getcwd()
CLEXMA_PATH = os.path.join(PROJECT_ROOT, "2025_Clexma")
BOOGIE_PROGRAM_FOLDER = os.path.join(PROJECT_ROOT, "Program_non")
RUNNING_TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, "src", "template")
if __name__ == "__main__":
    from datetime import datetime

    time_str = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    folder_name = "result_" + time_str.strip().replace(" ", "")
    template_folder_name = "templates"
    RESULT_FOLDER = os.path.join(CLEXMA_PATH, "Nested", folder_name)
    TEMPLATE_FOLDER = os.path.join(RESULT_FOLDER, template_folder_name)
    os.makedirs(RESULT_FOLDER)
    for file in os.listdir(BOOGIE_PROGRAM_FOLDER):
        if file.endswith("bpl"):
            command = ["python3", os.path.join(PROJECT_ROOT, "src", "CLIMain.py"), "lnested", "--depth_bound 4", os.path.join(BOOGIE_PROGRAM_FOLDER, file), ">>", os.path.join(RESULT_FOLDER, "output_" + file + ".txt")]
            
            print(" ".join(command))
            start = time.time()
            os.system(" ".join(command))
            end = time.time()
            os.system( "echo " + f"Running time: {end - start:.6f} s >> " + os.path.join(RESULT_FOLDER, "output_" + file + ".txt"))
            print(f"Running time: {end - start:.6f} s")
            
    os.system("mv " + os.path.join(RUNNING_TEMPLATE_FOLDER, "*") + " " + TEMPLATE_FOLDER)
