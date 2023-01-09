#!/bin/python3

import os
import subprocess
import datetime
import re


class MyDate:
    def __init__(self, *args) -> None:
        self.this = "date"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        # self.color = "^c#1A1A1A^^b#516FAB^"
        self.color = "^c#babbf1^^b#1a1b26^"
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
            case "update":
                self.update()
            case "notify":
                self.notify()
            case _:
                self.click(args[1])

    def update(self) -> None:
        now = datetime.datetime.now()
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

            tmp.append(
                f'{self.this} = "{self.color}{self.signal}{text}{self.s2d_reset}"\n'
            )
            f.truncate()
            f.writelines(tmp)

    def notify(self) -> None:
        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f'notify-send "  Calendar\n{"-" * 20}" "$(cal --color=always | sed 1,2d | sed \'s/..7m/<b><span color="#4F5C80">/;s/..27m/<\\/span><\\/b>/\')\n<b>{"-" * 20}</b>\n TODO\n$(cat ~/.todo.md | sed \'s/\\(- \\[x\\] \\)\\(.*\\)/<span color="#ff79c6">\\1<s>\\2<\\/s><\\/span>/\' | sed \'s/- \\[[ |x]\\] //\')" -r 9527',
            ],
        )

    def todo(self):
        pid, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                "ps aux | grep 'st -t statusutil' | grep -v grep | awk '{print $2}'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()
        pid = pid != b"" and pid.decode() or ""

        x, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                "xdotool getmouselocation --shell | grep X= | sed 's/X=//'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()
        x = x != b"" and x.decode() or ""

        y, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                "xdotool getmouselocation --shell | grep Y= | sed 's/Y=//'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()
        y = y != b"" and y.decode() or ""

        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f"kill -9 {pid} || st -t statusutil_todo -g 50x15+$(({x} - 200))+$(({y} + 20)) -c noborder -e nvim ~/.todo.md ",
            ],
        )

    def click(self, mode):
        match mode:
            case "L":
                self.notify()
            case "R":
                self.todo()
