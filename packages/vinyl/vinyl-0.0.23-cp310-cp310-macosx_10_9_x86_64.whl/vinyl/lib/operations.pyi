from _typeshed import Incomplete
from ibis.expr.types import BooleanValue as BooleanValue, Column as Column, IntegerColumn as IntegerColumn, IntegerValue as IntegerValue, Value as Value
from typing import Any

def case(pairs: list[tuple[BooleanValue, Value]], default: Value | None = None) -> Value:
    """
    Returns the first value for which the corresponding condition is true. If no conditions are true, return the default.

    Conditions should be specified as a list of tuples, where the first element of each tuple is a boolean expression and the second element is the value to return if the condition is true.
    """
def if_else(condition: Any, true_value: Any | None, false_value: Any | None) -> Value:
    """
    Constructs a conditional expression. If the condition is true, return the true_value; otherwise, return the false_value.

    Can be chained together by making the true_value or false_value another if_else expression.
    """
def coalesce(*exprs) -> Value:
    """
    Return the first non-null value in the expression list.
    """
def least(*args: Any) -> Value:
    """
    Return the smallest value among the supplied arguments.
    """
def greatest(*args: Any) -> Value:
    """
    Return the largest value among the supplied arguments.
    """
def row_number() -> IntegerColumn:
    """
    Returns the current row number.

    This function is normalized across backends to start from 0.
    """
def rank(dense: bool = False) -> IntegerColumn:
    """
    Compute position of first element within each equal-value group in sorted order.

    If `dense` don't skip records after ties. See [here](https://learnsql.com/cookbook/whats-the-difference-between-rank-and-dense_rank-in-sql/) for a good primer on the difference.

    """
def percent_rank() -> Column:
    """
    Compute the relative rank of a value within a group of values.
    """
def ntile(n: int | IntegerValue) -> IntegerColumn:
    """
    Divide the rows into `n` buckets, assigning a bucket number to each row.
    """

case: Incomplete
if_else: Incomplete
coalesce: Incomplete
least: Incomplete
greatest: Incomplete
row_number: Incomplete
rank: Incomplete
percent_rank: Incomplete
ntile: Incomplete
