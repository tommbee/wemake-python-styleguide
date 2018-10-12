# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.naming import (
    UnderScoredNumberNameViolation,
)
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
    WrongModuleNameVisitor,
)


@pytest.mark.parametrize('filename', [
    'version_2.py',
    'custom_2_version.py',
])
def test_filename_with_underscored_number(
    assert_errors,
    filename,
    default_options,
):
    """Testing that file names with underscored numbers are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [UnderScoredNumberNameViolation])


@pytest.mark.parametrize('filename', [
    'version2.py',
    'version2_8.py',
])
def test_filename_without_underscored_number(
    assert_errors,
    filename,
    default_options,
):
    """Testing that file names with underscored numbers are restricted."""
    visitor = WrongModuleNameVisitor(default_options, filename=filename)
    visitor.run()

    assert_errors(visitor, [])
