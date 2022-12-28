#!/bin/python3

import threading
import sys
import time
import subprocess
from bar import bat
from bar import vol
from bar import date
from bar import cpu
from bar import mem
from bar import blues
from bar import light


class status_bar:

    def __init__(self, args: list[str]) -> None:
        self.map: dict = {
            "bat": (bat, "MyBat"),
            "vol": (vol, "MyVol"),
            "date": (date, "MyDate"),
            "cpu": (cpu, "MyCpu"),
            "mem": (mem, "MyMem"),
            "blues": (blues, "MyBlues"),
            "light": (light, "MyLight"),
        }

        if args[0] == "cron":
            threading.Thread(target=self.cron).start()
        elif args[0] == "update":
            self.update(*args[1:])
            self.refresh()
        elif args[0] == "updateall" or args[0] == "check":
            self.update("bat", "vol", "date", "cpu", "mem", "blues", "light")
            self.refresh()
        else:
            self.click(args[0], args[1])
            self.refresh()

    def cron(self) -> None:
        while True:
            t: float = time.time()
            f: time.struct_time = time.gmtime(t)
            run: int = int(time.strftime("%S", f))

            _ = not run % 5                 \
                and self.update("bat")      \
                and self.update("vol")      \
                and self.update("cpu")      \
                and self.update("mem")      \
                and self.update("light")    \
                and self.update("blues")

            _ = not run % 1 and self.update("date")

            time.sleep(1)

    def update(self, *args) -> None:
        if len(args) < 1:
            return

        print("update", *args, end=" ")
        getattr(self.map[args[0]][0], self.map[args[0]][1])("update")
        args = args[1:]
        self.update(*args)

    def refresh(self):
        import tmp
        subprocess.Popen([
            "/bin/bash", "-c",
            f"xsetroot -name \"{tmp.cpu}{tmp.mem}{tmp.light}{tmp.vol}{tmp.blues}{tmp.bat}{tmp.date}\""
        ])

    def click(self, *args) -> None:
        if len(args) < 2:
            return
        getattr(self.map[args[0]][0], self.map[args[0]][1])("click", args[1])


status_bar(sys.argv[1:])
