#!/bin/python3

import os
import subprocess
from datetime import datetime
import re


class MyDate:

    def __init__(self, *args) -> None:
        self.this = "date"
        self.dwm = os.environ['DWM']
        self.s2d_reset = "^d^"
        self.color = "^c#1A1A1A^^b#334466^"
        self.signal = f"^s{self.this}^"
        self.icon = {
            "01": "",
            "02": "",
            "03": "",
            "04": "",
            "05": "",
            "06": "",
            "07": "",
            "08": "",
            "09": "",
            "10": "",
            "11": "",
            "12": "",
        }

        match args[0]:
            case "update": self.update()
            case "notify": self.notify()
            case _: self.click(args[1])

    def update(self) -> None:
        now: datetime = datetime.now()
        self.time: str = now.strftime("%Y/%m/%d %H:%M:%S")
        minute = now.strftime("%I")

        text = f" {self.icon[minute]} {self.time} "

        print(text)
        with open(self.dwm + "/statusbar/tmp.py", "r+") as f:
            lines = f.readlines()
            tmp = []

            f.seek(0)
            for line in lines:
                _ = re.search(rf"{self.this} = .*$", line) or tmp.append(line)

            tmp.append(f"{self.this} = \"{self.color}{self.signal}{text}{self.s2d_reset}\"\n")
            f.truncate()
            f.writelines(tmp)

    def notify(self) -> None:
        self.update()
        subprocess.Popen([
            "/bin/bash", "-c",
            "notify-send \"  Calendar\" \"\n$(cal --color=always | sed 1,2d | sed 's/..7m/<b><span color=\"#4F5C80\">/;s/..27m/<\\/span><\\/b>/' )\" -r 9527"
        ],
                         stdout=subprocess.PIPE).communicate()

    def notify_todo(self) -> None:
        self.update()
        subprocess.Popen([
            "/bin/bash", "-c",
            "notify-send \" TODO\" \"\n$(cat ~/.todo.md | sed 's/\\(- \\[x\\] \\)\\(.*\\)/<span color=\"#ff79c6\">\\1<s>\\2<\\/s><\\/span>/' | sed 's/- \\[[ |x]\\] //')\" -r 9527"
        ],
                         stdout=subprocess.PIPE).communicate()

    def click(self, mode):
        match mode:
            case "L": self.notify()
            case "M":
                subprocess.Popen([
                    "/bin/bash", "-c",
                    "alacritty --class float -e nvim ~/.todo.md  &"
                ],
                                 stdout=subprocess.PIPE).communicate()
            case "R": self.notify_todo()
            case "U": pass
            case "D": pass
