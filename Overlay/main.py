import tkinter as tk
import psutil
import sys
import GPUtil
import threading
import os
import time
import json
import recorder
import webbrowser
import pythonping
import termcolor
import colorama
import clr
clr.AddReference(os.path.abspath("data//open_hardware_monitor//OpenHardwareMonitorLib.dll"))
from OpenHardwareMonitor import Hardware


class DisplayOverlay:
    def __init__(self):

        self.overlay = tk.Canvas(width=910, height=310, highlightthickness=0)
        self.overlay.master.overrideredirect(True)
        self.overlay.master.lift()
        #self.overlay.master.wm_attributes("-disabled", True)
        self.overlay.master.wm_attributes("-topmost", True)
        self.overlay.master.wm_attributes("-transparentcolor", "gray30")
        self.overlay.create_rectangle(0, 0, 910, 310, fill="gray30")
        self.overlay.pack()

        GetDisplayData(self.display_label)

    def display_label(self, text, row, column, get_data_function):
        label = tk.Label(self.overlay, text=text, bg="gray30", fg=SETTINGS_DATA["font_color"],
                         font=("Comic Sans MS", SETTINGS_DATA["font_size"], "bold"))
        label.grid(row=row, column=column)
        label.after(SETTINGS_DATA["refresh"], get_data_function)
        label.after(SETTINGS_DATA["refresh"], label.destroy)


class GetDisplayData:
    def __init__(self, display_function):
        self.loading = True
        threading._start_new_thread(self.loading_animation, ())

        self.display = display_function

        self.ip_server_to_pinging = "146.66.153.12"  # EU west CS-GO server
        self.ping = int(pythonping.ping(self.ip_server_to_pinging).rtt_max_ms)
        self.pinging = False

        self.old_internet_usage = (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv)

        self.is_admin = True
        self.is_gpu = True

        self.computer = Hardware.Computer()
        self.computer.CPUEnabled = True
        self.computer.GPUEnabled = True
        self.computer.Open()

        threading._start_new_thread(self.get_current_fps, ())
        threading._start_new_thread(self.get_average_fps, ())
        threading._start_new_thread(self.get_ping, ())
        threading._start_new_thread(self.get_internet_usage, ())
        threading._start_new_thread(self.get_cpu_usage, ())
        threading._start_new_thread(self.get_cpu_temp, ())
        threading._start_new_thread(self.get_gpu_usage, ())
        threading._start_new_thread(self.get_gpu_temp, ())
        threading._start_new_thread(self.get_gpu_memory_max, ())
        threading._start_new_thread(self.get_gpu_memory_usage, ())
        threading._start_new_thread(self.get_max_ram, ())
        threading._start_new_thread(self.get_ram_usage, ())

        self.loading = False
        time.sleep(0.2)
        threading._start_new_thread(GettingAndSavingUserConfig().get_user_input, ())

    def loading_animation(self):
        animation_text = [" [=     ]", " [ =    ]", " [  =   ]", " [   =  ]", " [    = ]",
                          " [     =]", " [    = ]", " [   =  ]", " [  =   ]", " [ =    ]"]
        i = 0
        while self.loading:
            print(termcolor.colored(animation_text[i % len(animation_text)], "blue"), end="\r")
            i += 1
            time.sleep(0.2)

    def get_current_fps(self):
        fps = "soon"  # todo
        text = f"FPS: {fps}"
        row = 1
        column = 1
        self.display(text, row, column, self.get_current_fps)

    def get_average_fps(self):
        average_fps = "soon"  # todo
        text = f"Average FPS: {average_fps}"
        row = 1
        column = 2
        self.display(text, row, column, self.get_average_fps)

    def get_ping(self):
        if SETTINGS_DATA["ping_function"]:
            if not self.pinging:
                threading._start_new_thread(self.pinging_function, ())
            text = f"Ping: {self.ping}ms"
        else:
            text = "Ping: OFF"
        row = 2
        column = 1
        self.display(text, row, column, self.get_ping)

    def pinging_function(self):
        self.pinging = True
        ping_test = pythonping.ping(self.ip_server_to_pinging)
        if int(ping_test.rtt_max_ms) == 2000:
            self.ping = "Internet proble"
        else:
            self.ping = int(ping_test.rtt_avg_ms)
        self.pinging = False

    def get_internet_usage(self):
        new_internet_usage = (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv)
        internet_usage = (new_internet_usage - self.old_internet_usage) / 1024. / 1024. * 8  # /1024./1024.*8 to convert to Mb/s
        self.old_internet_usage = new_internet_usage
        text = f"Internet usage: {'%.2f' % internet_usage}Mb/s"
        row = 2
        column = 2
        self.display(text, row, column, self.get_internet_usage)

    def get_cpu_usage(self):
        cpu_usage = psutil.cpu_percent()
        text = f"Cpu - Using: {'%.1f' % cpu_usage}%"
        row = 3
        column = 1
        self.display(text, row, column, self.get_cpu_usage)

    def get_cpu_temp(self):
        self.computer.Hardware[0].Update()
        temps = []
        for a in range(0, len(self.computer.Hardware[0].Sensors)):
            # print(self.computer.Hardware[0].Sensors[a].Identifier)
            if "temperature" in str(self.computer.Hardware[0].Sensors[a].Identifier):
                temps.append(self.computer.Hardware[0].Sensors[a].get_Value())
        try:
            cpu_temp = sum(temps) / len(temps)
            text = f"Temp: {'%.1f' % cpu_temp}C"
        except TypeError:
            if self.is_admin:
                print(termcolor.colored("""Can't get access to CPU temperature. To see CPU temperature run program as admin
Source: https://www.digitalcitizen.life/run-as-admin/\n""", "red"))
            text = "Temp: None"
            self.is_admin = False
        row = 3
        column = 2
        self.display(text, row, column, self.get_cpu_temp)

    def get_gpu_usage(self):
        try:
            gpu_usage = GPUtil.showUtilization()
            text = f"GPU - Using: {'%.1f' % float(gpu_usage.load * 100)}%"
        except UnboundLocalError:
            if self.is_gpu:
                print(termcolor.colored("Can't find GPU\n", "red"))
            text = "GPU - Using: None"
            self.is_gpu = False
        row = 4
        column = 1
        self.display(text, row, column, self.get_gpu_usage)

    def get_gpu_temp(self):
        try:
            self.computer.Hardware[1].Update()
            gpu_temperature = self.computer.Hardware[1].Sensors[0].Value
            text = f"Temp: {gpu_temperature}C"
        except UnboundLocalError:
            text = "Temp: None"
        row = 4
        column = 2
        self.display(text, row, column, self.get_gpu_temp)

    def get_gpu_memory_max(self):
        try:
            gpu_usage = GPUtil.showUtilization()
            text = f"GPU memory - Total: {'%.2f' % float(gpu_usage.memoryTotal / 1000)}GB"
        except UnboundLocalError:
            text = "GPU memory - Total: None"
        row = 5
        column = 1
        self.display(text, row, column, self.get_gpu_memory_max)

    def get_gpu_memory_usage(self):
        try:
            gpu_usage = GPUtil.showUtilization()
            text = f"Using: {'%.2f' % float(gpu_usage.memoryUsed / 1000)}GB ({'%.1f' % (float(gpu_usage.memoryUsed / gpu_usage.memoryTotal) * 100)}%)"
        except UnboundLocalError:
            text = "Using: None"
        row = 5
        column = 2
        self.display(text, row, column, self.get_gpu_memory_usage)

    def get_max_ram(self):
        ram_usage_total = psutil.virtual_memory().total / 2 ** 30  # divide by 2**30 to convert to GB
        text = f"Ram - Total: {'%.1f' % ram_usage_total}GB"
        row = 6
        column = 1
        self.display(text, row, column, self.get_max_ram)

    def get_ram_usage(self):
        ram_usage = psutil.virtual_memory()  # divide by 2**30 to convert to GB
        text = f"Using: {'%.1f' % float(ram_usage.used / 2 ** 30)}GB ({ram_usage.percent}%)"
        row = 6
        column = 2
        self.display(text, row, column, self.get_ram_usage)


class GettingAndSavingUserConfig:
    def get_user_input(self):
        while True:
            commend = input("Write command (help to get commands list, q to quit program) --> ")
            if commend == "help":
                self.send_help_command()
            elif commend == "q":
                self.quit_from_program()
            elif commend == "fs":
                self.change_font_size()
            elif commend == "fc":
                self.change_font_color()
            elif commend == "ref":
                self.change_refresh_time()
            elif commend == "ping":
                self.ping_label_switch()
            elif commend == "record":
                recording(self.get_user_input)
                break

    @staticmethod
    def send_help_command():
        print(f"""\nVersion: 0.7
Available commands:
{termcolor.colored('help', 'blue', attrs=['bold'])} - send commands
{termcolor.colored('q', 'blue', attrs=['bold'])} - quit from program
{termcolor.colored('fs', 'blue', attrs=['bold'])} - change font size
{termcolor.colored('fc', 'blue', attrs=['bold'])} - change font color
{termcolor.colored('ref', 'blue', attrs=['bold'])} - change refresh time
{termcolor.colored('ping', 'blue', attrs=['bold'])} - disable/enable ping label
{termcolor.colored('record', 'blue', attrs=['bold'])} - record screen\n""")

    def quit_from_program(self):
        input("\nThanks for using my program. Hope you liked it! Click enter to close program")
        ROOT.quit()
        sys.exit()

    def change_font_size(self):
        while True:
            try:
                new_font_size = int(input(f"Current font size: {SETTINGS_DATA['font_size']}\nWrite new font_size: "))
                break
            except ValueError:
                print(termcolor.colored("You have to write number like 10", "red"))
        if new_font_size > 25:
            new_font_size = 25
            print(termcolor.colored("Max font size is 25", "red"))
        elif new_font_size < 5:
            new_font_size = 5
            print(termcolor.colored("Minimum font size is 5", "red"))
        SETTINGS_DATA["font_size"] = new_font_size
        print(termcolor.colored(f"New font size is {new_font_size}\n", "yellow"))
        self.save()

    def change_font_color(self):
        while True:
            try:
                new_color = input(
                    f"Current color: {SETTINGS_DATA['font_color']}\nWrite new color\nIf you want see all available colors write 1: ")
                if new_color == "1":
                    webbrowser.open(
                        "http://www.science.smith.edu/dftwiki/images/thumb/3/3d/TkInterColorCharts.png/800px-TkInterColorCharts.png")
                else:
                    test_label = tk.Label(fg=new_color)
                    break
            except tk.TclError:
                print(termcolor.colored("Wrong color", "red"))
        SETTINGS_DATA["font_color"] = new_color
        print(termcolor.colored(f"New color is {new_color}\n", "yellow"))
        self.save()

    def change_refresh_time(self):
        while True:
            try:
                new_refresh_time = float(
                    input(
                        f"Current refresh time: {SETTINGS_DATA['refresh'] / 1000}\nWrite new refresh time (in sec): "))
                break
            except ValueError:
                print(termcolor.colored("You have to write number like 10", "red"))
        if new_refresh_time > 50:
            new_refresh_time = 50
            print(termcolor.colored("Max refresh_time is 50", "red"))
        elif new_refresh_time < 0.2:
            new_refresh_time = 0.2
            print(termcolor.colored("Minimum refresh time is 0.2", "red"))
        new_refresh_time *= 1000  # because 1sec = 1000 in tkinter
        SETTINGS_DATA["refresh"] = int(new_refresh_time)
        print(termcolor.colored(f"New refresh time is {new_refresh_time / 1000}sec\n", "yellow"))
        self.save()

    def ping_label_switch(self):
        if SETTINGS_DATA["ping_function"]:
            print(termcolor.colored("Ping label is now disabled", "yellow"))
            SETTINGS_DATA["ping_function"] = False
        else:
            print(termcolor.colored("Ping label is now enabled", "yellow"))
            SETTINGS_DATA["ping_function"] = True
        self.save()

    @staticmethod
    def save():
        with open("data/settings.json", "w") as file:
            json.dump(SETTINGS_DATA, file)


def recording(checking_input_function):
    print(termcolor.colored("\nIf you have noises, turn off microphone", "yellow"))
    while True:
        try:
            fps = int(input("Write in how many fps record video: "))
            break
        except ValueError:
            print(termcolor.colored("You have to write number", "red"))
    if fps > 75:
        fps = 75
        print(termcolor.colored("Max fps is 75", "red"))
    elif fps < 5:
        fps = 5
        print(termcolor.colored("Minimum fps is 5", "red"))
    i = 5
    for _ in range(5):
        print(f"Time to start: {i}")
        i -= 1
        time.sleep(1)
    recorder.Recorder(checking_input_function, fps)


if __name__ == '__main__':
    colorama.init()

    made_by = """
.___  ___.      ___       _______   _______        .______   ____    ____       
|   \/   |     /   \     |       \ |   ____|       |   _  \  \   \  /   /       
|  \  /  |    /  ^  \    |  .--.  ||  |__          |  |_)  |  \   \/   /        
|  |\/|  |   /  /_\  \   |  |  |  ||   __|         |   _  <    \_    _/         
|  |  |  |  /  _____  \  |  '--'  ||  |____        |  |_)  |     |  |           
|__|  |__| /__/     \__\ |_______/ |_______|       |______/      |__|           
"""
    made_by2 = """
 _______    ______     _______      _______.  ______   .__   __.    
|       \  /  __  \   /  _____|    /       | /  __  \  |  \ |  |
|  .--.  ||  |  |  | |  |  __     |   (----`|  |  |  | |   \|  |
|  |  |  ||  |  |  | |  | |_ |     \   \    |  |  |  | |  . `  |
|  '--'  ||  `--'  | |  |__| | .----)   |   |  `--'  | |  |\   |
|_______/  \______/   \______| |_______/     \______/  |__| \__|
"""

    print(termcolor.colored(made_by, "green"))
    print(termcolor.colored(made_by2, "green"))
    print(termcolor.colored("""Loading program...
You can minimize this window. Close this window if you want close program
If this program don't work in game, change game settings to display game in window\n""", "blue", attrs=["bold"]))
    print(termcolor.colored("""Ping is pinging only EU west CS-GO server, soo in other games ping can be different
In addition this option can slow down your Internet a bit. Write ping to disable this option\n""", "yellow"))

    with open("data//settings.json", "r") as file:
        SETTINGS_DATA = json.load(file)
    ROOT = tk.Tk()

    DisplayOverlay()
    ROOT.mainloop()

