import os
from typing import ClassVar, Dict


class ConsoleUI:
    """A class for handling console UI elements and styling"""

    # ANSI Color Codes with Cyberpunk/Hacker theme
    NEON_PINK: ClassVar[str] = '\033[38;5;198m'
    NEON_GREEN: ClassVar[str] = '\033[38;5;46m'
    NEON_BLUE: ClassVar[str] = '\033[38;5;51m'
    ACID_GREEN: ClassVar[str] = '\033[38;5;118m'
    NEON_ORANGE: ClassVar[str] = '\033[38;5;208m'
    NEON_RED: ClassVar[str] = '\033[38;5;196m'
    RESET: ClassVar[str] = '\033[0m'
    BOLD: ClassVar[str] = '\033[1m'
    DIM: ClassVar[str] = '\033[2m'                   # For subtle effects
    BLINK: ClassVar[str] = '\033[5m'                 # For warning effects

    # Message style mapping with cyberpunk theme
    _STYLES: ClassVar[Dict[str, str]] = {
        "success": ACID_GREEN,
        "warning": NEON_ORANGE,
        "error": NEON_RED,
        "info": NEON_BLUE,
        "header": NEON_PINK
    }

    _SYMBOLS: ClassVar[Dict[str, str]] = {
        "+": "success",
        "*": "warning",
        "-": "error",
        "@": "info",
        "#": "header"
    }

    @classmethod
    def format_styled(cls, action: str, message: str = "") -> str:
        """
        Format a styled message with a cyberpunk indicator

        Args:
            action: Message type ("+", "*", "-", "@", "#") or style name
            message: The message to display

        Returns:
            str: Formatted message with color
        """
        if action in cls._STYLES:
            color = cls._STYLES[action]
        else:
            style_name = cls._SYMBOLS.get(action, "header")
            color = cls._STYLES[style_name]

        # Add blinking effect for errors and warnings
        if action in ["-", "*"] or action in ["error", "warning"]:
            indicator = f"{cls.BLINK}●{cls.RESET}"
        else:
            indicator = "●"

        return f"[{color}{indicator}{cls.RESET}] {color}{message}{cls.RESET}"

    @classmethod
    def display_banner(cls) -> None:
        """Display the welcome banner with ASCII art"""
        print(cls.NEON_GREEN + cls.BOLD + """
──────────────────████
─────────────────█░░███
─────────────────█░░████
──────────────────███▒██─────████████
────────████████─────█▒█──████▒▒▒▒▒▒████
──────███▒▒▒▒▒▒████████████░░████▒▒▒▒▒███
────██▒▒▒▒░▒▒████░░██░░░░██░░░░░█▒▒▒▒▒▒▒███
───██▒▒░░░░▒██░░░░░█▒░░░░░██▒░░░░░░░▒▒▒▒▒▒█
──██▒░░░░░▒░░░░░░░░░▒░░░░░░░▒▒░░░░░░░▒▒▒▒▒██
──█░░░░░░▒░░░██░░░░░░░░░░░░░██░░░░░░░░▒▒▒▒▒█
──█░░░░░░░░█▒▒███░░░░░░░░░█▒▒███░░░░░░░▒▒▒▒█
──█░░░░░░░████████░░░░░░░████████░░░░░░▒▒▒▒█
──█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒█
──██░░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░▒▒▒▒█
───█░░░░██░█░░░░░░░░░░░░░░░░░░░░░░░███▒▒▒▒▒█
───█▒▒░░░░█████░░░█░░░░██░░░██░░████░▒▒▒▒▒▒█
───██▒▒░░░░░█████████████████████░░░▒▒▒▒▒▒██
────██▒▒▒▒░░░░░██░░░███░░░██░░░█░░░▒▒▒▒▒▒██
─────███▒▒▒░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒█████
───────███▒▒▒▒▒▒░░░░░░░░░░░░░▒▒▒▒▒▒████
──────────██████████████████████████

╻ ╻┏━╸╻  ┏━╸┏━┓┏┳┓┏━╸   ╺┳╸┏━┓   ┏━┓┏━┓┏━┓┏┳┓┏┳┓┏━╸┏━┓
┃╻┃┣╸ ┃  ┃  ┃ ┃┃┃┃┣╸     ┃ ┃ ┃   ┗━┓┣━┛┣━┫┃┃┃┃┃┃┣╸ ┣┳┛
┗┻┛┗━╸┗━╸┗━╸┗━┛╹ ╹┗━╸    ╹ ┗━┛   ┗━┛╹  ╹ ╹╹ ╹╹ ╹┗━╸╹┗╸
""" + cls.RESET)

    @classmethod
    def display_heart(cls) -> None:
        """Display heart ASCII art"""
        print(cls.NEON_PINK + cls.BOLD + """
────────────────────▒
───────────────────░█
──────────────────███
─────────────────██ღ█
────────────────██ღ▒█──────▒█
───────────────██ღ░▒█───────██
───────────────█ღ░░ღ█──────█ღ▒█
──────────────█▒ღ░▒ღ░█───██░ღღ█
─────────────░█ღ▒░░▒ღ░████ღღღ█
─────░───────█▒ღ▒░░░▒ღღღ░ღღღ██─────░█
─────▓█─────░█ღ▒░░░░░░░▒░ღღ██─────▓█░
─────██─────█▒ღ░░░░░░░░░░ღ█────▓▓██
─────██────██ღ▒░░░░░░░░░ღ██─░██ღ▒█
────██ღ█──██ღ░▒░░░░░░░░░░ღ▓██▒ღღ█
────█ღღ▓██▓ღ░░░▒░░░░░░░░▒░ღღღ░░▓█
───██ღ▒▒ღღ░░ღღღღ░░▒░░░░ ღღღღ░░ღღღ██
───█ღ▒ღღ█████████ღღ▒░ღ██████████ღ▒█░
──██ღღ▒████████████ღღ████████████░ღ█▒
──█░ღღ████████████████████████████ღღ█
──█▒ღ██████████████████████████████ღ█
──██ღღ████████████████████████████ღ██
───██ღღ██████████████████████████ღ██
────░██ღღ██████████████████████ღღ██
──────▓██ღ▒██████████████████▒ღ██
─────░──░███ღ▒████████████▒ღ███
──────░░───▒██ღღ████████▒ღ██
─────────────▒██ღ██████ღ██
───────────────██ღ████ღ█
─────────────────█ღ██ღ█
──────────────────█ღღ█
──────────────────█ღ█░
───────────────────██░
""" + cls.RESET)

    @classmethod
    def display_menu(cls) -> None:
        """Display the main menu options"""
        print(cls.NEON_GREEN + """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ SMS                        ┃   1   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━┫
┃ Call                       ┃   2   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━┛
""" + cls.RESET)

    @staticmethod
    def clear_screen() -> None:
        """Clear the console screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
