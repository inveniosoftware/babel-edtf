#!/usr/bin/env sh
# SPDX-FileCopyrightText: 2020 CERN.
# SPDX-License-Identifier: MIT

python -m sphinx.cmd.build -qnNW docs docs/_build/html && \
python -m pytest && \
python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest
