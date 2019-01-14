Project description
-------------------

This package aims to solve a set of needs present in applications where
dates need to be represented in a relative fashion, like background periodic
tasks, datetime range pickers... in a compact and stringified format. This
enables the programmer to persist these tokens during the lifetime of a
process or even longer, since calculations are performed in the moment of
evaluation. Theses tokens are also useful when caching URLs as replacement
of timestamps, which would break caching given their mutability nature.

Some common examples of relative tokens:

-  Today: ``now/d``, ``now``
-  Yesterday: ``now-d/d``, ``now-d@d``
-  Last 24 hours: ``now-1d``, ``now``. Also writable as: ``now-24h``,
   ``now``
-  Last business week: ``now-w/bw``, ``now-w@bw``
-  This business week: ``now/bw``, ``now@bw``
-  Last month: ``now-1M/M``, ``now-1M@M``
-  Last month first business week: ``now-M/M+w/bw``, ``now-M/M+w@bw``

As you may have noticed, token follow a pattern:

-  The word ``now``. It means the point in the future timeline when
   tokens are parsed to their datetime form.
-  Optionally, modifiers to add and/or subtract the future value of
   ``now`` can be used. Unsurprisingly, additions are set via ``+``, while
   ``-`` mean subtractions. These modifiers can be chained as many times
   as needed. E.g: ``now-1M+3d+2h``. Along with the arithmetical sign
   and the amount, the unit of time the amount refers to must be
   specified. Currently, the supported units are:

   -  ``s`` seconds
   -  ``m`` minutes
   -  ``h`` hours
   -  ``d`` days
   -  ``w`` weeks
   -  ``M`` months

-  Optionally, there exist two extra modifiers to snap dates to the
   start or the end of any given snapshot unit. Those are:

   -  ``/`` Snap the date to the start of the snapshot unit.
   -  ``@`` Snap the date to the end of the snapshot unit.

   Snapshot units are the same as arithmetical modifiers, plus ``bw``,
   meaning *business week*. With this, we achieve a simple way to define
   canonical relative date ranges, such as *Today* or *Last month*. As
   an example of the later:

   -  String representation: ``now-1M/M``, ``now-1M@M``
   -  Being today *15 Jan 2018*, the result range should be: *2018-01-01
      00:00:00 / 2018-01-31 23:59:59*


Installing
----------

Install and update via either `pipenv`_ or `pip`_

.. code:: shell

    pipenv install datetoken

or

.. code:: shell

    pip install datetoken


Examples and usage
------------------

Most probably you will be dealing with simple presets such as
*yesterday* or the *last 24 hours*.

.. code:: python

   >>> from datetoken.utils import token_to_date
   >>> from datetime import datetime
   >>> print(datetime.utcnow())
   2018-10-18 14:08:47
   >>> simple_token_to_date('now-d/d')  # Start of yesterday
   2018-10-17 00:00:00
   >>> simple_token_to_date('now-d@d')  # End of yesterday
   2018-10-17 23:59:59

.. _pipenv: https://pipenv.readthedocs.io/en/latest/
.. _pip: https://pip.pypa.io/en/stable/quickstart/

