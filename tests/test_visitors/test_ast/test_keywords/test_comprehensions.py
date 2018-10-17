# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyForsInComprehensionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultipleIfsInComprehensionViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import (
    WrongListComprehensionVisitor,
)

# Lists:

list_ifs_multiple = """
nodes = [node for node in "abc" if node != "a" if node != "b" if node != "c"]
"""

list_ifs_twice = """
nodes = [node for node in "abc" if node != "a" if node != "b"]
"""

list_ifs_single = 'nodes = [node for node in "abc" if node != "a"]'
list_without_ifs = 'nodes = [node for node in "abc"]'

# Dicts:

dict_ifs_multiple = """
nodes = {xy: xy for xy in "abc" if xy != "a" if xy != "b" if xy != "c"}
"""

dict_ifs_twice = 'nodes = {xy: xy for xy in "abc" if xy != "a" if xy != "b"}'
dict_ifs_single = 'nodes = {xy: xy for xy in "abc" if xy != "a"}'
dict_without_ifs = 'nodes = {xy: xy for xy in "abc"}'

# Generator expressions:

gen_ifs_multiple = """
nodes = (xy for xy in "abc" if xy != "a" if xy != "b" if xy != "c")
"""

gen_ifs_twice = 'nodes = (xy for xy in "abc" if xy != "a" if xy != "b")'
gen_ifs_single = 'nodes = (xy for xy in "abc" if xy != "a")'
gen_without_ifs = 'nodes = (no for xy in "abc")'

# Set comprehensions:

set_ifs_multiple = """
nodes = {xy for xy in "abc" if xy != "a" if xy != "b" if xy != "c"}
"""

set_ifs_twice = 'nodes = {xy for xy in "abc" if xy != "a" if xy != "b"}'
set_ifs_single = 'nodes = {xy for xy in "abc" if xy != "a"}'
set_without_ifs = 'nodes = {xy for xy in "abc"}'

# Async:

async_list_ifs_multiple = """
async def wrapper():
    return [xy async for xy in "abc" if xy != "a" if xy != "b" if xy != "c"]
"""

async_list_ifs_twice = """
async def wrapper():
    return [xy async for xy in "abc" if xy != "a" if xy != "b"]
"""

async_list_ifs_single = """
async def wrapper():
    return [xy async for xy in "abc" if xy != "a"]
"""

async_list_without_ifs = """
async def wrapper():
    return [xy async for xy in "abc"]
"""

nested_loops = """
nodes = [
    target
    for assignment in top_level_assigns
    for target in assignment.targets
    for _ in range(10)
    if isinstance(target, ast.Name) and is_upper_case_name(target.id)
]
"""


@pytest.mark.parametrize('code', [
    list_ifs_single,
    list_without_ifs,
    dict_ifs_single,
    dict_without_ifs,
    gen_ifs_single,
    gen_without_ifs,
    set_ifs_single,
    set_without_ifs,
    async_list_ifs_single,
    async_list_without_ifs,
])
def test_if_keyword_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that using `if` keyword is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongListComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    list_ifs_multiple,
    list_ifs_twice,
    dict_ifs_multiple,
    dict_ifs_twice,
    gen_ifs_multiple,
    gen_ifs_twice,
    set_ifs_multiple,
    set_ifs_twice,
    async_list_ifs_multiple,
    async_list_ifs_twice,
])
def test_multiple_if_keywords_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that using multiple `if` keywords is restricted."""
    tree = parse_ast_tree(code)
    visitor = WrongListComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MultipleIfsInComprehensionViolation])


@pytest.mark.parametrize('code', [
    nested_loops,
])
def test_multiple_for_keywords_in_comprehension(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that using multiple `for` keywords is restricted."""
    tree = parse_ast_tree(code)
    visitor = WrongListComprehensionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyForsInComprehensionViolation])
