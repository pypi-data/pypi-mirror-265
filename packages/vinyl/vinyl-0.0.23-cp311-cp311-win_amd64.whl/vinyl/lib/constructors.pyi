from _typeshed import Incomplete
from ibis.expr.datatypes import DataType as DataType
from ibis.expr.types import DateValue as DateValue, NumericValue as NumericValue, TimestampValue as TimestampValue
from typing import Any
from vinyl.lib.column import VinylColumn as VinylColumn

def literal(value, type: Incomplete | None = None):
    """
    Create a scalar expression from a Python value.
    """
def random() -> NumericValue:
    """
    Generate a random float between 0 inclusive and 1 exclusive.

    Similar to random.random in the Python standard library.
    """
def now() -> VinylColumn:
    """
    Get the current timestamp.
    """
def date(year: int, month: int | None = None, day: int | None = None) -> DateValue:
    """
    Create a date scalar expression from year, month, and day.

    Alternatively, you can create a date directly from the python standard library datetime using datetime.date()
    """
def time(hour: str, minute: str | None = None, second: str | None = None) -> TimestampValue:
    """
    Create a time scalar expression from hour, minute, and second.

    Alternatively, you can create a time directly from the python standard library datetime using datetime.time().
    """
def timestamp(year: str | None = None, month: str | None = None, day: str | None = None, hour: str | None = None, minute: str | None = None, second: str | None = None, timezone: str | None = None) -> TimestampValue:
    """
    Create a timestamp scalar expression from year, month, day, hour, minute, and second.

    Specify a timezone to create a timestamp with timezone. If no timezone is specified, the timestamp will be timezone naive.
    """
def interval(years: int | None = None, quarters: int | None = None, months: int | None = None, weeks: int | None = None, days: int | None = None, hours: int | None = None, minutes: int | None = None, seconds: int | None = None, milliseconds: int | None = None, microseconds: int | None = None) -> TimestampValue:
    """
    Create an interval scalar expression from years, months, weeks, days, hours, minutes, and seconds.
    """
def map(map: dict[Any, Any]):
    """
    Create a map scalar expression from a Python dictionary.
    """
def struct(struct: dict[str, Any], type: str | DataType | None = None):
    """
    Create a struct scalar expression from a Python dictionary.

    Optionally, you can specify a type for the struct. Otherwise, the type will be inferred
    """

literal: Incomplete
random: Incomplete
now: Incomplete
date: Incomplete
time: Incomplete
timestamp: Incomplete
interval: Incomplete
map: Incomplete
struct: Incomplete
