"""Tests for the baseopt package.
"""

import pytest
from baseopt import BaseOption, BaseOptions


class TestOptions():
    """Test class BaseOptions"""
    def test_help(self):
        """Print the help message."""
        options = BaseOptions()
        options.help()

        assert True

    def test_add_opt(self):
        """Add an option to the option list."""
        options = BaseOptions()
        options.add(name="test", default="on", doc="An option for testing")

        assert options["test"].value == "on"

    def test_set_value(self):
        """Set the value of an option manually."""
        options = BaseOptions([
            BaseOption(name="help", default=True, dtype=bool)
            ])
        options["help"].value = True

        assert options["help"].value

    def test_undefined_option(self):
        """Access an undefined option."""
        options = BaseOptions()

        with pytest.raises(KeyError):
            options["undefined name"]


class TestOption():
    """Test class BaseOption"""
    def test_empty_opt(self):
        """Invalid empty opt."""
        with pytest.raises(ValueError):
            BaseOption()

    def test_invalid_shortname(self):
        """Short name longer than 1 character."""
        with pytest.raises(ValueError):
            BaseOption(name="test", shortname="test")
