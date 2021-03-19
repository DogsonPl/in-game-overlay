import tkinter as tk
import json


ROOT = tk.Tk()

with open("data//settings.json", "r") as file:
    SETTINGS_DATA = json.load(file)
