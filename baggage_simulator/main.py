import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from gui import SecuritySimulationGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = SecuritySimulationGUI(root)
    root.mainloop()