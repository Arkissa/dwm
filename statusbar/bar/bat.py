#!/bin/python3

import os
import subprocess
import re


class MyBat:
    def __init__(self, *args) -> None:
        self.this = "bat"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        self.color = "^c#1A1A1A^^b#334467^"
        self.signal = f"^s{self.this}^"
        self.bat = {
            0: "",
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "",
        }
        byte, _ = subprocess.Popen(
            ["/bin/acpi", "-b"], stdout=subprocess.PIPE
        ).communicate()
        stdout = byte.decode()
        stdout = stdout.replace("Battery 0: ", "")
        stdout = re.sub(r"\w+$", "", stdout, re.I)
        stdout = stdout.split("\n")[0].split(",")

        _ = len(stdout) < 3 and stdout.append("")

        self.status, self.remaining, self.time = stdout
        find = re.search(r"\d+:\d+:\d+", self.time)
        self.time = find and find.group() or ""
        remaining = self.remaining.split("%")[0]

        remaining = int(int(remaining) * 0.1)
        charge_icon = self.status != "Discharging" and remaining < 9 and "ﮣ" or ""
        self.icon = charge_icon + self.bat[remaining]

        match args[0]:
            case "update":
                self.update()
            case "notify":
                self.notify()
            case _:
                self.click(args[1])

    def update(self) -> None:

        text = f" {self.icon}{self.remaining:4} "

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
        remaining: str = (
            self.status != "Full" and "\n剩余: " + self.icon + self.remaining or ""
        )
        time: str = self.time and f"\n可用时间: {self.time}" or ""

        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f"notify-send -r 9527 \"  Battery\n{'-' * 20}\" \"<p>状态: {self.status}{remaining}{time}</p>\"",
            ]
        ).communicate()

    def click(self, mode) -> None:
        match mode:
            case "L":
                self.notify()
            case "R":
                subprocess.Popen(
                    [
                        "/bin/bash",
                        "-c",
                        "killall mate-power-preferences || mate-power-preferences",
                    ],
                ).communicate()
