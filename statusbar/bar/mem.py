#!/bin/python3

import os
import subprocess
import psutil
import re


class MyMem:

    def __init__(self, *args) -> None:
        self.this = "mem"
        self.dwm = os.environ['DWM']
        self.s2d_reset = "^d^"
        self.color = "^c#1A1A1A^^b#334466^"
        self.signal = f"^s{self.this}^"

        match args[0]:
            case "update": self.update()
            case "notify": self.notify()
            case _: self.click(args[1])

    def update(self) -> None:
        self.icon = ""
        memory_info = psutil.virtual_memory()
        memory_total = round(memory_info.total / (1024 ** 3), 2)
        memory_used = round(memory_info.used / (1024 ** 3), 2)

        text = f" {self.icon} {memory_used}Gb/{memory_total}Gb "

        print(text)
        with open(self.dwm + "/statusbar/tmp.py", "r+") as f:
            lines = f.readlines()
            tmp = []

            f.seek(0)
            for line in lines:
                _ = re.search(rf"{self.this} = .*$", line) or tmp.append(line)

            tmp.append(f"{self.this} = \"{self.color}{self.signal}{text}|{self.s2d_reset}\"\n")
            f.truncate()
            f.writelines(tmp)

    def notify(self) -> None:
        self.update()
        subprocess.Popen([
            "/bin/bash", "-c",
            "notify-send \" Memory tops\" \"\n$(ps axch -o cmd:15,%mem --sort=-%mem | head)\" -r 9527"
        ],
                         stdout=subprocess.PIPE).communicate()

    def click(self, mode):
        match mode:
            case "L": self.notify()
            case "M": pass
            case "R":
                subprocess.Popen([
                    "/bin/bash", "-c",
                    "killall btop || alacritty --class noborder -e btop &"
                ], stdout=subprocess.PIPE).communicate()
            case "U": pass
            case "D": pass
