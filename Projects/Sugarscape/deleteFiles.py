import os

folder = "chests"
files = os.listdir(folder)
save_files = ["GUI.py", "Model.py", "Patch.py", "Agent.py",
              "AgentBranch.py", "deleteFiles.py"
              "sugar-map.txt", "testDctDelete.py", "__pycache__",
              "No Exchange"]
for file in files:
    if file not in save_files:
        os.remove(folder + "\\" + file)