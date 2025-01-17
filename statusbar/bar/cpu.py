#!/bin/python3

import os
import datetime
import subprocess
import psutil


class MyCpu:
    def __init__(self) -> None:
        self.this = "cpu"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        # self.color = "^c#1A1A1A^^b#516FAB^"
        self.color = "^c#babbf1^^b#1a1b26^"
        self.signal = f"^s{self.this}^"

    def __str__(self) -> str:
        return self.this

    def update(self) -> tuple[str, str]:
        cpu_icon = "閭"
        cpu_usage = psutil.cpu_percent()
        cpu = round(cpu_usage)
        temps_dict = psutil.sensors_temperatures()
        temps = int(temps_dict["acpitz"][0].current)

        temps_icon = (
            temps >= 85
            and ""
            or temps >= 70
            and ""
            or temps >= 60
            and ""
            or temps >= 50
            and ""
            or ""
        )

        cpu = cpu < 10 and f"{cpu_icon} 0{str(cpu)}%" or f"{cpu_icon} {str(cpu)}%"

        text = f"{temps_icon} {temps}°C {cpu} "

        print(text)
        return (
            rf"{self.this} = .*$",
            f'{self.this} = ("{self.color}{self.signal}{text}{self.s2d_reset}", 2)\n'
        )

    def notify(self) -> None:
        boot_time = psutil.boot_time()
        threads_count = 0
        process_count = 0
        for process in psutil.process_iter():
            threads_count += process.num_threads()
            process_count += 1

        speed = round(psutil.cpu_freq().current / 1000, 2)

        cpu_usage = round(psutil.cpu_percent())
        cpu_usage = cpu_usage < 10 and f"0{str(cpu_usage)}%" or f"{str(cpu_usage)}%"

        run_time = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
        days = run_time.days
        days = days < 10 and f"0{str(days)}" or days

        hours = run_time.seconds // 3600
        hours = hours < 10 and f"0{str(hours)}" or hours

        miuntes = (run_time.seconds % 3600) // 60
        miuntes = miuntes < 10 and f"0{miuntes}" or miuntes

        seconds = run_time.seconds % 60
        seconds = seconds < 10 and f"0{seconds}" or seconds

        uptime = f"{days}:{hours}:{miuntes}:{seconds}"

        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f'notify-send "閭 CPU tops" "<p>使用率: {cpu_usage}</p><br><p>速度: {speed}GHz</p><br><p>进程数: {process_count}</p><br><p>线程数: {threads_count}</p><br><p>运行时间: {uptime}</p>" -r 9527',
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
        return 5

    def close(self) -> None:
        pass
