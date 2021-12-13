import json
import os
import clr

import tkinter as tk
import colorama

colorama.init()

ROOT = tk.Tk()

try:
    with open("data//settings.json", "r") as file:
        SETTINGS_DATA = json.load(file)
except FileNotFoundError:
    SETTINGS_DATA = {"font_size": 14, "refresh": 1000, "font_color": "yellow", "ping_function": True}

SLEEP_IN_SEC = SETTINGS_DATA["refresh"]/1000

if not os.path.exists("Videos"):
    os.mkdir("Videos")

if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("data//videos_data"):
    os.mkdir("data//videos_data")

if not os.path.exists("data//OpenHardwareMonitor//OpenHardwareMonitorLib.dll"):
    import wget
    import zipfile
    print("Downloading required files to run program...")
    wget.download("https://openhardwaremonitor.org/files/openhardwaremonitor-v0.9.6.zip", "data//")
    with zipfile.ZipFile("data//openhardwaremonitor-v0.9.6.zip") as file:
        file.extractall("data//")
    os.remove("data//openhardwaremonitor-v0.9.6.zip")

clr.AddReference(os.path.abspath("data//OpenHardwareMonitor//OpenHardwareMonitorLib.dll"))
