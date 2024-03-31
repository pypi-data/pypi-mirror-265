from typing import Literal
from vinyl.lib.set_methods import AUTO_JOIN_DEFAULT_HOW as AUTO_JOIN_DEFAULT_HOW, MANUAL_JOIN_DEFAULT_HOW as MANUAL_JOIN_DEFAULT_HOW, base_join_type as base_join_type
from vinyl.lib.table import VinylTable as VinylTable

def join(left: VinylTable, right: VinylTable, *args, auto: bool = True, auto_allow_cross_join: bool = False, on: base_join_type | list[base_join_type] = [], how: Literal['inner', 'left', 'outer', 'right', 'semi', 'anti', 'any_inner', 'any_left', 'left_semi'] = None, lname: str = '', rname: str = '{name}_right', _how_override: bool = False) -> VinylTable:
    """
    Joins two or more tables together. if `on` is not provided and `auto` is True, the function will attempt to automatically join the tables (including multi-hop joins) based on the relationships defined in the vinyl field graph. If `on` is provided, the function will join the tables based on the provided predicates.

    If `how` is not provided, the function will default to a left join for successful auto joins and an inner join for manual joins. If `how` is provided, the function will use the specified join type. If the auto join fails, the function will raise an error unless `allow_cross_join` is set to True, in which case it will return the cross join.

    By default, all columns from the left and right tables will be included in the output. If you want to exclude columns from the right table, you can use the `select` method to select only the columns you want to keep. If there are duplicate column names in the left and right tables, lname and rname can be used to specify the suffixes to add to the column names from the left and right tables, respectively.
    """
def union(first: VinylTable, *rest: VinylTable, distinct: bool = False) -> VinylTable:
    """
    Compute the set union of multiple table expressions.

    Unlike the SQL UNION operator, this function allows for the union of tables with different schemas. If a column is present in one table but not in another, the column will be added to the other table with NULL values.

    If `distinct` is True, the result will contain only distinct rows. If `distinct` is False, the result will contain all rows from all tables, including duplicates.
    """
def difference(first: VinylTable, *rest: VinylTable, distinct: bool = False) -> VinylTable:
    """
    Compute the set difference of multiple table expressions.

    Unlike the SQL EXCEPT operator, this function allows for the difference of tables with different schemas. If a column is present in one table but not in another, the column will be added to the other table with NULL values.

    If `distinct` is True, the result will contain only distinct rows. If `distinct` is False, the result will contain all rows from the first table, including duplicates.
    """
def intersect(first: VinylTable, *rest: VinylTable, distinct: bool = True) -> VinylTable:
    """
    Compute the set intersection of multiple table expressions.

    Unlike the SQL INTERSECT operator, this function allows for the intersection of tables with different schemas. If a column is present in one table but not in another, the column will be added to the other table with NULL values.

    If `distinct` is True, the result will contain only distinct rows. If `distinct` is False, the result will contain all rows that are present in all tables, including duplicates.
    """
