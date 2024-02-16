#!/bin/python3

import os
import subprocess
import time
import calendar
import re


class MyDate:
    def __init__(self) -> None:
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
        self.weekday = ["一", "二", "三", "四", "五", "六", "日"]

    def __str__(self) -> str:
        return self.this

    def update(self) -> tuple[str, str]:
        now = time.localtime()
        t: str = f'{now.tm_hour}:{now.tm_min}  {self.weekday[now.tm_wday]} {time.strftime("%m", now)}/{now.tm_mday}'
        minute = time.strftime("%I", now)

        text = f"{self.icon[minute]} {t} "

        print(text)
        
        return (
            rf"{self.this} = .*$",
            f'{self.this} = ("{self.color}{self.signal}{text}{self.s2d_reset}", 1)\n'
        )

    def notify(self) -> None:
        now = time.localtime()
        cal = (
            calendar.month(now.tm_year, now.tm_mon)
            .replace(str(now.tm_year), "")
            .replace(str(now.tm_mday), f'<b><span color="#4F5C80">{now.tm_mday}</span></b>', 1)
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
                f"notify-send '  Calendar {now.tm_year}\n{'-' * 20}' '{' '*3}{cal}\n<b>{'-' * 20}</b>\n TODO\n{todo}' -r 9527",
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

    def second(self) -> int:
        return 1

    def close(self) -> None:
        pass
