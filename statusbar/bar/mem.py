#!/bin/python3

import os
import subprocess
import psutil
import re


class MyMem:
    def __init__(self, *args) -> None:
        self.this = "mem"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        # self.color = "^c#1A1A1A^^b#516FAB^"
        self.color = "^c#babbf1^^b#1a1b26^"
        self.signal = f"^s{self.this}^"

        match args[0]:
            case "update":
                self.update()
            case "notify":
                self.notify()
            case _:
                self.click(args[1])

    def update(self) -> None:
        self.icon = ""
        memory_info = psutil.virtual_memory()

        memory_percent = round(memory_info.percent)
        memory_percent = (
            memory_percent < 10 and f"0{str(memory_percent)}" or memory_percent
        )

        text = f" {self.icon} {memory_percent}% "

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
        self.update()
        memory_info = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()

        memory_total = f"{self.convert(memory_info.total)}Gb"
        memory_used = f"{self.convert(memory_info.used)}"
        memory_available = f"{self.convert(memory_info.available)}Gb"
        memory_buffers = f"{self.convert(memory_info.buffers)}Gb"
        memory_cached = f"{self.convert(memory_info.cached)}Gb"
        memory_inactive = f"{self.convert(memory_info.inactive)}Gb"
        swap_used = f"{self.convert(swap_memory.used)}"
        swap_total = f"{self.convert(swap_memory.total)}Gb"

        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f'notify-send " Memory tops" "已用内存: {memory_used}/{memory_total}\n可用内存: {memory_available}\n已缓存文件: {memory_buffers}\n已保留内存: {memory_inactive}\n已缓存: {memory_cached}\nSWAP: {swap_used}/{swap_total}" -r 9527',
            ],
        )

    def convert(self, num):
        return round(num / (1024**3), 2)

    def btop(self):
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
                f"kill -9 {pid} || st -t statusutil_btop -g 82x25+$(({x} - 200))+$(({y} + 20)) -c noborder -e btop",
            ],
        )

    def click(self, mode):
        match mode:
            case "L":
                self.notify()
            case "R":
                self.btop()
