#!/bin/python3

import os
import subprocess
import re


class MyBlues:

    def __init__(self, *args) -> None:
        self.this = "blues"
        self.dwm = os.environ['DWM']
        self.s2d_reset = "^d^"
        self.color = "^c#1A1A1A^^b#334466^"
        self.signal = f"^s{self.this}^"
        self.blues_status, _ = subprocess.Popen([
            "/bin/bash", "-c",
            "bluetoothctl show | grep 'Powered:' | awk -F ': ' '{print $2}'"
        ],
                         stdout=subprocess.PIPE).communicate()

        self.blues_name, _ = subprocess.Popen([
            "/bin/bash", "-c",
            "bluetoothctl info | grep 'Name:' | sed 's/^[\t]*//g' |awk -F ':' '{print $2}' | sed 's/^[ ]//g'"
        ],
                         stdout=subprocess.PIPE).communicate()
        self.blues_name = self.blues_name.decode().split("\n")[0]

        self.blues_mac, _ = subprocess.Popen([
            "/bin/bash", "-c",
            r"bluetoothctl info | grep '^Device ' | awk '{print $2}' |grep -E '\w+:\w+:\w+:\w+:\w+:\w+'"
        ],
                         stdout=subprocess.PIPE).communicate()
        self.blues_mac = self.blues_mac.decode().split("\n")[0]

        self.blues_type, _ = subprocess.Popen([
            "/bin/bash", "-c",
            "bluetoothctl info | grep 'Icon' | awk -F ': ' '{print $2}'"
        ],
                         stdout=subprocess.PIPE).communicate()

        self.blues_info, _ = subprocess.Popen([
            "/bin/bash", "-c",
            "bluetoothctl info"
        ],
                         stdout=subprocess.PIPE).communicate()
        self.blues_info = self.blues_info.decode().split("\n")[0]

        match args[0]:
            case "update": self.update()
            case "notify": self.notify()
            case _: self.click(args[1])

    def update(self) -> None:
        blues = [self.blues_status.decode() == "yes\n" and "" or ""]

        blues_type = self.blues_type.decode() == "input-mouse\n" and "" \
            or self.blues_type.decode() == "audio-headset\n" and "" \
            or ""

        blues.append(blues_type)

        if self.blues_info == "Missing device address argument":
            self.blues_name = "--"
            blues = [""]

        blues_icon = " ".join(blues)

        text = f" {blues_icon} {self.blues_name} "

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
        msg = self.blues_info == "Missing device address argument" and "没有连接任何设备" \
            or f"蓝牙名: {self.blues_name}\nMAC: {self.blues_mac}"
        subprocess.Popen([
            "/bin/bash", "-c",
            f"notify-send -r 9527 ' bluetooth' '{msg}'"
        ],
                         stdout=subprocess.PIPE).communicate()

    def toggle(self):
        _ = self.blues_status.decode() == "no\n" and \
            subprocess.Popen([
                "/bin/bash", "-c",
                "bluetoothctl power on"
            ],
                             stdout=subprocess.PIPE).communicate() \
            or \
            subprocess.Popen([
                "/bin/bash", "-c",
                "bluetoothctl power off"
            ],
                             stdout=subprocess.PIPE).communicate()

    def click(self, mode):
        match mode:
            case "L": self.notify()
            case "M": self.toggle()
            case "R":
                subprocess.Popen([
                    "/bin/bash", "-c",
                    "killall blueberry || blueberry &"
                ], stdout=subprocess.PIPE).communicate()
            case "U": pass
            case "D": pass
