#!/bin/python3

import os
import subprocess
import re


class MyBat:
    def __init__(self) -> None:
        self.this = "bat"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        self.color = "^c#babbf1^^b#1a1b26^"
        # self.color = "^c#1A1A1A^^b#516FAB^"
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

    def __str__(self) -> str:
        return self.this

    def update(self) -> tuple[str, str]:
        byte, _ = subprocess.Popen(
            ["/bin/acpi", "-b"], stdout=subprocess.PIPE
        ).communicate()
        stdout = byte.decode()
        stdout = stdout.replace("Battery 0: ", "")
        stdout = re.sub(r"\w+$", "", stdout, re.I)
        stdout = stdout.split("\n")[0].split(",")

        if len(stdout) < 3:
            stdout.append("")

        self.status, \
        self.remaining, \
        self.time = stdout

        find = re.search(r"\d+:\d+:\d+", self.time)
        self.time = find.group() if find else ""
        remaining = self.remaining.split("%")[0]

        remaining = int(int(remaining) * 0.1)
        charge_icon = "ﮣ" if self.status not in ("Discharging", "Full") else ""
        self.icon = charge_icon + self.bat[remaining]

        text = f"{self.icon}{self.remaining:4} "

        print(text)
        return (
            rf"{self.this} = .*$",
            f'{self.this} = ("{self.color}{self.signal}{text}{self.s2d_reset}", 8)\n'
        )

    def notify(self) -> None:
        time: str = self.time and f"\n可用时间: {self.time}" or ""

        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f'notify-send -r 9527 "  Battery[{self.icon}{self.remaining}]" "<p>状态: {self.status}{time}</p>"',
            ]
        )

    def click(self, mode: str) -> None:
        match mode:
            case "L":
                self.notify()
            case "M":
                subprocess.Popen(
                    [
                        "/bin/bash",
                        "-c",
                        "~/.config/rofi/bin/powermenu",
                    ],
                ).communicate()
            case "R":
                subprocess.Popen(
                    [
                        "/bin/bash",
                        "-c",
                        "killall xfce4-power-manager-settings || xfce4-power-manager-settings",
                    ],
                ).communicate()

    def second(self) -> int:
        return 2

    def close(self) -> None:
        pass
