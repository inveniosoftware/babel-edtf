# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Babel-EDTF is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from datetime import datetime

import pytest
from edtf import Date, Interval
from edtf.parser.edtf_exceptions import EDTFParseException

from babel_edtf import edtf_to_datetime, format_edtf, parse_edtf, \
    parse_edtf_level0

separator = '\u2009–\u2009'


@pytest.mark.parametrize('edtfstr,locale,format,expected', [
    # ## Dates
    # Year (en)
    ('2020', 'en', 'short', '2020'),
    ('2020', 'en', 'medium', '2020'),
    ('2020', 'en', 'long', '2020'),
    ('2020', 'en', 'full', '2020'),
    # Year (da)
    ('2020', 'da', 'short', '2020'),
    ('2020', 'da', 'medium', '2020'),
    ('2020', 'da', 'long', '2020'),
    ('2020', 'da', 'full', '2020'),
    # Year-Month (en)
    ('2020-09', 'en', 'short', '9/2020'),
    ('2020-09', 'en', 'medium', 'Sep 2020'),
    ('2020-09', 'en', 'long', 'September 2020'),
    ('2020-09', 'en', 'full', 'September 2020'),
    # Year-Month (da)
    ('2020-09', 'da', 'short', '9.2020'),
    ('2020-09', 'da', 'medium', 'sep. 2020'),
    ('2020-09', 'da', 'long', 'september 2020'),
    ('2020-09', 'da', 'full', 'september 2020'),
    # Year-Month-Day (en)
    ('2020-09-30', 'en', 'short', '9/30/20'),
    ('2020-09-30', 'en', 'medium', 'Sep 30, 2020'),
    ('2020-09-30', 'en', 'long', 'September 30, 2020'),
    ('2020-09-30', 'en', 'full', 'Wednesday, September 30, 2020'),
    # Year-Month-Day (da)
    ('2020-09-30', 'da', 'short', '30.09.2020'),
    ('2020-09-30', 'da', 'medium', '30. sep. 2020'),
    ('2020-09-30', 'da', 'long', '30. september 2020'),
    ('2020-09-30', 'da', 'full', 'onsdag den 30. september 2020'),
    # ### Intervals (same precision)
    # Year (en)
    ('2020/2021', 'en', 'short', f'2020{separator}2021'),
    ('2020/2021', 'en', 'medium', f'2020{separator}2021'),
    ('2020/2021', 'en', 'long', f'2020{separator}2021'),
    ('2020/2021', 'en', 'full', f'2020{separator}2021'),
    # Year (da)
    ('2020/2021', 'da', 'short', '2020–2021'),
    ('2020/2021', 'da', 'medium', '2020–2021'),
    ('2020/2021', 'da', 'long', '2020–2021'),
    ('2020/2021', 'da', 'full', '2020–2021'),
    # Year-Month (constant year) (en)
    ('2020-09/2020-11', 'en', 'short', f'9/2020{separator}11/2020'),
    ('2020-09/2020-11', 'en', 'medium', f'Sep{separator}Nov 2020'),
    ('2020-09/2020-11', 'en', 'long', f'September{separator}November 2020'),
    ('2020-09/2020-11', 'en', 'full', f'September{separator}November 2020'),
    # Year-Month (different year) (en)
    ('2020-09/2021-11', 'en', 'short', f'9/2020{separator}11/2021'),
    ('2020-09/2021-11', 'en', 'medium', f'Sep 2020{separator}Nov 2021'),
    (
        '2020-09/2021-11',
        'en',
        'long',
        f'September 2020{separator}November 2021'
    ),
    (
        '2020-09/2021-11',
        'en',
        'full',
        f'September 2020{separator}November 2021'
    ),
    # Year-Month (reverse chronological order) (da)
    ('2021-11/2020-09', 'da', 'full', 'november 2021–september 2020'),
    # Year-Month-Day (en)
    ('2020-09-01/2020-11-15', 'en', 'short', f'9/1/2020{separator}11/15/2020'),
    ('2020-09-01/2020-11-15', 'en', 'medium', f'Sep 1{separator}Nov 15, 2020'),
    # Note the next two lines. For date intervals we are forced to use
    # format_skeleton, and thus these lines differ in format from other
    # long/full formats.
    ('2020-09-01/2020-11-15', 'en', 'long', f'Sep 1{separator}Nov 15, 2020'),
    (
        '2020-09-01/2020-11-15',
        'en',
        'full',
        f'Tue, Sep 1{separator}Sun, Nov 15, 2020'
    ),
    # ### Intervals (different precision)
    ('2020-09-02/2020-11', 'en', 'long', f'Sep 2{separator}Nov 30, 2020'),
    ('2020-09/2020-11-15', 'en', 'long', f'Sep 1{separator}Nov 15, 2020'),
])
def test_format_edtf(edtfstr, locale, format, expected):
    assert format_edtf(edtfstr, format=format, locale=locale) == expected


def test_format_edtf_invalid():
    """Test invalid values to format_edtf."""
    pytest.raises(ValueError, format_edtf, 'invalid')
    pytest.raises(ValueError, format_edtf, '2021/')
    pytest.raises(ValueError, format_edtf, '2020?')
    pytest.raises(TypeError, format_edtf, 2020)


def test_edtf_to_datetime():
    """Test datetime conversion."""
    y = parse_edtf_level0('2020')
    assert edtf_to_datetime(y, 'lower') == datetime(2020, 1, 1)
    assert edtf_to_datetime(y, 'upper') == datetime(2020, 12, 31)
    pytest.raises(ValueError, edtf_to_datetime, y, 'invalid')


def test_edtf_to_datetime_limit():
    """Test lowest possible date."""
    y = parse_edtf_level0('1000')
    assert edtf_to_datetime(y, 'lower') == datetime(1000, 1, 1)
    assert edtf_to_datetime(y, 'upper') == datetime(1000, 12, 31)


def test_format_edtf_default():
    """Test the default time being used if not value provided."""
    today = datetime.utcnow().date()
    assert format_edtf(format='short', locale='en') == '{}/{}/{}'.format(
        today.month, today.day, str(today.year)[2:4]
    )


def test_format_edtf_format():
    """Test overriding the format."""
    assert format_edtf('2020-11', format='yMd', locale='en') == '11/1/2020'
    assert format_edtf('2020/2021', format='yM', locale='en') == \
        f'1/2020{separator}12/2021'


@pytest.mark.parametrize('edtfstr,expected', [
    # Year in range
    ('2020', Date('2020')),
    ('2020/2021', Interval(Date('2020'), Date('2021'))),
    # Month in range
    ('2020-12', Date('2020', '12')),
    ('2020-09/2020-12', Interval(Date('2020', '09'), Date('2020', '12'))),
    # Day in range
    ('2020-12-31', Date('2020', '12', '31')),
    (
        '2020-09-01/2020-12-31',
        Interval(Date('2020', '09', '01'), Date('2020', '12', '31'))
    ),
    # Day in range for month of February on leap year
    ('2020-02-29', Date('2020', '02', '29')),
    (
        '2020-02-29/2020-12-31',
        Interval(Date('2020', '02', '29'), Date('2020', '12', '31'))
    ),
])
def test_parse_edtf(edtfstr, expected):
    """Test valid values to parse_edtf."""
    parse_edtf(edtfstr) == expected


@pytest.mark.parametrize('edtfstr', [
    # Month out of range
    ('2020-13'),
    ('2020-13/2021-11'),
    ('2020-09/2021-13'),
    ('2020-13-01'),
    ('2020-09-01/2020-13-01'),
    ('2020-13-01/2020-09-01'),
    # Day out of range for month
    ('2020-04-31'),
    ('2020-04-31/2020-11-15'),
    ('2020-09-01/2020-04-31'),
    ('2020-02-30'),
    ('2020-02-30/2020-11-15'),
    ('2020-09-01/2020-02-30'),
    # Day out of range for month of February on non-leap year
    ('2021-02-29'),
    ('2021-02-29/2020-11-15'),
    ('2020-09-01/2021-02-29'),
])
def test_parse_edtf_invalid(edtfstr):
    """Test invalid values to parse_edtf."""
    pytest.raises(EDTFParseException, parse_edtf, edtfstr)
