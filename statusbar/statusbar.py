#!/usr/bin/python3

import re
import os
import sys
import time
import importlib
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
        self.dwm = os.environ["DWM"]
        self.imp = False

        if args[0] == "cron":
            self.cron()
        elif args[0] == "update":
            self.update(*args[1:])
            self.refresh()
        elif args[0] == "updateall" or args[0] == "check":
            self.update("bat", "vol", "date", "cpu", "mem", "blues", "light")
            self.refresh()
        else:
            self.click(args[0], args[1])

    def cron(self) -> None:
        while True:
            try:
                t: float = time.time()
                f: time.struct_time = time.gmtime(t)
                run: int = int(time.strftime("%S", f))

                _ = not run % 2 and self.update("bat")
                _ = not run % 2 and self.update("vol")
                _ = not run % 5 and self.update("cpu")
                _ = not run % 5 and self.update("mem")
                _ = not run % 2 and self.update("light")
                _ = not run % 2 and self.update("blues")
                _ = not run % 1 and self.update("date")

                self.refresh()
                time.sleep(1)
                self.imp = True
            except FileNotFoundError:
                open(self.dwm + "/statusbar/tmp.py", "w").close()
            except Exception as err:
                self.statusbar_log(err.__str__())

    def update(self, *args) -> None:
        if len(args) < 1:
            return

        print("update", *args, end=" ")
        getattr(self.map[args[0]][0], self.map[args[0]][1])("update")
        args = args[1:]

        _ = args and self.update(*args)

    def refresh(self):
        try:
            tmp = importlib.import_module("tmp")
            _ = self.imp and importlib.reload(tmp)
            subprocess.Popen(
                [
                    "/bin/bash",
                    "-c",
                    f'xsetroot -name "{tmp.date}{tmp.cpu}{tmp.mem}{tmp.light}{tmp.vol}{tmp.blues}{tmp.bat:10}"',
                ]
            )

        except Exception:
            self.check_tmp_content()

    def check_tmp_content(self):
        with open(self.dwm + "/statusbar/tmp.py", "r+") as f:
            lines = f.readlines()
            t = []

            f.seek(0)
            for i in lines:
                if not re.search(r"^(cpu|mem|bat|vol|light|blues|date) = .*$", i):
                    continue
                t.append(i)
            f.truncate()
            f.writelines(t)

    def statusbar_log(self, content):
        with open(self.dwm + "/statusbar/log", "w+") as log:
            log.write(content)

    def click(self, *args) -> None:
        if len(args) < 2:
            return
        getattr(self.map[args[0]][0], self.map[args[0]][1])("click", args[1])
        self.update(args[0])
        self.refresh()


status_bar(sys.argv[1:])
