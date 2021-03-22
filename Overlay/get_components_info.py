import psutil
import pythonping
import GPUtil
import threading
import termcolor
import time
import user_actions
import config
from components_info import COMPONENTS_INFO
from OpenHardwareMonitor import Hardware

COMPUTER = Hardware.Computer()
COMPUTER.CPUEnabled = True
COMPUTER.GPUEnabled = True
COMPUTER.Open()

# todo finish refactoring
class GetDisplayData:
    def __init__(self):
        threading._start_new_thread(GetGPUInfo, ())
        threading._start_new_thread(GetCPUInfo, ())
        threading._start_new_thread(GetRAMInfo, ())
        threading._start_new_thread(GetGPUInfo, ())
        threading._start_new_thread(GetFPSInfo, ())
        threading._start_new_thread(GetInternetInfo, ())

        time.sleep(0.2)
        user_actions.get_user_input()


class GetCPUInfo:
    def __init__(self):
        threading._start_new_thread(self.get_cpu_usage, ())
        self.get_cpu_temp()

    @staticmethod
    def get_cpu_usage():
        while True:
            cpu_usage = psutil.cpu_percent()
            COMPONENTS_INFO["cpu_usage"]["message"] = f"CPU - Using: {'%.1f' % cpu_usage}%"
            time.sleep(config.SLEEP_IN_SEC)

    @staticmethod
    def get_cpu_temp():
        while True:
            COMPUTER.Hardware[0].Update()
            temps = []
            for a in range(0, len(COMPUTER.Hardware[0].Sensors)):
                # print(self.computer.Hardware[0].Sensors[a].Identifier)
                if "temperature" in str(COMPUTER.Hardware[0].Sensors[a].Identifier):
                    temps.append(COMPUTER.Hardware[0].Sensors[a].get_Value())
            try:
                cpu_temp = sum(temps) / len(temps)
                COMPONENTS_INFO["cpu_temp"]["message"] = f"Temp: {'%.1f' % cpu_temp}C"
            except TypeError:
                print(termcolor.colored("""Can't get access to CPU temperature. To see CPU temperature run program as admin
    Source: https://www.digitalcitizen.life/run-as-admin/\n""", "red"))
                COMPONENTS_INFO["cpu_temp"]["message"] = "Temp: None"
                break
            time.sleep(config.SLEEP_IN_SEC)


class GetGPUInfo:
    def __init__(self):
        threading._start_new_thread(self.get_gpu_usage, ())
        threading._start_new_thread(self.get_gpu_temp, ())
        threading._start_new_thread(self.get_gpu_memory_owned, ())
        self.get_gpu_memory_usage()

    @staticmethod
    def get_gpu_usage():
        while True:
            try:
                gpu_usage = GPUtil.showUtilization()
                COMPONENTS_INFO["gpu_usage"]["message"] = f"GPU - Using: {'%.1f' % float(gpu_usage.load * 100)}%"
            except UnboundLocalError:
                print(termcolor.colored("Can't find GPU\n", "red"))
                COMPONENTS_INFO["gpu_usage"]["message"] = "GPU - Using: None"
                break
            time.sleep(config.SLEEP_IN_SEC)

    @staticmethod
    def get_gpu_temp():
        while True:
            try:
                COMPUTER.Hardware[1].Update()
                gpu_temperature = COMPUTER.Hardware[1].Sensors[0].Value
                COMPONENTS_INFO["gpu_temp"]["message"] = f"Temp: {gpu_temperature}C"
            except UnboundLocalError:
                COMPONENTS_INFO["gpu_temp"]["message"] = "Temp: None"
            time.sleep(config.SLEEP_IN_SEC)

    @staticmethod
    def get_gpu_memory_owned():
        try:
            gpu_usage = GPUtil.showUtilization()
            COMPONENTS_INFO["gpu_memory_owned"]["message"] = f"GPU memory - Total: {'%.2f' % float(gpu_usage.memoryTotal / 1000)}GB"
        except UnboundLocalError:
            COMPONENTS_INFO["gpu_memory_owned"]["message"] = "GPU memory - Total: None"

    @staticmethod
    def get_gpu_memory_usage():
        while True:
            try:
                gpu_usage = GPUtil.showUtilization()
                COMPONENTS_INFO["gpu_memory_usage"]["message"] = f"Using: {'%.2f' % float(gpu_usage.memoryUsed / 1000)}GB ({'%.1f' % (float(gpu_usage.memoryUsed / gpu_usage.memoryTotal) * 100)}%)"
            except UnboundLocalError:
                COMPONENTS_INFO["gpu_memory_usage"]["message"] = "Using: None"
                break
            time.sleep(config.SLEEP_IN_SEC)


class GetRAMInfo:
    def __init__(self):
        threading._start_new_thread(self.get_owned_ram, ())
        self.get_ram_usage()

    @staticmethod
    def get_owned_ram():
        ram_usage_total = psutil.virtual_memory().total / 2 ** 30  # divide by 2**30 to convert to GB
        COMPONENTS_INFO["ram_owned"]["message"] = f"RAM - Total: {'%.1f' % ram_usage_total}GB"

    @staticmethod
    def get_ram_usage():
        while True:
            ram_usage = psutil.virtual_memory()  # divide by 2**30 to convert to GB
            COMPONENTS_INFO["ram_usage"]["message"] = f"Using: {'%.1f' % float(ram_usage.used / 2 ** 30)}GB ({ram_usage.percent}%)"
            time.sleep(config.SLEEP_IN_SEC)


class GetInternetInfo:
    def __init__(self):
        self.ip_server_to_pinging = "155.133.250.1"  # EU west CS-GO server
        self.old_internet_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        threading._start_new_thread(self.get_ping())
        self.get_internet_usage()

    def get_ping(self):
        while True:
            if config.SETTINGS_DATA["ping_function"]:
                ping_test = pythonping.ping(self.ip_server_to_pinging)
                if int(ping_test.rtt_max_ms) == 2000:
                    ping = "Internet proble"
                else:
                    ping = int(ping_test.rtt_avg_ms)
                COMPONENTS_INFO["ping"]["message"] = f"Ping: {ping}ms"
            else:
                COMPONENTS_INFO["ping"]["message"] = "Ping: OFF"
            time.sleep(config.SLEEP_IN_SEC)

    def get_internet_usage(self):
        while True:
            new_internet_usage = (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv)
            internet_usage = (new_internet_usage - self.old_internet_usage) / 1024 / 1024 * 8  # /1024/1024*8 to convert to Mb/s
            self.old_internet_usage = new_internet_usage
            COMPONENTS_INFO["internet_usage"]["message"] = f"Internet usage: {'%.2f' % internet_usage}Mb/s"
            time.sleep(config.SLEEP_IN_SEC)


class GetFPSInfo:
    def __init__(self):
        threading._start_new_thread(self.get_current_fps, ())
        self.get_average_fps()

    def get_current_fps(self):
        while True:
            fps = "soon"  # todo
            COMPONENTS_INFO["fps"]["message"] = f"FPS: {fps}"
            time.sleep(config.SLEEP_IN_SEC)

    def get_average_fps(self):
        while True:
            average_fps = "soon"  # todo
            COMPONENTS_INFO["fps_average"]["message"] = f"Average FPS: {average_fps}"
            time.sleep(config.SLEEP_IN_SEC)
