#!/bin/python3

import os
import subprocess
import re


class MyLight:
    def __init__(self, *args) -> None:
        self.this = "light"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        # self.color = "^c#1A1A1A^^b#516FAB^"
        self.color = "^c#babbf1^^b#1a1b26^"
        self.signal = f"^s{self.this}^"
        self.handle()

        match args[0]:
            case "update":
                self.update()
            case "notify":
                self.notify()
            case _:
                self.click(args[1])

    def handle(self):
        self.map = {
            0: "",
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "",
        }

        byte, _ = subprocess.Popen(
            ["/bin/bash", "-c", "light | awk -F '.' '{print $1}'"],
            stdout=subprocess.PIPE,
        ).communicate()
        self.light = int(byte.decode())
        self.icon = self.map[int(self.light * 0.1)]

    def update(self) -> None:

        text = f"{self.icon} {self.light}% "

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
                f'notify-send -r 9527 -h int:value:{self.light} -h string:hlcolor:#7F7FFF " Screen light[{self.icon} {self.light}%]"',
            ]
        )

    def click(self, mode) -> None:
        match mode:
            case "L":
                self.notify()
            case "U":
                subprocess.Popen(
                    ["/bin/bash", "-c", "light -A 5"],
                )
                self.notify()
            case "D":
                subprocess.Popen(
                    ["/bin/bash", "-c", "light -U 5"],
                )
                self.notify()