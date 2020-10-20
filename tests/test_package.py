# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Babel-EDTF is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""


def test_version():
    """Test version import."""
    from babel_edtf import __version__
    assert __version__
