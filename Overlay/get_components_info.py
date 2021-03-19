import psutil
import pythonping
import GPUtil
import threading
import os
import clr
import termcolor
import time
clr.AddReference(os.path.abspath("data//OpenHardwareMonitor//OpenHardwareMonitorLib.dll"))
from OpenHardwareMonitor import Hardware
import user_actions
import config


class GetDisplayData:
    def __init__(self, display_function):
        self.loading = True
        threading._start_new_thread(self.loading_animation, ())

        self.display = display_function

        self.ip_server_to_pinging = "155.133.250.1"  # EU west CS-GO server
        self.ping = int(pythonping.ping(self.ip_server_to_pinging).rtt_max_ms)
        self.pinging = False

        self.old_internet_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

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
        threading._start_new_thread(user_actions.get_user_input, ())

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
        if config.SETTINGS_DATA["ping_function"]:
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
        text = f"CPU - Using: {'%.1f' % cpu_usage}%"
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
        text = f"RAM - Total: {'%.1f' % ram_usage_total}GB"
        row = 6
        column = 1
        self.display(text, row, column, self.get_max_ram)

    def get_ram_usage(self):
        ram_usage = psutil.virtual_memory()  # divide by 2**30 to convert to GB
        text = f"Using: {'%.1f' % float(ram_usage.used / 2 ** 30)}GB ({ram_usage.percent}%)"
        row = 6
        column = 2
        self.display(text, row, column, self.get_ram_usage)
