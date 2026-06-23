"""
Three exercises on writing custom exceptions in Python.
Implement each class/function marked with TODO.

Run the tests test_exercises.py
"""



# ══════════════════════════════════════════════════════════════════
# EXERCISE 1 — Temperature Converter
# ══════════════════════════════════════════════════════════════════
#
# Build a temperature converter that raises domain-specific errors
# instead of generic ValueError / RuntimeError.
#
# Rules:
#   • Absolute zero is −273.15 °C (nothing can be colder).
#   • Only the scale strings "C", "F", and "K" are valid.
#   • A TemperatureError base class must exist so callers can
#     catch *all* temperature errors with a single except clause.
# ──────────────────────────────────────────────────────────────────


class TemperatureError(Exception):
    """Base exception for all temperature-related errors."""
    # TODO: no body needed — just `pass`
    pass


class BelowAbsoluteZeroError(TemperatureError):
    """
    Raised when a temperature value is below absolute zero.

    Attributes:
        value_celsius: The offending temperature in °C.
    """
    ABSOLUTE_ZERO_C = -273.15

    def __init__(self, value_celsius: float) -> None:
        # TODO: store value_celsius as an attribute and call super().__init__
        # with a message like:
        #   "-300 °C is below absolute zero (-273.15 °C)"
        self.value_celsius = value_celsius
        message = f"{value_celsius} °C is below absolute zero ({self.ABSOLUTE_ZERO_C} °C)"
        super().__init__(message)


class InvalidScaleError(TemperatureError):
    """
    Raised when an unrecognised temperature scale is supplied.

    Attributes:
        scale:           The invalid scale string the caller provided.
        valid_scales:    Tuple of accepted scale strings.
    """
    VALID_SCALES = ("C", "F", "K")

    def __init__(self, scale: str) -> None:
        # TODO: store scale and valid_scales as attributes and call super().__init__
        # with a message like:
        #   "Unknown scale 'X'; valid scales are: C, F, K"
        self.scale = scale
        self.valid_scales = self.VALID_SCALES
        message = f"Unknown scale '{scale}'; valid scales are: {', '.join(self.VALID_SCALES)}"
        super().__init__(message)


def convert_temperature(value: float, from_scale: str, to_scale: str) -> float:
    """
    Convert *value* from *from_scale* to *to_scale*.

    Raises:
        InvalidScaleError:      if either scale string is invalid.
        BelowAbsoluteZeroError: if the value is below absolute zero
                                (check after normalising to Celsius).

    Returns the converted value rounded to 4 decimal places.
    """
    # TODO: implement
    #   1. Validate both scales (raise InvalidScaleError for bad ones).
    #   2. Convert to Celsius first.
    #   3. Check against absolute zero (raise BelowAbsoluteZeroError if needed).
    #   4. Convert from Celsius to the target scale.
    #   5. Return the result rounded to 4 decimal places.
    if from_scale not in InvalidScaleError.VALID_SCALES:
        raise InvalidScaleError(from_scale)
    if to_scale not in InvalidScaleError.VALID_SCALES:
        raise InvalidScaleError(to_scale)
    
    # Conversion formulae:
    #   F → C : (F - 32) * 5/9
    #   K → C : K - 273.15
    #   C → F : C * 9/5 + 32
    #   C → K : C + 273.15

    # CELSJUSZA
    if from_scale == "C":
        c = value
    elif from_scale == "F":
        c = (value - 32) * 5 / 9


    if from_scale == "C":
        c = value
    elif from_scale == "F":
        c = 
    

# ══════════════════════════════════════════════════════════════════
# EXERCISE 2 — User Registry
# ══════════════════════════════════════════════════════════════════
#
# Build a simple in-memory user registry that maintains a dict of
# {username -> email}.  Operations must raise custom exceptions
# instead of KeyError / ValueError.
#
# Rules:
#   • Usernames are case-insensitive (store and look up as lowercase).
#   • A UserRegistryError base class must exist.
# ──────────────────────────────────────────────────────────────────


class UserRegistryError(Exception):
    """Base exception for the user registry."""


class UserAlreadyExistsError(UserRegistryError):
    """
    Raised when trying to register a username that is already taken.

    Attributes:
        username: The duplicate username (lowercase).
    """

    def __init__(self, username: str) -> None:
        # TODO: store username and call super().__init__ with a clear message
        raise NotImplementedError


class UserNotFoundError(UserRegistryError):
    """
    Raised when looking up a username that does not exist.

    Attributes:
        username: The username that was not found (lowercase).
    """

    def __init__(self, username: str) -> None:
        # TODO: store username and call super().__init__ with a clear message
        raise NotImplementedError


class UserRegistry:
    """In-memory registry mapping usernames to e-mail addresses."""

    def __init__(self) -> None:
        self._users: dict[str, str] = {}   # {lowercase_username: email}

    def register(self, username: str, email: str) -> None:
        """
        Add a new user.

        Raises:
            UserAlreadyExistsError: if *username* (case-insensitive) is taken.
        """
        # TODO: implement
        raise NotImplementedError

    def get_email(self, username: str) -> str:
        """
        Return the e-mail for *username*.

        Raises:
            UserNotFoundError: if *username* does not exist.
        """
        # TODO: implement
        raise NotImplementedError

    def delete(self, username: str) -> None:
        """
        Remove a user from the registry.

        Raises:
            UserNotFoundError: if *username* does not exist.
        """
        # TODO: implement
        raise NotImplementedError

    def list_users(self) -> list[str]:
        """Return a sorted list of all registered usernames (lowercase)."""
        # TODO: implement
        raise NotImplementedError


# ══════════════════════════════════════════════════════════════════
# EXERCISE 3 — Pipeline with Exception Chaining
# ══════════════════════════════════════════════════════════════════
#
# Implement a two-stage data pipeline:
#
#   Stage A — parse_record(raw: str) -> dict
#     Parses a comma-separated string "name,age,score" into a dict.
#
#   Stage B — process_record(record: dict) -> dict
#     Validates and processes the parsed dict:
#       • "name"  must be a non-empty string.
#       • "age"   must be an integer between 0 and 150 (inclusive).
#       • "score" must be a float between 0.0 and 100.0 (inclusive).
#     Returns {"name": str, "age": int, "score": float, "grade": str}
#     where grade is: A (≥90), B (≥75), C (≥60), D (≥45), F (<45).
#
#   Stage C — run_pipeline(raw: str) -> dict
#     Calls parse_record then process_record.
#     Wraps any ParseError or ProcessError in a PipelineError using
#     exception chaining (`raise PipelineError(...) from original`).
#
# Custom exceptions required:
#   PipelineError(Exception)     — base, holds .raw (original input)
#   ParseError(PipelineError)    — bad format; holds .raw
#   ProcessError(PipelineError)  — validation failure; holds .raw
#                                  and .field (which field failed)
# ──────────────────────────────────────────────────────────────────


class PipelineError(Exception):
    """
    Base exception for the data pipeline.

    Attributes:
        raw: The original raw input string that caused the failure.
    """

    def __init__(self, message: str, raw: str) -> None:
        # TODO: store raw and call super().__init__(message)
        raise NotImplementedError


class ParseError(PipelineError):
    """Raised when the raw string cannot be parsed into a record."""
    # No new __init__ needed — inherits from PipelineError.
    # TODO: just write `pass`


class ProcessError(PipelineError):
    """
    Raised when a parsed record fails validation.

    Attributes:
        raw:   The original raw input string.
        field: The name of the field that failed validation.
    """

    def __init__(self, message: str, raw: str, field: str) -> None:
        # TODO: store field and call super().__init__(message, raw)
        raise NotImplementedError


def parse_record(raw: str) -> dict:
    """
    Parse "name,age,score" into {"name": str, "age": str, "score": str}.

    Raises:
        ParseError: if the string does not have exactly three comma-separated
                    parts, or if age/score cannot be converted to their types.
    """
    # TODO: implement
    #   • Split on comma; raise ParseError if not exactly 3 parts.
    #   • Raise ParseError if age is not a valid integer.
    #   • Raise ParseError if score is not a valid float.
    #   • Return {"name": name_str, "age": age_int, "score": score_float}
    raise NotImplementedError


def process_record(record: dict, raw: str) -> dict:
    """
    Validate and enrich a parsed record.

    Raises:
        ProcessError: for any field that fails its validation rule.
    """
    # TODO: implement validation rules and grade assignment
    raise NotImplementedError


def run_pipeline(raw: str) -> dict:
    """
    Run parse_record → process_record.

    Raises:
        PipelineError: wrapping any ParseError or ProcessError,
                       using exception chaining.
    """
    # TODO: implement — remember to chain exceptions with `from`
    raise NotImplementedError
