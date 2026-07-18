import datetime
import threading
from colorama import Fore, Style, init
import os

class Console:
    def __init__(self) -> None:
        init(autoreset=True)
        self.print_lock = threading.Lock()
        self.colors = {
            "green": Fore.GREEN,
            "red": Fore.RED,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
            "black": Fore.BLACK,
            "reset": Style.RESET_ALL,
            "lightblack": Fore.LIGHTBLACK_EX,
            "lightred": Fore.LIGHTRED_EX,
            "lightgreen": Fore.LIGHTGREEN_EX,
            "lightyellow": Fore.LIGHTYELLOW_EX,
            "lightblue": Fore.LIGHTBLUE_EX,
            "lightmagenta": Fore.LIGHTMAGENTA_EX,
            "lightcyan": Fore.LIGHTCYAN_EX,
            "lightwhite": Fore.LIGHTWHITE_EX
        }

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def timestamp(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def regened(self, message, obj=""):
        with self.print_lock:
            print(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors['lightblue']}REGENED {self.colors['lightblack']}•{self.colors['white']} {message} [{self.colors['lightblue']}{obj}{self.colors['white']}]{self.colors['reset']}")

    def success(self, message, obj=""):
        with self.print_lock:
            print(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors['lightgreen']}SUCCESS {self.colors['lightblack']}•{self.colors['white']} {message} [{self.colors['lightgreen']}{obj}{self.colors['white']}]{self.colors['reset']}")

    def discount(self, message, obj=""):
        with self.print_lock:
            print(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors['lightyellow']}DISCOUNT {self.colors['lightblack']}•{self.colors['white']} {message} [{self.colors['lightyellow']}{obj}{self.colors['white']}]{self.colors['reset']}")

    def revoked(self, message, obj=""):
        with self.print_lock:
            print(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors['lightgreen']}REVOKED {self.colors['lightblack']}•{self.colors['white']} {message} [{self.colors['lightgreen']}{obj}{self.colors['white']}]{self.colors['reset']}")

    def failed(self, message, obj=""):
        with self.print_lock:
            print(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors['lightred']}FAILED  {self.colors['lightblack']}•{self.colors['white']} {message} [{self.colors['lightred']}{obj}{self.colors['white']}]{self.colors['reset']}")

    def warning(self, message, obj=""):
        with self.print_lock:
            print(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors['lightyellow']}WARN    {self.colors['lightblack']}•{self.colors['white']} {message} [{self.colors['lightyellow']}{obj}{self.colors['white']}]{self.colors['reset']}")

    def info(self, message, obj=""):
        with self.print_lock:
            print(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors['lightblue']}INFO    {self.colors['lightblack']}•{self.colors['white']} {message} [{self.colors['lightblue']}{obj}{self.colors['white']}]{self.colors['reset']}")

    def custom(self, message, obj, color):
        with self.print_lock:
            print(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors[color.upper()]}{color.upper()} {self.colors['lightblack']}•{self.colors['white']} {message} [{self.colors[color.upper()]}{obj}{self.colors['white']}]{self.colors['reset']}")

    def input(self, message):
        with self.print_lock:
            return input(f"{self.colors['lightblack']}{self.timestamp()} » {self.colors['lightcyan']}INPUT   {self.colors['lightblack']}•{self.colors['white']} {message}{self.colors['reset']}")


