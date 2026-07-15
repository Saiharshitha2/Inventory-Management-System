"""
input_helpers.py
-----------------
Small helper functions to safely read and validate user input from
the console. Centralizing this logic avoids duplicated try/except
blocks throughout main.py and ensures consistent error messages for
invalid input.
"""

from display import print_error


def read_non_empty_string(prompt):
    """Keep asking until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print_error("Input cannot be empty. Please try again.")


def read_optional_string(prompt):
    """Read a string that may be left blank (used for 'update' fields)."""
    return input(prompt).strip()


def read_float(prompt, allow_blank=False):
    """Read a valid non-negative float. If allow_blank, empty input returns None."""
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            value = float(raw)
            if value < 0:
                print_error("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print_error("Invalid number. Please enter a valid price (e.g. 19.99).")


def read_int(prompt, allow_blank=False):
    """Read a valid non-negative integer. If allow_blank, empty input returns None."""
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            value = int(raw)
            if value < 0:
                print_error("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print_error("Invalid number. Please enter a whole number (e.g. 25).")


def read_menu_choice(prompt, valid_choices):
    """Read a menu choice and validate it's one of the valid_choices (strings)."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print_error(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}.")
