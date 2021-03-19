import tkinter as tk
import json
import os
import sys


ROOT = tk.Tk()

with open("data//settings.json", "r") as file:
    SETTINGS_DATA = json.load(file)

if not os.path.exists("Videos"):
    os.mkdir("Videos")

if not os.path.exists("data//open_hardware_monitor//OpenHardwareMonitorLib.dll"):
    input("Cannot find 'data//open_hardware_monitor//OpenHardwareMonitorLib.dll'")
    sys.exit()
