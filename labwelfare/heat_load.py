#
# Copyright (c) Murilo Ijanc' <mbsd@m0x.ru>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
"""Module that calculates heat load index.

Gaughan et al. (2008) proposed this thermal comfort index for feedlot beef
cattle in Australia. It can be calculated for two different environmental
conditions.
"""
import logging
import math
import numbers
from enum import Enum, unique

LOGGER = logging.getLogger(__name__)
DEFAULT_THRESHOLD = 86


@unique
class Indicator(Enum):
    """Indicator risk."""
    NEGLEGIBLE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    EXTREME = 5


def hli_bg(bg_temp, rel_hum, wind_speed):
    """Heat Load Index.

    Args:
        bg_temp (float): black globe temperature (°C).
        rel_hum (float): relative humidity (%).
        wind_speed (float): wind speed (km/h).

    Returns:
        float: heat load index value

    Raises:
        ValueError: If bg_temp, rel_hum and wind_speed not a number.
                    If rel_hum or wind_speed is a negative number.
    """
    if not isinstance(bg_temp, numbers.Number) or \
            not isinstance(rel_hum, numbers.Number) or \
            not isinstance(wind_speed, numbers.Number):
        LOGGER.exception('black globe, humidity, and wind be numeric value')
        raise ValueError('black globe, humidity, and wind be numeric value')

    # wind speed and relative humidity cannot be negative.
    if rel_hum < 0 or wind_speed < 0:
        LOGGER.exception('Relative humidity: {} or wind speed: {} '
                         'cannot be negative.'.format(rel_hum, wind_speed))
        raise ValueError('Relative humidity: {} or wind speed: {} '
                         'cannot be negative.'.format(rel_hum, wind_speed))

    # TODO: what's it?
    frac_high = 1.0 / (1.0 + math.exp(-((bg_temp - 25.0) / 2.25)))
    # TODO: what's it?
    hli_high = 1.55 * bg_temp + 0.38 * rel_hum - 0.5 * \
        wind_speed + math.exp(2.4 - wind_speed) + 8.62
    # TODO: what's it?
    hli_low = 1.3 * bg_temp + 0.28 * rel_hum - wind_speed + 10.66
    _hli = (frac_high * hli_high) + ((1 - frac_high) * hli_low)

    return _hli


def hli_no_bg(air_temp, rel_hum, solar_rad, wind_speed):
    """Heat load index indicator no black globe.

    Args:
        air_temp (float): air temperature (°C).
        rel_hum (float): relative humidity (%).
        solar_rad (float): solar radiation value.
        wind_speed (float): wind speed (km/h).

    Returns:
        float: heat load index value

    Raises:
        ValueError: If hli and thresgold not a number.
                    If hli or threshold is a negative number.
    """
    if not isinstance(air_temp, numbers.Number) or \
            not isinstance(rel_hum, numbers.Number) or \
            not isinstance(solar_rad, numbers.Number) or \
            not isinstance(wind_speed, numbers.Number):
        LOGGER.exception('black globe, humidity, and wind be numeric value')
        raise ValueError('black globe, humidity, and wind be numeric value')

    # wind speed and relative humidity cannot be negative.
    if rel_hum < 0 or solar_rad < 0 or wind_speed < 0:
        LOGGER.exception(
            'Relative humidity: {} or solar radiation: {} or wind speed: {} '
            'cannot be negative.'.format(rel_hum, solar_rad, wind_speed))
        raise ValueError(
            'Relative humidity: {} or solar radiation: {} or wind speed: {} '
            'cannot be negative.'.format(rel_hum, solar_rad, wind_speed))

    # predicted black globe temperature based on air temp and solar radiation
    pred_bg = 1.33 * air_temp - 2.65 * math.pow(
        air_temp, 0.5) + 3.21 * math.log10(solar_rad + 1) + 3.5
    return hli_bg(pred_bg, rel_hum, wind_speed)


def hli_indicator(hli, threshold=86):
    """Heat load index indicator.

    Args:
        hli (float): heat load index value.
        threshold (float): threshold value.

    Returns:
        string: indicating the thermal risk of the animal.

    Raises:
        ValueError: If hli and threshold not a number.
                    If hli or threshold is a negative number.
    """
    if not isinstance(hli, numbers.Number) or \
            not isinstance(threshold, numbers.Number):
        LOGGER.exception('heat load index, threshold be numeric value')
        raise ValueError('heat load index, threshold be numeric value')

    # wind speed and relative humidity cannot be negative.
    if hli < 0 or threshold < 0:
        LOGGER.exception('Heat load index: {} or threshold: {} '
                         'cannot be negative.'.format(hli, threshold))
        raise ValueError('Heat load index: {} or threshold: {} '
                         'cannot be negative.'.format(hli, threshold))

    if hli == 0:
        indicator_value = Indicator.NEGLEGIBLE.value
    elif 1 < hli <= 20:
        indicator_value = Indicator.LOW.value
    elif 21 < hli <= threshold:
        indicator_value = Indicator.MEDIUM.value
    elif threshold < hli <= 100:
        indicator_value = Indicator.HIGH.value
    else:
        indicator_value = Indicator.EXTREME.value

    return indicator_value


def hli(indicator=False, **kwargs):
    """Heat load index.

    Calculate the heat load index based on the possible arguments that may be
    used, in which case the wind speed values in km/h and relative humidity
    will have to be passed. Already for the other arguments you must pass
    temperature of the black globe ``or`` air temperature and solar radiation.

    Args:
        indicator (bool): if true return heat load index and indicator.
        kwargs (dict): requires keys rel_hum, wind_speed, If you have the
                       black globe temperature value use the ``bg_temp``
                       key otherwise enter the air temperature ``air_temp``,
                       solar radiation ``solar_rad`` keys.

    Returns:
        tuple: if indicator true return tuple (heat load index, indicator).
    """
    args = kwargs.keys()
    h = None
    threshold = DEFAULT_THRESHOLD

    # check if exist threshold in kwargs
    if 'threshold' in args:
        threshold = kwargs['threshold']

    # required args rel_hum and wind_speed
    if 'rel_hum' not in args and 'wind_speed' not in args:
        LOGGER.exception('Required keys: rel_hum and wind_speed')
        raise ValueError('Required keys: rel_hum and wind_speed')
    # black globe temperature in args
    if 'bg_temp' in args:
        h = hli_bg(kwargs['bg_temp'], kwargs['rel_hum'], kwargs['wind_speed'])
    # calculate heat load index withoud black globe
    elif 'air_temp' in args and 'solar_rad' in args:
        h = hli_no_bg(kwargs['air_temp'], kwargs['rel_hum'],
                      kwargs['solar_rad'], kwargs['wind_speed'])
    else:
        LOGGER.exception(
            'Must have key bg_temp or keys air_temp and solar_rad')
        ValueError('Must have key bg_temp or keys air_temp and solar_rad')
    # return heat load index and indicator value Ex. (98.1, 4)
    if indicator:
        ind = hli_indicator(h, threshold)
        return (h, ind)
    return (h, None)
