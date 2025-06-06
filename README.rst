deco3
=====

Decorated Concurrency.

A simplified parallel computing model for Python. DECO automatically
parallelizes Python programs, and requires minimal modifications to
existing serial programs.

Overview
========

|package_bold| is a strict fork of Alex Sherman's `deco package <deco_>`_
with a fix allowing to work with Python3 or higher and with a little code
reformatting and minor improvements.

`PyPI record`_.

`Documentation`_.

Overview below is a copy from the original `deco website <deco_>`_
(with only the necessary changes regarding |package|).

Documentation
-------------

You can reference the `Wiki on Github <deco_wiki_>`_
for slightly more in-depth documentation.

General Usage
-------------

Using DECO is as simple as finding, or creating, two functions in your
Python program. The first function is the one we want to run in
parallel, and is decorated with ``@concurrent``. The second function is
the function which calls the ``@concurrent`` function and is decorated
with ``@synchronized``. Decorating the second function is optional, but
provides some very cool benefits. Let's take a look at an example.

.. code:: python

   @concurrent  # We add this for the concurrent function
   def process_lat_lon(lat, lon, data):
     #Does some work which takes a while
     return result

   @synchronized  # And we add this for the function which calls the concurrent function
   def process_data_set(data):
     results = defaultdict(dict)
     for lat in range(...):
       for lon in range(...):
         results[lat][lon] = process_lat_lon(lat, lon, data)
     return results

That's it, two lines of changes is all we need in order to parallelize
this program. Now this program will make use of all the cores on the
machine it's running on, allowing it to run significantly faster.

What it does
------------

- The ``@concurrent`` decorator uses multiprocessing.pool to parallelize
  calls to the target function
- Indexed based mutation of function arguments is handled automatically,
  which pool cannot do
- The ``@synchronized`` decorator automatically inserts synchronization
  events
- It also automatically refactors assignments of the results of
  ``@concurrent`` function calls to happen during synchronization events

Limitations
-----------

- The ``@concurrent`` decorator will only speed up functions that take
  longer than ~1ms

  - If they take less time your code will run slower!

- By default, ``@concurrent`` function arguments/return values must be
  pickleable for use with ``multiprocessing``
- The ``@synchronized`` decorator only works on 'simple' functions, make
  sure the function meets the following criteria

  - Only calls, or assigns the result of ``@concurrent`` functions to
    indexable objects such as:

    - concurrent(...)
    - result[key] = concurrent(...)

  - Never indirectly reads objects that get assigned to by calls of the
    ``@concurrent`` function

How it works
------------

For an in depth discussion of the mechanisms at work, we wrote a paper
for a class which `can be found here <decorated_concurrency_>`_
(or original `can be found here <decorated_concurrency_org_>`_).

As an overview, DECO is mainly just a smart wrapper for Python's
multiprocessing.pool. When ``@concurrent`` is applied to a function it
replaces it with calls to pool.apply_async. Additionally when arguments
are passed to pool.apply_async, DECO replaces any index mutable objects
with proxies, allowing it to detect and synchronize mutations of these
objects. The results of these calls can then be obtained by calling
wait() on the concurrent function, invoking a synchronization event.
These events can be placed automatically in your code by using the
``@synchronized`` decorator on functions that call ``@concurrent``
functions. Additionally while using ``@synchronized``, you can directly
assign the result of concurrent function calls to index mutable objects.
These assignments get refactored by DECO to automatically occur during
the next synchronization event. All of this means that in many cases,
parallel programming using DECO appears exactly the same as simpler
serial programming.

Installation
============

Prerequisites:

+ Python 3.10 or higher

  * https://www.python.org/

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

  .. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

Visit `Development page`_.

Installation from sources:

clone the sources:

  .. parsed-literal::

    git clone |respository| |package|

and run:

  .. parsed-literal::

    python -m pip install ./|package|

or on development mode:

  .. parsed-literal::

    python -m pip install --editable ./|package|

License
=======

  | |copyright|
  | Copyright (c) 2016 Alex Sherman
  | Licensed under the MIT License
  | https://opensource.org/license/mit
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Alex Sherman <asherman1024@gmail.com>
* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: deco3
.. |package_bold| replace:: **deco3**
.. |copyright| replace:: Copyright (c) 2025-2025 Adam Karpierz
.. |respository| replace:: https://github.com/karpierz/deco3.git
.. _Development page: https://github.com/karpierz/deco3
.. _PyPI record: https://pypi.org/project/deco3/
.. _Documentation: https://deco3.readthedocs.io/
.. _deco: https://pypi.org/project/deco/
.. _deco_wiki: https://github.com/alex-sherman/deco/wiki
.. _decorated_concurrency: _static/Decorated_Concurrency.pdf
.. _decorated_concurrency_org: https://drive.google.com/file/d/0B_olmC0u8E3gWTBmN3pydGxHdEE/view?usp=sharing&resourcekey=0-9aUctXy9Hn5g9SIul4kbVw
