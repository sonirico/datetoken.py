# Datetoken Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [unreleased]

## [0.6.0 - 2021-10-05]

- Feature: quarters
- Chore: Updated `pytz` dep from <2020.2,>=2018.04 to >=2018.04,<2020.5
- Chore: Updated `python-dateutil` dep from <2021.2,>=2018.04 to >=2018.04,<2021.4

## [0.5.2 - 2020-11-07]

- Updated `pytz` dep from <2020.2,>=2018.04 to >=2018.04,<2020.5

## [0.5.1 - 2020-10-12]

### Added

- Token 'Y' as both snap and modifier behaviours. By @Sighery

## [0.4.1 - 2020-03-06]

### Changed

- Updated depedencies

### Fixed

- Deprecation warnings from the usage of 'collections.Sequence'.

## [0.4.0 - 2019-11-24]
- Feature day of week snappers
- Dependency upgrades:
   - pytz >= 2018.04 < 2019.04
   - python-dateutil >= 2.7.3 < 2.8.2

## [0.3.2 - 2019-10-06]
- Updated dependencies:
    - pytz
    - freeegun
    - python-dateutil

## [0.3.1 - 2019-03-01]
- Fixed `token_to_utc_date` not reading `token` keyword argument

## [0.3.0 - 2019-02-26]
- Refactored testing suite to replace `mock` with
  `freezegun` as it is more convenient to work
  with dates.
- Added features:
  + Support for setting time zones so as to
    localize the `now`'s value prior to apply
    token modifiers.
  + `token_to_utc_date` to evaluate a token and
     get back the result in UTC
  + `eval_datetoken`: Evaluate a token and more
     arguments to later return and `datetoken.objects:Token`
  + `datetoken.evaluator.Datetoken`: Helper to configure
    tokens. Supports fluent programming
- Dropped features:
  + `datetoken.models:Token.from_string` in favor of
    `datetoken.evaluator.eval_datetoken`


## [0.2.0 - 2019-01-14]
- Added features:
  + Chainable modifiers after snap modifiers
  + Partial Pratt parser
- Dropped features:
  + `complex_token_to_date` util
  + `simple_token_to_date` util
  + `SimpleToken` model
  + `ComplexToken` model

## [0.1.2 - 2018-11-29]
- Limit dateutil dependency versions

## [0.1.1 - 2018-10-19]
- Hello world!



