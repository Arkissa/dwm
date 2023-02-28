#!/bin/python3

import os
import subprocess
import datetime
import calendar
import re


class MyDate:
    def __init__(self, *args) -> None:
        self.this = "date"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
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
        self.time: str = f'{now.strftime("%R")}  {now.strftime("%m/%d")}'
        minute = now.strftime("%I")

        text = f"{self.icon[minute]} {self.time} "

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
        now = datetime.datetime.now()
        cal = (
            calendar.month(now.year, now.month)
            .replace(str(now.day), f'<b><span color="#4F5C80">{now.day}</span></b>', 1)
            .replace("\n", "\\n")
        )
        todo = ""
        home = os.environ["HOME"]
        with open(home + "/.todo.md") as f:
            r = re.compile(r"- \[x\].*")
            for i in f.readlines():
                i = i.replace("- [ ] ", "")
                todo += r.sub(
                    '<s><span color="#4F5C80">{}</span></s>'.format(
                        i.replace("\n", "").replace("- [x] ", "")
                    ),
                    i,
                )

        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f"notify-send '  Calendar\n{'-' * 20}' '{cal}\n<b>{'-' * 20}</b>\n TODO\n{todo}' -r 9527",
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
