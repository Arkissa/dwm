#!/bin/python3

import os
import subprocess
import re


class MyVol:
    def __init__(self) -> None:
        self.this = "vol"
        self.dwm = os.environ["DWM"]
        self.s2d_reset = "^d^"
        # self.color = "^c#1A1A1A^^b#516FAB^"
        self.color = "^c#babbf1^^b#1a1b26^"
        self.signal = f"^s{self.this}^"

    def __str__(self) -> str:
        return self.this

    def update(self) -> tuple[str, str]:
        byte, _ = subprocess.Popen(
            ["/bin/pactl", "info"], stdout=subprocess.PIPE
        ).communicate()
        sink_stdout = byte.decode()
        sink_stdout = re.search("Default Sink: .*", sink_stdout)
        
        self.sink_stdout = sink_stdout \
                                .group() \
                                .replace("\n", "") \
                                .replace("Default Sink: ", "") \
                                .replace("\n", "") \
                                if sink_stdout is not None \
                                else ""

        byte, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f"pactl list sinks | grep {self.sink_stdout} -A 6 | sed -n '7p' | grep 'Mute: no'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()
        mute_stdout = byte.decode()

        byte, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f"pactl list sinks | grep {self.sink_stdout} -A 7 | sed -n '8p' | awk '{{printf int($5)}}'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()
        vol = int(byte.decode())
        self.num = vol
        self.vol, self.icon = (
            not mute_stdout
            and ("--", "ﱝ")
            or vol == 0
            and ("00" + "%", "婢")
            or vol < 10
            and ("0" + str(vol) + "%", "奄")
            or vol <= 50
            and (str(vol) + "%", "奔")
            or (str(vol) + "%", "墳")
        )

        text = f"{self.icon} {self.vol} "

        print(text)

        return (
            rf"{self.this} = .*$",
            f'{self.this} = ("{self.color}{self.signal}{text}{self.s2d_reset}", 6)\n'
        )

    def notify(self):
        byte, _ = subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f"pactl list sinks | grep '{self.sink_stdout}' -A 10 | grep 'Description: ' | awk -F 'Description: ' '{{print $2}}'",
            ],
            stdout=subprocess.PIPE,
        ).communicate()
        card_name = byte.decode().split("\n")[0]
        subprocess.Popen(
            [
                "/bin/bash",
                "-c",
                f"notify-send -r 9527 -h int:value:{self.num} -h string:hlcolor:#7F7FFF ' {card_name}[{self.icon} {self.vol}]'",
            ],
        )

    def click(self, mode):
        match mode:
            case "L":
                self.notify()
            case "M":
                subprocess.Popen(
                    ["/bin/bash", "-c", "pactl set-sink-mute @DEFAULT_SINK@ toggle"],
                )
            case "R":
                subprocess.Popen(
                    ["/bin/bash", "-c", "killall pavucontrol || pavucontrol &"],
                )
            case "U":
                subprocess.Popen(
                    ["/bin/bash", "-c", "pactl set-sink-volume @DEFAULT_SINK@ +5%"],
                )
                self.notify()
            case "D":
                subprocess.Popen(
                    ["/bin/bash", "-c", "pactl set-sink-volume @DEFAULT_SINK@ -5%"],
                )
                self.notify()

    def second(self) -> int:
        return 2

    def close(self) -> None:
        pass
