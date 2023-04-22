#!/usr/bin/python3

class style():
    BOLD = '\033[1m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    UNSET = "UNSET"
    INFO = "INFO"
    ERROR = "ERROR"

    def format_color(type: str, text: str) -> str:
        match type:
            case style.INFO:
                return style.BOLD + text + style.RESET
            case style.ERROR:
                return style.RED + text + style.RESET
            case other:
                return text

    def printc(type: str, text: str) -> None:
        print(style.format_color(type, text))
