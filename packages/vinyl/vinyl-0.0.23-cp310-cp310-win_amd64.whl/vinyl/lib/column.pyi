from _typeshed import Incomplete
from collections.abc import Iterable, Sequence
from ibis.expr.datatypes import DataType as DataType
from ibis.expr.types import ArrayColumn, ArrayValue as ArrayValue, BooleanValue as BooleanValue, Column as Column, DateValue as DateValue, IntegerValue as IntegerValue, IntervalValue as IntervalValue, MapColumn as MapColumn, NumericValue as NumericValue, Scalar as Scalar, StringValue as StringValue, StructColumn as StructColumn, Value
from typing import Any, Callable, Literal

class VinylColumn:
    array: VinylColumn.ArrayFunctions
    math: VinylColumn.MathFunctions
    url: VinylColumn.URLFunctions
    re: VinylColumn.RegexFunctions
    str: VinylColumn.StringFunctions
    dict: VinylColumn.MapFunctions
    obj: VinylColumn.StructFunctions
    dt: VinylColumn.TemporalFunctions
    def __init__(self, _col: Column) -> None: ...
    def __abs__(self) -> VinylColumn: ...
    def __add__(self, other: Any) -> VinylColumn: ...
    def __and__(self, other: Any) -> VinylColumn: ...
    def __bool__(self) -> VinylColumn: ...
    def __ceil__(self) -> VinylColumn: ...
    def __cmp__(self, other: Any) -> VinylColumn: ...
    def __contains__(self, key: Any) -> VinylColumn: ...
    def __divmod__(self, other: Any) -> VinylColumn: ...
    def __eq__(self, other: Any) -> VinylColumn: ...
    def __float__(self) -> VinylColumn: ...
    def __floor__(self) -> VinylColumn: ...
    def __floordiv__(self, other: Any) -> VinylColumn: ...
    def __ge__(self, other: Any) -> VinylColumn: ...
    def __getitem__(self, key: Any) -> VinylColumn: ...
    def __gt__(self, other: Any) -> VinylColumn: ...
    def __hash__(self) -> VinylColumn: ...
    def __int__(self) -> VinylColumn: ...
    def __invert__(self) -> VinylColumn: ...
    def __iter__(self) -> VinylColumn: ...
    def __le__(self, other: Any) -> VinylColumn: ...
    def __len__(self) -> VinylColumn: ...
    def __lshift__(self, other: Any) -> VinylColumn: ...
    def __lt__(self, other: Any) -> VinylColumn: ...
    def __mod__(self, other: Any) -> VinylColumn: ...
    def __mul__(self, other: Any) -> VinylColumn: ...
    def __ne__(self, other: Any) -> VinylColumn: ...
    def __neg__(self) -> VinylColumn: ...
    def __next__(self) -> VinylColumn: ...
    def __nonzero__(self) -> VinylColumn: ...
    def __or__(self, other: Any) -> VinylColumn: ...
    def __pos__(self) -> VinylColumn: ...
    def __pow__(self, other: Any) -> VinylColumn: ...
    def __radd__(self, other: Any) -> VinylColumn: ...
    def __rand__(self, other: Any) -> VinylColumn: ...
    def __rdiv__(self, other: Any) -> VinylColumn: ...
    def __rdivmod__(self, other: Any) -> VinylColumn: ...
    def __rfloordiv__(self, other: Any) -> VinylColumn: ...
    def __rlshift__(self, other: Any) -> VinylColumn: ...
    def __rmul__(self, other: Any) -> VinylColumn: ...
    def __ror__(self, other: Any) -> VinylColumn: ...
    def __round__(self, ndigits: Any) -> VinylColumn: ...
    def __rpow__(self, other: Any) -> VinylColumn: ...
    def __rrshift__(self, other: Any) -> VinylColumn: ...
    def __rshift__(self, other: Any) -> VinylColumn: ...
    def __rsub__(self, other: Any) -> VinylColumn: ...
    def __rtruediv__(self, other: Any) -> VinylColumn: ...
    def __rxor__(self, other: Any) -> VinylColumn: ...
    def __sub__(self, other: Any) -> VinylColumn: ...
    def __truediv__(self, other: Any) -> VinylColumn: ...
    def __trunc__(self) -> int: ...
    def __xor__(self, other: Any) -> VinylColumn: ...
    def between(self, lower: Value, upper: Value) -> VinylColumn:
        """
        Check if this expression is between lower and upper, inclusive.
        """
    def match(self, case_pairs: list[tuple[BooleanValue, Value]], default: Value | None = None) -> Value:
        """
        Return a value based on the first matching condition in the expression. The default value is returned if no conditions are met, otherwise null is returned.
        """
    def cast(self, target_type: Any, try_: bool = False) -> Value:
        """
        Cast expression to indicated data type. Type inputs can include strings, python type annotations, numpy dtypes, pandas dtypes, and pyarrow dtypes.

        If try_ is True, then the cast will return null if the cast fails, otherwise it will raise an error.
        """
    def coalesce(self, *args: Value) -> Value:
        """
        Return the first non-null value in the expression list.
        """
    def hash(self) -> IntegerValue:
        """
        Compute an integer hash value of the expression.

        The hashing function used is dependent on the backend, so usage across dialect will likely return a different number.
        """
    def equivalent(self, other: Value) -> BooleanValue:
        """
        Null-aware version of ==. Returns true if both expressions are equal or both are null.
        """
    def isin(self, values: Value | Sequence[Value]) -> BooleanValue:
        """
        Check if this expression is in the provided set of values. Exists in place of the python `in` operator because of its requirement to evaluate to a python boolean.
        """
    def type(self, db_type: bool = True) -> DataType | IntegerValue:
        """
        Return the string name of the datatype of the expression.

        If db_type is True, then the string will be the name of the datatype in the specific backend (e.g. duckdb), otherwise it will be cross-dialect data type name from Vinyl.
        """
    def median(self, where: BooleanValue | None = None, approx: bool = False) -> Scalar:
        """
        Return the median value of the expression.

        If a `where` condition is specified, method only considers rows meeting the `where` condition.

        If `approx` is True, method will use the approximate median function, which is faster but less accurate.
        """
    def count(self, where: BooleanValue | None = None, distinct: bool = False, approx: bool = False) -> Scalar:
        """
        Return the number of non-null values in the expression, only including values when the `where` condition is true.

        If `distinct` is True, then the number of unique values will be returned instead of the total count.

        If `approx` is True and `distinct` is True, method will use approximate count distinct function, which is faster but less accurate. This is only available for count distinct.
        """
    def argmin(self, key: Value, where: BooleanValue | None = None) -> Scalar:
        """
        Return the value of key when the expression is at its minimum value.

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def argmax(self, key: Value, where: BooleanValue | None = None) -> Scalar:
        """
        Return the value of key when the expression is at its maximum value.

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def as_scalar(self) -> Scalar:
        """
        Convert the expression to a scalar value. Note that the execution of the scalar subquery will fail if the column expression contains more than one value.
        """
    def first(self, where: BooleanValue | None = None) -> Scalar:
        """
        Return the first value in the expression.

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def last(self, where: BooleanValue | None = None) -> Scalar:
        """
        Return the last value in the expression.

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def lag(self, offset: int | IntegerValue | None = None, default: Value | None = None) -> Scalar:
        """
        Return the row located at offset rows before the current row. If no row exists at offset, the default value is returned.
        """
    def lead(self, offset: int | IntegerValue | None = None, default: Value | None = None) -> Scalar:
        """
        Return the row located at offset rows after the current row. If no row exists at offset, the default value is returned.
        """
    def max(self, where: BooleanValue | None = None) -> Scalar:
        """
        Return the maximum value of the expression

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def min(self, where: BooleanValue | None = None) -> Scalar:
        """
        Return the minimum value of the expression

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def mode(self, where: BooleanValue | None = None) -> Scalar:
        """
        Return the mode value of the expression

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def nth(self, n: int | IntegerValue) -> Scalar:
        """
        Return the nth value of the expression
        """
    def quantile(self, quantiles: float | NumericValue | list[NumericValue | float], where: BooleanValue | None = None) -> Scalar:
        """
        Return value at the given quantile. If multiple quantiles are specified, then the output will be an array of values.

        The output of this method a discrete quantile if the input is an float, otherwise it is a continuous quantile.
        """
    def like(self, patterns: str | StringValue | Iterable[str | StringValue], case_sensitive: bool = True) -> BooleanValue:
        """
        This function is modeled after SQL's `LIKE` and `ILIKE` directives. Use `%` as a
        multiple-character wildcard or `_` as a single-character wildcard.

        For regular expressions, use `re.search`.
        """
    def combine(self, sep: str = ', ', where: Incomplete | None = None) -> Value:
        """
        Combine the expression into a single string using the specified separator.

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def collect(self, where: BooleanValue | None = None) -> ArrayColumn:
        """
        Collect the expression into an array.

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def sum(self, where: BooleanValue | None = None) -> VinylColumn:
        """
        Return the sum of the expression

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    def mean(self, where: BooleanValue | None = None) -> VinylColumn:
        """
        Return the mean of the expression

        If a `where` condition is specified, method only considers rows meeting the `where` condition.
        """
    class MathFunctions:
        def __init__(self, col: Column) -> None: ...
        def fabs(self) -> VinylColumn:
            """
            Return the absolute value of the expression.
            """
        def acos(self) -> VinylColumn:
            """
            Return the arc cosine of the expression.
            """
        def asin(self) -> VinylColumn:
            """
            Return the arc sine of the expression.
            """
        def atan(self) -> VinylColumn:
            """
            Return the arc tangent of the expression.
            """
        def atan2(self, other: NumericValue) -> VinylColumn:
            """
            Return the two-argument arc tangent of the expression.
            """
        def ceil(self) -> VinylColumn:
            """
            Return the smallest integer value not less than the expression.
            """
        def cos(self) -> VinylColumn:
            """
            Return the cosine of the expression.
            """
        def cot(self) -> VinylColumn:
            """
            Return the cotangent of the expression.
            """
        def degrees(self) -> VinylColumn:
            """
            Convert radians to degrees.
            """
        def exp(self) -> VinylColumn:
            """
            Return the expression raised to the power of e.
            """
        def floor(self) -> VinylColumn:
            """
            Return the largest integer value not greater than the expression.
            """
        def log(self, base: NumericValue | None = None) -> VinylColumn:
            """
            Return the logarithm of the expression. If base is specified, then the logarithm will be taken to that base. Otherwise, the natural logarithm is taken.
            """
        def log10(self) -> VinylColumn:
            """
            Return the base-10 logarithm of the expression.
            """
        def log2(self) -> VinylColumn:
            """
            Return the base-2 logarithm of the expression.
            """
        def radians(self) -> VinylColumn:
            """
            Convert degrees to radians.
            """
        def round(self, digits: int | IntegerValue | None = None) -> VinylColumn:
            """
            Round the expression to the specified number of decimal places. If digits is not specified, then the expression is rounded to the nearest integer.
            """
        def sign(self) -> VinylColumn:
            """
            Return the sign of the expression.
            """
        def sin(self) -> VinylColumn:
            """
            Return the sine of the expression.
            """
        def sqrt(self) -> VinylColumn:
            """
            Return the square root of the expression.
            """
        def tan(self) -> VinylColumn:
            """
            Return the tangent of the expression.
            """
        def copysign(self, other: NumericValue) -> VinylColumn:
            """
            Return the expression with the sign of the other expression.
            """
        def isclose(self, other: NumericValue, rel_tol: float = 1e-09, abs_tol: float = 0.0) -> VinylColumn:
            """
            Return True if the values are close to each other and False otherwise.
            """
        def isqrt(self) -> VinylColumn:
            """
            Return the integer square root of the expression.
            """
        def ldexp(self, other: NumericValue) -> VinylColumn:
            """
            Return the expression multiplied by 2 to the power of the other expression.
            """
        def modf(self) -> VinylColumn:
            """
            Return the fractional and integer parts of the expression.
            """
        def prod(self, *args: NumericValue) -> VinylColumn:
            """
            Return the product of the expression and the other expressions.
            """
        def remainder(self, other: int | IntegerValue) -> VinylColumn:
            """
            Return the remainder of the expression divided by the other expression.
            """
        def sumprod(self, other: NumericValue) -> VinylColumn:
            """
            Return the sum of the product of the expression and the other expression.
            """
        def trunc(self) -> VinylColumn:
            """
            Return the truncated value of the expression.
            """
        def cbrt(self) -> VinylColumn:
            """
            Return the cube root of the expression.
            """
        def exp2(self) -> VinylColumn:
            """
            Return 2 raised to the power of the expression.
            """
        def expm1(self) -> VinylColumn:
            """
            Return e raised to the power of the expression minus 1.
            """
        def pow(self, other: NumericValue) -> VinylColumn:
            """
            Return the expression raised to the power of the other expression.
            """
        def norm(self, type_: Literal['L1', 'L2'] = 'L2') -> VinylColumn:
            """
            Return the L2 norm of the expression.
            """
        def dist(self, other: NumericValue, type_: Literal['Euclidian', 'Manhattan', 'Cosine']) -> VinylColumn:
            """
            Return the distance between the expression and the other expression.
            """
        def acosh(self) -> VinylColumn:
            """
            Return the inverse hyperbolic cosine of the expression.
            """
        def asinh(self) -> VinylColumn:
            """
            Return the inverse hyperbolic sine of the expression.
            """
        def atanh(self) -> VinylColumn:
            """
            Return the inverse hyperbolic tangent of the expression.
            """
        def cosh(self) -> VinylColumn:
            """
            Return the hyperbolic cosine of the expression.
            """
        def sinh(self) -> VinylColumn:
            """
            Return the hyperbolic sine of the expression.
            """
        def tanh(self) -> VinylColumn:
            """
            Return the hyperbolic tangent of the expression.
            """
    class URLFunctions:
        def __init__(self, col: VinylColumn) -> None: ...
        def authority(self) -> VinylColumn:
            """
            Return the authority of the expression.
            """
        def file(self) -> VinylColumn:
            """
            Parse a URL and extract the file.
            """
        def fragment(self) -> VinylColumn:
            """
            Parse a URL and extract fragment identifier.
            """
        def host(self) -> VinylColumn:
            """
            Parse a URL and extract the host.
            """
        def path(self) -> VinylColumn:
            """
            Parse a URL and extract the path.
            """
        def protocol(self) -> VinylColumn:
            """
            Parse a URL and extract the protocol.
            """
        def query(self, key: str | StringValue | None = None) -> VinylColumn:
            """
            Parse a URL and extract the query string. If a key is specified, then the value of that key is returned. Otherwise, the entire query string is returned.
            """
        def userinfo(self) -> VinylColumn:
            """
            Parse a URL and extract the userinfo.
            """
    class RegexFunctions:
        def __init__(self, col: VinylColumn) -> None: ...
        def extract(self, pattern: str | StringValue, index: int | IntegerValue) -> VinylColumn:
            """
            Return the specified match at index from a regex pattern.

            The behavior of this function follows the behavior of Python’s match objects: when index is zero and there’s a match, return the entire match, otherwise return the content of the index-th match group.
            """
        def replace(self, pattern: str | StringValue, replacement: str | StringValue) -> VinylColumn:
            """
            Replace the matches of a regex pattern with a replacement string.
            """
        def search(self, pattern: str | StringValue) -> VinylColumn:
            """
            Returns True if the regex pattern matches a string and False otherwise.
            """
        def split(self, pattern: str | StringValue) -> VinylColumn:
            """
            Split the expression using a regex pattern.
            """
        def upper(self) -> VinylColumn:
            """
            Return a copy of the expression with all characters uppercased.
            """
    class StringFunctions:
        def __init__(self, col: VinylColumn) -> None: ...
        def ord(self) -> VinylColumn:
            """
            Return the unicode code point of the first character of the expression.
            """
        def capitalize(self) -> VinylColumn:
            """
            Return a copy of the expression with the first character capitalized and the rest lowercased.
            """
        def contains(self, substr: str | StringValue) -> VinylColumn:
            """
            Return True if the expression contains the substring and False otherwise.
            """
        def convert_base(self, from_base: IntegerValue, to_base: IntegerValue) -> VinylColumn:
            """
            Convert the expression from one base to another.
            """
        def endswith(self, end: str | StringValue) -> VinylColumn:
            """
            Return True if the expression ends with the specified suffix and False otherwise.
            """
        def find_in_set(self, str_list: list[str]) -> VinylColumn:
            """
            Return the position of the first occurrence of the expression in the list of strings.
            """
        def find(self, substr: str | StringValue, start: int | IntegerValue | None = None, end: int | IntegerValue | None = None) -> VinylColumn:
            """
            Return the position of the first occurrence of substring. Search is limited to the specified start and end positions, if provided. All indexes are 0-based.
            """
        def format(self, *args: Any, **kwargs: Any) -> VinylColumn:
            '''
            Return a formatted string using the expression as a format string.

            Note that only a subset of the python format string syntax is supported.
            ```
            *Supported*
            - {0}, {1}, .. {n} for args replacements
            - {key} for kwargs replacements

            **Not Supported**
            - conversion flags (e.g. "Harold\'s a clever {0\\!s}")
            - implicit references (e.g. "From {} to {}")
            - positional arguments / attributes (e.g. {0.weight} or {players[0]})
            ```
            '''
        def to_strptime(self, format: str | StringValue) -> VinylColumn:
            """
            Parse a string into a timestamp using the specified strptime format.
            """
        def hash(self, algorithm: Literal['md5', 'sha1', 'sha256', 'sha512'] = 'sha256', return_type: Literal['bytes', 'hex'] = 'hex') -> VinylColumn:
            """
            Return the hash of the expression using the specified algorithm.
            """
        def join(self, strings: list[str | StringValue]) -> VinylColumn:
            """
            Concatenate the elements of the list using the provided separator.
            """
        def len(self, substr: str | StringValue) -> VinylColumn:
            """
            Return the number of non-overlapping occurrences of substring in the expression.
            """
        def levenshtein(self, other: str | StringValue) -> VinylColumn:
            """
            Return the Levenshtein distance between the expression and the other string.
            """
        def lower(self) -> VinylColumn:
            """
            Return a copy of the expression with all characters lowercased.
            """
        def ljust(self, length: int | IntegerValue, fillchar: str | StringValue | None = ' ') -> VinylColumn:
            """
            Return the expression padded with the provided fill character to the specified length.
            """
        def lstrip(self) -> VinylColumn:
            """
            Return a copy of the expression with leading whitespace removed.

            Note: doesn't support removing specific characters like the standard library function.
            """
        def repeat(self, n: int | IntegerValue) -> VinylColumn:
            """
            Return the expression repeated `n` times.
            """
        def replace(self, pattern: str | StringValue, replacement: str | StringValue) -> VinylColumn:
            """
            Replace the matches of an exact (non-regex) pattern with a replacement string.
            """
        def rjust(self, length: int | IntegerValue, fillchar: str | StringValue | None = ' ') -> VinylColumn:
            """
            Return the expression padded with the provided fill character to the specified length.
            """
        def rstrip(self) -> VinylColumn:
            """
            Return a copy of the expression with trailing whitespace removed.

            Note: doesn't support removing specific characters like the standard library function.
            """
        def split(self, delimiter: str | StringValue) -> VinylColumn:
            """
            Split the expression using the specified delimiter.
            """
        def startswith(self, start: str | StringValue) -> VinylColumn:
            """
            Return True if the expression starts with the specified prefix and False otherwise.
            """
        def strip(self) -> VinylColumn:
            """
            Return a copy of the expression with leading and trailing whitespace removed.
            """
        def reverse(self) -> VinylColumn:
            """
            Return a copy of the expression with the characters reversed.
            """
        def center(self, width: int | IntegerValue, fillchar: str | StringValue | None = None) -> VinylColumn:
            """
            Return the expression centered in a string of length width. Padding is done using the specified fill character.
            """
        def substr(self, start: int | IntegerValue, length: int | IntegerValue | None = None) -> StringValue:
            """
            Return a substring of the expression starting at the specified index and optionally ending at the specified index.
            """
    class ArrayFunctions:
        def __init__(self, col: VinylColumn) -> None: ...
        def unnest(self) -> VinylColumn:
            """
            Unnest the array into a new table.

            Note: Rows with empty arrays are dropped in the output.
            """
        def join(self, sep: str) -> VinylColumn:
            """
            Concatenate the elements of the array using the provided separator.
            """
        def filter(self, predicate: Callable[[Value], bool] | BooleanValue) -> VinylColumn:
            """
            Return a new array containing only the elements of the original array for which the predicate is true.
            """
        def flatten(self) -> VinylColumn:
            """
            Remove one level of nesting from the array.
            """
        def index(self, value: Value) -> VinylColumn:
            """
            Return the position of the first occurrence of the value in the array.
            """
        def len(self) -> VinylColumn:
            """
            Return the length of the array.
            """
        def map(self, func: Callable[[Value], Value]) -> VinylColumn:
            """
            Apply the function to each element of the array.

            Note: also supports more complex callables like functools.partial and lambdas with closures
            """
        def remove(self, value: Value) -> VinylColumn:
            """
            Return a new array with all occurrences of the value removed. Note that in the python standard library, this method only removes the first occurrence.
            """
        def repeat(self, n: int | IntegerValue) -> VinylColumn:
            """
            Return the array repeated `n` times.
            """
        def sort(self) -> VinylColumn:
            """
            Return a new array with the elements sorted.
            """
        def union(self, other: ArrayColumn) -> VinylColumn:
            """
            Return a new array with the elements of both arrays, with duplicates removed.
            """
        def unique(self) -> VinylColumn:
            """
            Return a new array with the duplicate elements removed.
            """
        def zip(self, other: ArrayValue, *others: ArrayValue) -> VinylColumn:
            """
            Return a new array with the elements of the original array and the other arrays zipped together.

            The combined map will have f1, f2, f3, etc. as the keys.
            """
        def del_(self, index: int | IntegerValue) -> VinylColumn:
            """
            Remove the element at the specified index from the array.
            """
        def insert(self, index: int | IntegerValue, value: Value) -> VinylColumn:
            """
            Insert the value at the specified index in the array.
            """
        def max(self) -> VinylColumn:
            """
            Return the maximum value of the array
            """
        def min(self) -> VinylColumn:
            """
            Return the minimum value of the array
            """
    class MapFunctions:
        def __init__(self, col: VinylColumn) -> None: ...
        def contains(self, key: int | str | IntegerValue | StringValue) -> VinylColumn:
            """
            Return True if the map contains the specified key and False otherwise.
            """
        def get(self, key: Value, default: Value | None = None) -> VinylColumn:
            """
            Return the value of the specified key. If the key is not found, the default value is returned.
            """
        def keys(self) -> VinylColumn:
            """
            Return the keys of the map.
            """
        def len(self) -> VinylColumn:
            """
            Return the length of the map.
            """
        def values(self) -> VinylColumn:
            """
            Return the values of the map.
            """
    class StructFunctions:
        def __init__(self, col: VinylColumn) -> None: ...
        @property
        def fields(self) -> VinylColumn:
            """
            Return a mapping from the field name to the field type of the struct
            """
        @property
        def names(self) -> VinylColumn:
            """
            Return the names of the struct fields.
            """
        @property
        def types(self) -> VinylColumn:
            """
            Return the types of the struct fields.
            """
        def destructure(self) -> VinylColumn:
            """
            Destructure a StructValue into the corresponding struct fields.

            When assigned, a destruct value will be destructured and assigned to multiple columns.
            """
        def lift(self) -> VinylColumn:
            """
            Project the fields of self into a table.

            This method is useful when analyzing data that has deeply nested structs or arrays of structs. lift can be chained to avoid repeating column names and table references.
            """
    class TemporalFunctions:
        def __init__(self, col: VinylColumn) -> None: ...
        def extract(self, unit: Literal['year', 'quarter', 'month', 'week_of_year', 'day', 'day_of_year', 'hour', 'minute', 'second', 'microsecond', 'millisecond']) -> VinylColumn:
            """
            Extract the specified component from the datetime expression.
            """
        def floor(self, years: int | IntegerValue | None = None, quarters: int | IntegerValue | None = None, months: int | IntegerValue | None = None, weeks: int | IntegerValue | None = None, days: int | IntegerValue | None = None, hours: int | IntegerValue | None = None, minutes: int | IntegerValue | None = None, seconds: int | IntegerValue | None = None, milliseconds: int | IntegerValue | None = None, offset: IntervalValue | None = None) -> VinylColumn:
            """
            Round down the datetime expression to the specified unit. If an offset is specified, then the datetime will be rounded down to the nearest unit after the offset.

            If multiple units are specified, these will be combined together to form the unit. E.g. 1 quarter and 1 month will be transformed to 4 months.
            """
        def epoch_seconds(self) -> VinylColumn:
            """
            Return the number of seconds since the Unix epoch.
            """
        def strftime(self, format: str | StringValue) -> VinylColumn:
            """
            Format string may depend on the backend, but we try to conform to ANSI strftime.
            """
