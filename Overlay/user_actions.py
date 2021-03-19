import tkinter as tk
import termcolor
import sys
import webbrowser
import json
import recorder
import config


def get_user_input():
    commands = {"help": send_help_command,
                "q": quit_from_program,
                "fs": change_font_size,
                "fc": change_font_color,
                "ref": change_refresh_time,
                "ping": ping_label_switch,
                "record": recorder.Recorder}
    while True:
        commend = input("Write command (help to get commands list, q to quit program) --> ")
        try:
            commands[commend]()
        except KeyError:
            pass


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


def quit_from_program():
    input("\nThanks for using my program. Hope you liked it! Click enter to close program")
    config.ROOT.quit()
    sys.exit()


def change_font_size():
    while True:
        try:
            new_font_size = int(input(f"Current font size: {config.SETTINGS_DATA['font_size']}\nWrite new font_size: "))
            break
        except ValueError:
            print(termcolor.colored("You have to write number like 10", "red"))
    if new_font_size > 25:
        new_font_size = 25
        print(termcolor.colored("Max font size is 25", "red"))
    elif new_font_size < 5:
        new_font_size = 5
        print(termcolor.colored("Minimum font size is 5", "red"))
    config.SETTINGS_DATA["font_size"] = new_font_size
    print(termcolor.colored(f"New font size is {new_font_size}\n", "yellow"))
    save()


def change_font_color():
    while True:
        try:
            new_color = input(
                f"Current color: {config.SETTINGS_DATA['font_color']}\nWrite new color\nIf you want see all available colors write 1: ")
            if new_color == "1":
                webbrowser.open(
                    "http://www.science.smith.edu/dftwiki/images/thumb/3/3d/TkInterColorCharts.png/800px-TkInterColorCharts.png")
            else:
                test_label = tk.Label(fg=new_color)
                break
        except tk.TclError:
            print(termcolor.colored("Wrong color", "red"))
    config.SETTINGS_DATA["font_color"] = new_color
    print(termcolor.colored(f"New color is {new_color}\n", "yellow"))
    save()


def change_refresh_time():
    while True:
        try:
            new_refresh_time = float(
                input(
                    f"Current refresh time: {config.SETTINGS_DATA['refresh'] / 1000}\nWrite new refresh time (in sec): "))
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
    config.SETTINGS_DATA["refresh"] = int(new_refresh_time)
    print(termcolor.colored(f"New refresh time is {new_refresh_time / 1000}sec\n", "yellow"))
    save()


def ping_label_switch():
    if config.SETTINGS_DATA["ping_function"]:
        print(termcolor.colored("Ping label is now disabled", "yellow"))
        config.SETTINGS_DATA["ping_function"] = False
    else:
        print(termcolor.colored("Ping label is now enabled", "yellow"))
        config.SETTINGS_DATA["ping_function"] = True
    save()


def save():
    with open("data//settings.json", "w") as file:
        json.dump(config.SETTINGS_DATA, file)
