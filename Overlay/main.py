import tkinter as tk
import termcolor
import colorama
import config
import get_components_info


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

        get_components_info.GetDisplayData(self.display_label)

    def display_label(self, text, row, column, get_data_function):
        label = tk.Label(self.overlay, text=text, bg="gray30", fg=config.SETTINGS_DATA["font_color"],
                         font=("Comic Sans MS", config.SETTINGS_DATA["font_size"], "bold"))
        label.grid(row=row, column=column)
        label.after(config.SETTINGS_DATA["refresh"], get_data_function)
        label.after(config.SETTINGS_DATA["refresh"], label.destroy)


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

    DisplayOverlay()
    config.ROOT.mainloop()
