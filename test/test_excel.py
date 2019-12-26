"""
Tests for `excel` module.
"""
import pytest

from labwelfare import excel


class TestExcel(object):
    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        pass

    def test_failed_open_file(self):
        """Test for exception when opening file."""
        with pytest.raises(OSError):
            excel.read("/no_file_exist.xlsx")

    def teardown_method(self, method):
        pass

    @classmethod
    def teardown_class(cls):
        pass
