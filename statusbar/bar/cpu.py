#!/bin/python3

import os
import subprocess
import psutil
import re


class MyCpu:

    def __init__(self, *args) -> None:
        self.this = "cpu"
        self.dwm = os.environ['DWM']
        self.s2d_reset = "^d^"
        self.color = "^c#1A1A1A^^b#334466^"
        self.signal = f"^s{self.this}^"

        match args[0]:
            case "update": self.update()
            case "notify": self.notify()
            case _: self.click(args[1])

    def update(self) -> None:
        self.icon = "閭"
        cpu_usage = psutil.cpu_percent()
        cpu = round(cpu_usage)
        temps_dict = psutil.sensors_temperatures()
        temps = int(temps_dict["acpitz"][0].current)

        temps_icon = temps >= 85 and "" \
            or temps >= 70 and "" \
            or temps >= 60 and "" \
            or temps >= 50 and "" \
            or ""

        _ = temps >= 85 and subprocess.Popen([
            "/bin/bash", "-c",
            f"notify-send -r 9627 -u critical  \"温度过高: {temps_icon} {temps}°C\""
        ],
                         stdout=subprocess.PIPE).communicate()

        cpu = cpu < 10 and f"{self.icon} 0{str(cpu)}%" or f"{self.icon} {str(cpu)}%"

        text = f" {cpu} | {temps_icon} {temps}°C "

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
            "notify-send \"閭 CPU tops\" \"\n$(ps axch -o cmd:15,%cpu --sort=-%cpu | head)\\n\\n(100% per core)\" -r 9527"
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
