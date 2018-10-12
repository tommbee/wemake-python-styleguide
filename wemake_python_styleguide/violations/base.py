# -*- coding: utf-8 -*-

"""
Contains detailed information about violation and how to use them.

.. _violations:

Writing new violation
---------------------

First of all, you have to select the correct base class for new violation.
The main criteria is what logic will be used to find the flaw in your code.

.. currentmodule:: wemake_python_styleguide.violations.base

Available base classes
~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ASTViolation
   TokenizeViolation
   SimpleViolation

Violation can not have more than one base class.
Since it does not make sense to have two different node types at the same time.

Violations API
--------------

"""

import ast
import tokenize
from typing import ClassVar, Tuple, Union

#: General type for all possible nodes where error happens.
ErrorNode = Union[
    ast.AST,
    tokenize.TokenInfo,
    None,
]


class BaseViolation(object):
    """
    Abstract base class for all style violations.

    It basically just defines how to create any error and how to format
    this error later on.

    Each subclass must define ``error_template`` and ``code`` fields.

    Attributes:
        error_template: message that will be shown to user after formatting.
        code: violation unique number. Used to identify the violation.
        should_use_text: formatting option. Some do not require extra text.

    """

    error_template: ClassVar[str]
    code: ClassVar[int]
    should_use_text: ClassVar[bool] = True

    def __init__(self, node: ErrorNode, text: str = None) -> None:
        """
        Creates new instance of abstract violation.

        Parameters:
            node: violation was raised by this node. If applied.
            text: extra text to format the final message. If applied.

        """
        self._node = node

        if text is None:
            self._text = node.__class__.__name__.lower()
        else:
            self._text = text

    def _full_code(self) -> str:
        """
        Returns fully formatted code.

        Adds violation letter to the numbers.
        Also ensures that codes like ``3`` will be represented as ``Z003``.
        """
        return 'Z' + str(self.code).zfill(3)

    def _location(self) -> Tuple[int, int]:
        """
        Return violation location inside the file.

        Default location is in the so-called "file beginning".
        """
        return 0, 0

    def message(self) -> str:
        """
        Returns error's formatted message with code and reason.

        Conditionally formats the ``error_template`` if it is required.
        """
        if self.should_use_text:
            message = self.error_template.format(self._text)
        else:
            message = self.error_template
        return '{0} {1}'.format(self._full_code(), message)

    def node_items(self) -> Tuple[int, int, str]:
        """Returns tuple to match ``flake8`` API format."""
        return (*self._location(), self.message())


class ASTViolation(BaseViolation):
    """Violation for ``ast`` based style visitors."""

    _node: ast.AST

    def _location(self) -> Tuple[int, int]:
        line_number = getattr(self._node, 'lineno', 0)
        column_offset = getattr(self._node, 'col_offset', 0)
        return line_number, column_offset


class TokenizeViolation(BaseViolation):
    """Violation for ``tokenize`` based visitors."""

    _node: tokenize.TokenInfo

    def _location(self) -> Tuple[int, int]:
        return self._node.start


class SimpleViolation(BaseViolation):
    """Violation for cases where there's no associated nodes."""

    _node: None

    def __init__(self, node=None, text: str = None) -> None:
        """Creates new instance of simple style violation."""
        super().__init__(node, text=text)
