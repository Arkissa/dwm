#!/bin/python3

import os
import subprocess


class MyLight:
    def __init__(self) -> None:
        self.this = "light"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        # self.color = "^c#1A1A1A^^b#516FAB^"
        self.color = "^c#babbf1^^b#1a1b26^"
        self.signal = f"^s{self.this}^"
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

    def __str__(self) -> str:
        return self.this

    def update(self) -> tuple[str, str]:

        byte, _ = subprocess.Popen(
            ["/bin/bash", "-c", "light | awk -F '.' '{print $1}'"],
            stdout=subprocess.PIPE,
        ).communicate()
        self.light = int(byte.decode())
        self.icon = self.map[int(self.light * 0.1)]

        text = f"{self.icon} {self.light}% "

        print(text)
        return (
            rf"{self.this} = .*$",
            f'{self.this} = ("{self.color}{self.signal}{text}{self.s2d_reset}", 5)\n'
        )

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

    def second(self) -> int:
        return 60

    def close(self) -> None:
        pass
