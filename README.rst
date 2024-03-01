..
    Copyright (C) 2020 CERN.

    Babel-EDTF is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

============
 Babel-EDTF
============

A Python module for localization of Extended Date Time Format (EDTF) level 0
strings.

EDTF is a syntax for specifying imprecise dates. See
http://www.loc.gov/standards/datetime/. This modules relies on
`python-edtf <https://pypi.org/project/edtf/>`_ for
EDTF parsing.

Install
-------

Babel-EDTF is on PyPI so all you need is:

.. code-block:: console

   $ pip install babel-edtf

Quickstart
----------
Let's format some EDTF strings:

>>> from babel_edtf import format_edtf
>>> format_edtf('2020-01', locale='en')
'Jan 2020'

>>> format_edtf('2020-01/2020-09', locale='da')
'jan.–sep. 2020'

>>> format_edtf('2020-01/2020-09', format='long', locale='en')
'January\u2009–\u2009September 2020'

The following formats are supported:

- ``short``
- ``medium``
- ``long``
- ``full``
