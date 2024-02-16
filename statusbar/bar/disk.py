#!/bin/python3

import os
import subprocess
import psutil


class MyDisk:
    def __init__(self) -> None:
        self.this = "disk"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        self.color = "^c#babbf1^^b#1a1b26^"
        self.signal = f"^s{self.this}^"

    def __str__(self) -> str:
        return self.this

    def update(self) -> tuple[str, str]:
        disk_icon = ""
        disk = psutil.disk_usage("/")
        disk_percent = round(disk.percent)

        text = f"{disk_icon} {disk_percent}% "

        print(text)
        return (
            rf"{self.this} = .*$",
            f'{self.this} = ("{self.color}{self.signal}{text}{self.s2d_reset}", 4)\n'
        )

    def notify(self) -> None:
        disk = psutil.disk_usage("/")
        disk_io = psutil.disk_io_counters()
        if disk_io:
            disk_read = round(disk_io.read_bytes / (1024**3), 2)
            disk_write = round(disk_io.write_bytes / (1024**3), 2)
            disk_used = disk.used // (1024**3)
            disk_total = disk.total // (1024**3)
            disk_free = disk.free // (1024**3)
            disk_percent = round(disk.percent)

            subprocess.Popen(
                [
                    "/bin/bash",
                    "-c",
                    f'notify-send " Disk tops" "<p>使用率: {disk_percent}%</p><br><p>I/O: {disk_read}/{disk_write}Gb</p><br><p>容量: {disk_used}/{disk_total}Gb</p><br><p>可使用容量: {disk_free}Gb</p>" -r 9527',
                ],
            )
        else:
            subprocess.Popen(
                [
                    "/bin/bash",
                    "-c",
                    f'notify-send " Disk tops" "<p>Error in obtaining hard disk infomation</p>" -r 9527',
                ],
            )

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
                f"kill -9 {pid} || st -t statusutil_btop -g 140x25+$(({x} - 200))+$(({y} + 20)) -c noborder -e btop",
            ],
        )

    def click(self, mode):
        match mode:
            case "L":
                self.notify()
            case "R":
                self.btop()

    def second(self) -> int:
        return 60

    def close(self) -> None:
        pass
