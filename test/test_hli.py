"""
Tests for `heat_load` module.
"""
import pytest
from labwelfare import Indicator, hli, hli_bg, hli_indicator, hli_no_bg


class TestHLI(object):
    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        # air temperature
        self.air_temp = 27.4
        # black globe temperature
        self.bg_temp = 39
        # relative humidity
        self.r_hum = 93
        # invalid relative humidity
        self.r_hum_invalid = -93
        # invalid relative humidity non-numeric
        self.r_hum_invalid_str = 'invalid'
        # solar radiation
        self.solar_rad = 0
        # wind speed km/h
        self.w_speed = 12.9
        # invalid wind speed
        self.w_speed_invalid = -12.9
        # invalid wind speed non-numeric
        self.w_speed_invalid_str = 'invalid'

    def test_hli_bg_value_ok(self):
        """Test heat load index black globe value."""
        expected = pytest.approx(97.91, 0.1)
        h = hli_bg(self.bg_temp, self.r_hum, self.w_speed)
        assert h == expected

    def test_hli_bg_invalid_wind_speed_number(self):
        """Test for invalid numerical value for wind speed."""
        with pytest.raises(ValueError, match=r".* -12.9 .*"):
            hli_bg(self.bg_temp, self.r_hum, self.w_speed_invalid)

    def test_hli_bg_invalid_wind_speed_non_numeric(self):
        """Test for invalid non-numeric value for wind speed."""
        with pytest.raises(ValueError):
            hli_bg(self.bg_temp, self.r_hum, self.w_speed_invalid_str)

    def test_hli_bg_invalid_rel_humidity_number(self):
        """Test for invalid numerical value for relative humidity."""
        with pytest.raises(ValueError, match=r".* -93 .*"):
            hli_bg(self.bg_temp, self.r_hum_invalid, self.w_speed)

    def test_hli_bg_invalid_rel_humidity_non_numeric(self):
        """Test for invalid non-numeric value for relative humidity."""
        with pytest.raises(ValueError):
            hli_bg(self.bg_temp, self.r_hum_invalid, self.w_speed)

    def test_hli_no_bg_value_ok(self):
        """Test heat load index no black globe value."""
        expected = pytest.approx(63.15, 0.1)
        got = hli_no_bg(self.air_temp, 66, self.solar_rad, 9.7)
        assert got == expected

    def test_hli_no_bg_invalid_wind_speed_number(self):
        """Test heat load index no bg for invalid numerical value for wind
        speed."""
        with pytest.raises(ValueError, match=r".* -12.9 .*"):
            hli_no_bg(self.air_temp, self.r_hum, self.solar_rad,
                      self.w_speed_invalid)

    def test_hli_no_bg_invalid_wind_speed_non_numeric(self):
        """Test for invalid non-numeric value for wind speed."""
        with pytest.raises(ValueError):
            hli_no_bg(self.air_temp, self.r_hum, self.solar_rad,
                      self.w_speed_invalid_str)

    def test_hli_no_bg_invalid_rel_humidity_number(self):
        """Test for invalid numerical value for relative humidity."""
        with pytest.raises(ValueError, match=r".* -93 .*"):
            hli_no_bg(self.air_temp, self.r_hum_invalid, self.solar_rad,
                      self.w_speed)

    def test_hli_no_bg_invalid_rel_humidity_non_numeric(self):
        """Test for invalid non-numeric value for relative humidity."""
        with pytest.raises(ValueError):
            hli_no_bg(self.air_temp, self.r_hum_invalid, self.solar_rad,
                      self.w_speed)

    def test_hli_no_bg_invalid_solar_rad_number(self):
        """Test for invalid numerical value for solar radiation."""
        with pytest.raises(ValueError, match=r".* -5.1 .*"):
            hli_no_bg(self.air_temp, self.r_hum, -5.1, self.w_speed)

    def test_hli_no_bg_invalid_solar_rad_non_numeric(self):
        """Test for invalid non-numeric value for solar radiation."""
        with pytest.raises(ValueError):
            hli_no_bg(self.air_temp, self.r_hum, 'invalid number',
                      self.w_speed)

    def test_hli_indicator_neglegible(self):
        """Test heat load index indicator is neglegible."""
        expected = Indicator.NEGLEGIBLE.value
        indicator = hli_indicator(0)
        assert indicator == expected

    def test_hli_indicator_low_risk(self):
        """Test heat load index indicator is low risk."""
        expected = Indicator.LOW.value
        indicator = hli_indicator(19)
        assert indicator == expected

    def test_hli_indicator_medium_risk(self):
        """Test heat load index indicator is medium risk."""
        expected = Indicator.MEDIUM.value
        indicator = hli_indicator(22)
        assert indicator == expected

    def test_hli_indicator_high_risk(self):
        """Test heat load index indicator is high risk."""
        expected = Indicator.HIGH.value
        indicator = hli_indicator(97)
        assert indicator == expected

    def test_hli_indicator_extreme_risk(self):
        """Test heat load index indicator is extreme risk."""
        expected = Indicator.EXTREME.value
        indicator = hli_indicator(300)
        assert indicator == expected

    def test_hli_indicator_hli_non_numeric(self):
        """Test for invalid non-numeric value for hli."""
        with pytest.raises(ValueError):
            hli_indicator('invalid_number')

    def test_hli_indicator_threshold_non_numeric(self):
        """Test for invalid non-numeric value for hli."""
        with pytest.raises(ValueError):
            hli_indicator(98, threshold='invalid_number')

    def test_hli_indicator_hli_negative_number(self):
        """Test for invalid negative value for hli."""
        with pytest.raises(ValueError):
            hli_indicator(-1)

    def test_hli_indicator_threshold_negative_number(self):
        """Test for invalid negative value for threshold."""
        with pytest.raises(ValueError):
            hli_indicator(98, threshold=-1)

    def test_hli_from_bg(self):
        """Teste heat load index from black globe arguments."""
        expected_hli = pytest.approx(97.91, 0.1)
        expected_indicator = Indicator.HIGH.value
        arguments = {
            'bg_temp': self.bg_temp,
            'rel_hum': self.r_hum,
            'wind_speed': self.w_speed
        }
        h, ind = hli(True, **arguments)
        assert h == expected_hli
        assert ind == expected_indicator

    def test_hli_from_no_bg(self):
        """Teste heat load index from no black globe arguments."""
        expected_hli = pytest.approx(63.15, 0.1)
        expected_indicator = Indicator.MEDIUM.value
        arguments = {
            'air_temp': self.air_temp,
            'rel_hum': 66,
            'wind_speed': 9.7,
            'solar_rad': self.solar_rad
        }
        h, ind = hli(True, **arguments)
        assert h == expected_hli
        assert ind == expected_indicator

    def test_hli_required_arguments(self):
        """Test for missing required arguments."""
        with pytest.raises(ValueError):
            arguments = {
                'air_temp': self.air_temp,
                'solar_rad': self.solar_rad
            }
            hli(True, **arguments)

    def teardown_method(self, method):
        pass

    @classmethod
    def teardown_class(cls):
        pass
