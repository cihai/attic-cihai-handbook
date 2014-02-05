United front for open, permissive, high quality CJK datasets and clients.

``Cihai`` is a team, effort, united effort for incubating open,
permissive, high quality CJK datasets and clients.

- `cihai-handbook`_ - convert your cjk dataset to `datapackages`_-friendly
  format.
- Official client libraries. `cihai-python`_ a python client for
  cihai+datapackages datasets (cjklib style).
- Public datasets maintained by `cihai team`_. See `cihaidata-unihan on
  github`_.

.. _cihai: https://github.com/cihai/
.. _cihai-handbook: https://github.com/cihai/cihai-handbook
.. _cihai team: https://github.com/cihai?tab=members
.. _cihai-python: https://github.com/cihai/cihai-python
.. _cihaidata-unihan on github: https://github.com/cihai/cihaidata-unihan


Have a CJK dataset? Consider `permissively licensing your dataset`_ and
adopting `datapackages`_ standards.

For an example of a datapackage + cihai enabled dataset, see
https://github.com/cihai/cihaidata-unihan.

CJK Dataset Standards
"""""""""""""""""""""

Cihai CJK datasets follows `dataprotocols`_ conventions:

- `datapackages`_ format.
- `datapackage.json format`_ - has metadata for source file
- `json table schema`_ - ``datapackage.json`` schema information.
- `simple data format`_ - ``scripts/process.py`` produces ``data/unihan.csv``
- *(optional)* `PEP 301: python package format`_ - python package installation.

.. _permissively licensing your dataset: http://cihai.readthedocs.org/en/latest/information_liberation.html

==============  ==========================================================
Docs            http://cihai.rtfd.org
Changelog       http://cihai.readthedocs.org/en/latest/history.html
==============  ==========================================================

.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _Documentation: http://cihai.readthedocs.org/en/latest/
.. _Unihan: http://www.unicode.org/charts/unihan.html
.. _dataprotocols: http://dataprotocols.org
.. _datapackages: http://dataprotocols.org/data-packages/
.. _datapackage.json format: https://github.com/datasets/gdp/blob/master/datapackage.json
.. _json table schema: http://dataprotocols.org/json-table-schema/
.. _simple data format: http://data.okfn.org/standards/simple-data-format
.. _PEP 301\: python package format: http://www.python.org/dev/peps/pep-0301/
