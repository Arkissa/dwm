#!/bin/python3

import os
import subprocess
import re


class MyBlues:
    def __init__(self, *args) -> None:
        self.this = "blues"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        # self.color = "^c#1A1A1A^^b#334466^"
        self.color = "^c#1A1A1A^^b#516FAB^"
        self.signal = f"^s{self.this}^"
        self.blues_status, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                "bluetoothctl show | grep 'Powered:' | awk -F ': ' '{print $2}'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()

        blues_name, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                "bluetoothctl info | grep 'Name:' | sed 's/^[\t]*//g' |awk -F ':' '{print $2}' | sed 's/^[ ]//g'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()
        self.blues_name = blues_name.decode().split("\n")[0]

        blues_mac, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                r"bluetoothctl info | grep '^Device ' | awk '{print $2}' |grep -E '\w+:\w+:\w+:\w+:\w+:\w+'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()
        self.blues_mac = blues_mac.decode().split("\n")[0]

        self.blues_type, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                "bluetoothctl info | grep 'Icon' | awk -F ': ' '{print $2}'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()

        blues_info, _ = subprocess.Popen(
            ["/bin/bash", "-c", "bluetoothctl info"], stdout=subprocess.PIPE
        ).communicate()
        self.blues_info = blues_info.decode().split("\n")[0]

        match args[0]:
            case "update":
                self.update()
            case "notify":
                self.notify()
            case _:
                self.click(args[1])

    def update(self) -> None:
        blues = [self.blues_status.decode() == "yes\n" and "" or ""]

        blues_type = (
            self.blues_type.decode() == "input-mouse\n"
            and ""
            or self.blues_type.decode() == "audio-headset\n"
            and ""
            or ""
        )

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

            tmp.append(
                f'{self.this} = "{self.color}{self.signal}{text}|{self.s2d_reset}"\n'
            )
            f.truncate()
            f.writelines(tmp)

    def notify(self) -> None:
        msg = (
            self.blues_info == "Missing device address argument"
            and "没有连接任何设备"
            or f"蓝牙名: {self.blues_name}{self.blues_bettery()}\nMAC: {self.blues_mac}"
        )

        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f"notify-send -r 9527 ' bluetooth' '{msg}'",
            ]
        )

    def blues_bettery(self):
        battery = subprocess.check_output(
            [
                "/bin/bash",
                "-c",
                f"upower -i /org/freedesktop/UPower/devices/headset_dev_{self.blues_mac.replace(':', '_')}",
            ]
        )
        battery = battery != b"" and battery.decode() or ""
        battery = re.findall(r"\w+%", battery)[0]

        return battery != "" and "\n电量: " + battery or ""

    def toggle(self):
        _ = (
            self.blues_status.decode() == "no\n"
            and subprocess.Popen(["/bin/bash", "-c", "bluetoothctl power on"])
            or subprocess.Popen(["/bin/bash", "-c", "bluetoothctl power off"])
        )

    def click(self, mode):
        match mode:
            case "L":
                self.notify()
            case "R":
                subprocess.Popen(
                    ["/bin/bash", "-c", "killall blueberry || blueberry &"],
                    stdout=subprocess.PIPE,
                ).communicate()
