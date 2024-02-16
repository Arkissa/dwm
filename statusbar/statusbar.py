#!/usr/bin/python3

import re
import os
from signal import signal, SIGINT
import sys
import time
import importlib
import subprocess
from typing import List, Protocol, Tuple, runtime_checkable
from abc import abstractmethod


@runtime_checkable
class Bar(Protocol):
    @abstractmethod
    def update(self) -> Tuple[str, str]:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

    @abstractmethod
    def click(self, mod: str) -> None:
        pass

    @abstractmethod
    def second(self) -> int:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class StatusBar:
    def __init__(self, args: list[str]) -> None:
        self.dwm = os.environ["DWM"]
        self.bars: List[Bar] = []
        for ts in map(lambda mod: (mod, filter(lambda s: s[1][0] != "_", dir(mod))),
                    map(lambda mod: importlib.import_module(f"bar.{mod}"),
                        map(lambda x: x[:-3],
                            filter(lambda x: x.endswith(".py"), os.listdir(self.dwm + "/statusbar/bar"))))):

            for obj in map(lambda m: m(),
                           filter(callable,
                                  map(lambda v: getattr(ts[0], v), ts[1]))):
                if isinstance(obj, Bar):
                    self.bars.append(obj)
        self.imp = False

        match args[0]:
            case "cron":
                self.cron()
            case "update":
                self.update(*args[1:])
                self.refresh()
            case "updateall" | "check":
                self.update(*map(lambda x: x.__str__(), self.bars))
                self.refresh()
            case _:
                self.click(*args)

    def cron(self) -> None:
        def handle(x, y) -> None:
            _, _ = x, y
            for bar in self.bars:
                bar.close()

        signal(SIGINT, handle)
        while True:
            try:
                for bar in self.bars:
                   if not time.localtime().tm_sec % bar.second():
                    for bar in filter(lambda bar: not time.localtime().tm_sec % bar.second(),
                                      self.bars):
                        
                       self.update(bar.__str__())

                self.refresh()
                time.sleep(0.1)
                self.imp = True
            except UnicodeDecodeError:
                os.remove(self.dwm + "/statusbar/tmp.py")
            except FileNotFoundError:
                open(self.dwm + "/statusbar/tmp.py", "w").close()
            except Exception as err:
                self.statusbar_log(err.__str__())

    def update(self, *args: str) -> None:
        for bar in [bar for bar in self.bars for name in args if bar.__str__() == name]:
            self.write_to_tmp(*bar.update())

    def refresh(self):
        try:
            tmp = importlib.import_module("tmp")
            if self.imp:
                importlib.reload(tmp)

            bar = "".join(map(lambda xs: xs[0],
                              sorted(map(lambda v: getattr(tmp, v),
                                         filter(lambda v: v[0] != "_",
                                                dir(tmp))), key=lambda k: k[1])))
            subprocess.Popen(
                [
                    "/bin/bash",
                    "-c",
                    f'xsetroot -name "{bar}"',
                ]
            )

        except Exception:
            self.check_tmp_content()

    def write_to_tmp(self, exp: str, data: str):
        with open(self.dwm + "/statusbar/tmp.py", "r+") as f:
            lines = f.readlines()
            tmp = []

            f.seek(0)
            for line in lines:
                _ = re.search(exp, line) or tmp.append(line)

            tmp.append(data)
            f.truncate()
            f.writelines(tmp)

    def check_tmp_content(self):
        self.write_to_tmp(r"^(cpu|mem|bat|vol|light|blues|date) = .*$", "")

    def statusbar_log(self, content):
        with open(self.dwm + "/statusbar/log", "w+") as log:
            log.write(content)

    def click(self, *args) -> None:
        if len(args) < 2:
            return

        self.update(args[0])
        for bar in self.bars:
            if bar.__str__() == args[0]:
                bar.click(args[1])
        self.refresh()


if __name__ == "__main__":
    StatusBar(sys.argv[1:])
