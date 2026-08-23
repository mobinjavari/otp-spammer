from .console import ConsoleUI


class Message:
    """A class for handling user interaction messages and prompts"""

    @staticmethod
    def prompt_refresh() -> None:
        """Prompt user to press enter to refresh the page"""
        input(ConsoleUI.format_styled("info", "Press enter to refresh the page "))

    @staticmethod
    def show_exit() -> str:
        """Display exit message"""
        return ConsoleUI.format_styled("error", "You exited the program! ")

    @staticmethod
    def show_success(message: str) -> str:
        """Display a success message"""
        return ConsoleUI.format_styled("success", message)

    @staticmethod
    def show_error(message: str) -> str:
        """Display an error message"""
        return ConsoleUI.format_styled("error", message)

    @staticmethod
    def show_warning(message: str) -> str:
        """Display a warning message"""
        return ConsoleUI.format_styled("warning", message)

    @staticmethod
    def show_info(message: str) -> str:
        """Display an info message"""
        return ConsoleUI.format_styled("info", message)

    @staticmethod
    def confirm_action(action: str) -> bool:
        """
        Ask user to confirm an action

        Args:
            action: The action to confirm

        Returns:
            bool: True if user confirms, False otherwise
        """
        response = input(ConsoleUI.format_styled("warning", f"{action} (Y/n): ")).lower()
        return response != 'n' and response != 'no'
