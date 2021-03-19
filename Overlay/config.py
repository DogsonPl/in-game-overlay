import tkinter as tk
import json
import os
import sys
import wget
import zipfile


ROOT = tk.Tk()

try:
    with open("data//settings.json", "r") as file:
        SETTINGS_DATA = json.load(file)
except FileNotFoundError:
    SETTINGS_DATA = {"font_size": 14, "refresh": 1000, "font_color": "yellow", "ping_function": True}


if not os.path.exists("Videos"):
    os.mkdir("Videos")

if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("data//videos_data"):
    os.mkdir("data//videos_data")

if not os.path.exists("data//OpenHardwareMonitor//OpenHardwareMonitorLib.dll"):
    wget.download("https://openhardwaremonitor.org/files/openhardwaremonitor-v0.9.6.zip", "data//")
    with zipfile.ZipFile("data//openhardwaremonitor-v0.9.6.zip") as file:
        file.extractall("data//")
    os.remove("data//openhardwaremonitor-v0.9.6.zip")
