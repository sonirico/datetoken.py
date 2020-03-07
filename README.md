# Datetoken

[![Build Status](https://travis-ci.org/sonirico/datetoken.py.svg?branch=master&style=flat-square)](https://travis-ci.org/sonirico/datetoken.py)
[![PyPI versions](https://img.shields.io/pypi/v/datetoken?style=flat-square)](https://pypi.org/project/datetoken/)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=sonirico/datetoken.py)](https://dependabot.com)

## Features

TL;DR: This package allows you to store complex relative dates in string tokens.

- To define the initial/starting point in time (typically written as `now`), to
  work with dates in the past or in the future. Ideal to perform date
  simulations.
- Time zone configuration. Additionally to the starting point in time, TZs
  can be provided to as to somehow abstract the user away from localizing
  _datetimes_ objects in their apps.

  As a disclaimer, if the custom datetime specified as the starting point
  (`now`'s value) is tz-unaware or naive, it will be treated as an UTC one. 
  Default `now`'s value also fallsback to `datetime.datetime.utcnow`, localized
  to UTC.

  Now, if a time zone is specified, the `now`s value will be coerced to that
  TZ prior to applying both snap and modifier expressions. This is handy
  to quickly resolve tokens given any point in time (either naive or aware), a
  time zone and the datetoken itself.


## Motivation

Have you ever needed to make an application where dates needed to be
represented in a relative fashion, like background periodic
tasks, datetime range pickers... in a compact and stringified format? This
library enables you to persist these string tokens during the lifetime of a
process or even longer, since calculations are performed in the moment of
evaluation. Theses tokens are also useful when caching URLs as replacement
of timestamps, which would break caching given their mutability nature.

Some common examples of relative tokens:

| Presets                        | From           | To            |
|--------------------------------|----------------|---------------|
| Today                          | `now/d`        | `now`         |
| Yesterday                      | `now-d/d`      | `now-d@d`     |
| Last 24 hours                  | `now-24h`      | `now`         |
| Last business week             | `now-w/bw`     | `now-w@bw`    |
| This business week             | `now/bw`       | `now@bw`      |
| Last month                     | `now-1M/M`     | `now-1M@M`    |
| Next week                      | `now+w/w`      | `now+w@w`     |
| Custom range                   | `now+w-2d/h`   | `now+2M-10h`  |
| Last month first business week | `now-M/M+w/bw` | `now-M/+w@bw` |

As you may have noticed, tokens follow a pattern:

- The word `now`. It means the point in the future timeline when tokens are
  parsed to their datetime form.
- Optionally, modifiers to add and/or subtract the future value of `now` can
  be used. Unsurprisingly, additions are set via `+`, while `-` mean
  subtractions. These modifiers can be chained as many times as needed.
  E.g: `now-1M+3d+2h`. Along with the arithmetical sign and the amount, the
  unit of time the amount refers to must be specified. Currently, the supported
  units are:
  - `s` seconds
  - `m` minutes
  - `h` hours
  - `d` days
  - `w` weeks
  - `M` months
- Optionally, there exist two extra modifiers to snap dates to the start or the
  end of any given snapshot unit. Those are:
  - `/` Snap the date to the start of the snapshot unit.
  - `@` Snap the date to the end of the snapshot unit.

  Snapshot units are the same as arithmetical modifiers, plus the following
  ones:
  - `bw`, business week
  - `mon`, Monday
  - `tue`, Tuesday
  - `wed`, Wednesday
  - `thu`, Thursday
  - `fri`, Friday
  - `sat`, Saturday
  - `sun`, Sunday

  With this, we achieve a simple way to define canonical relative date ranges,
  such as _Today_ or _Last month_. As an example of the later:

  - String representation: `now-1M/M`, `now-1M@M`
  - Being today _15 Jan 2018_, the result range should be:
    _2018-01-01 00:00:00 / 2018-01-31 23:59:59_


## Installing

Install and update via either [pipenv](https://pipenv.readthedocs.io/en/latest/)
or [pip](https://pip.pypa.io/en/stable/quickstart/)

```shell
pipenv install datetoken
```

or

```shell
pip install datetoken
```

## A glance into the API

You can use either the _evaluator_ subpackage or the _utils_ one for quicker
access to simpler/common usages.

- `datetoken.evaluator.eval_datetoken`
    - Arguments:
        - token: `{string}` E.g: `now-w/w+2d+8h`
        - kwargs:
            - at: `{datetime.datetime}` custom starting point
            - tz: `{str|pytz.timezone}` custom time zone
    - Return:
        - `datetoken.objects.Token`. Model for tokens. Provides meta information
        such as AST nodes, and whether the token is snapped or has modifiers
        applied
- `datetoken.evaluator.Datetoken` Facade to build tokens on the fly. Supports
   fluent programming too.
- `datetoken.utils.token_to_date`: 
    - Arguments:
        - token: `{string}` E.g: `now-w/w+2d+8h`
        - kwargs:
            - at: `{datetime.datetime}` custom starting point
            - tz: `{str|pytz.timezone}` custom time zone
    - Return:
        - `datetime.datetime`. Datetime object with the result of applying
        token modifiers. Always returns aware tz objects.
- `datetoken.utils.token_to_utc_date`: Same as `token_to_date` but coercing
    the result to UTC.


## Examples

Most probably you will be dealing with simple presets such as _yesterday_ or
the _last 24 hours_.

```python
>>> from datetoken.utils import token_to_date
>>> from datetime import datetime
>>> print(datetime.utcnow())
2018-10-18 14:08:47
>>> token_to_date('now-d/d')  # Start of yesterday
2018-10-17 00:00:00
>>> token_to_date('now-d@d')  # End of yesterday
2018-10-17 23:59:59
```

However, more complex configurations are also supported so as to
provide the flexibility advanced users may need.

```python
>>> from datetoken.utils import token_to_date
>>> print(datetime.utcnow())
2018-10-18 16:34:29+02:00
>>> token_to_date('now-M/M+w/bw')  # Starting of first business week of previous
                                   # month
2018-09-03 00:00:00
```

Fluent programming is also supported:

```python
>>> import pytz
>>> from datetime import datetime
>>> from datetoken.evaluator import Datetoken
>>> then = datetime(2019, 1, 26, 12, 24, 23, tzinfo=pytz.UTC)
>>> Datetoken().at(then).on('Europe/Madrid').for_token('now/d').to_date()
datetime(2019, 1, 26, 0, 0, 0, tzinfo="<DstTzInfo 'Europe/Madrid' CET+1:00:00 STD>")
```

Retrieving dates in `UTC` is implemented too:

```python
>>> import pytz
>>> from datetime import datetime
>>> from datetoken.evaluator import Datetoken
>>> then = datetime(2019, 1, 26, 12, 24, 23, tzinfo=pytz.UTC)
>>> Datetoken().at(then).on('Europe/Madrid').for_token('now/d').to_utc_date()
datetime(2019, 1, 25, 23, 0, 0, tzinfo="<UTC>")

>>> from datetoken.utils import token_to_utc_date
>>> then_in_madrid = datetime(2019, 1, 26, 12, 24, 23, tzinfo=pytz.timezone('Europe/Madrid'))
>>> token_to_utc_date('now/d', at=then_in_madrid)
datetime(2019, 1, 25, 23, 0, 0, tzinfo="<UTC>")
```

If you thought fluent programming is no longer fashionable:

```python
...
>>> then = datetime(2019, 1, 26, 12, 24, 23, tzinfo=pytz.UTC)
>>> token = Datetoken(at=then, tz='Europe/Madrid', token='now/d')
>>> token.to_date()
datetime(2019, 1, 26, 0, 0, 0, tzinfo="<DstTzInfo 'Europe/Madrid' CET+1:00:00 STD>")
```


## Issues

- Business week snapshots might not be reliable in timezones where weeks
  start in days other than Monday or week duration lasts fewer or greater than
  five days

