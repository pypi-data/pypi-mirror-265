# Changelog

All notable changes to this project will be documented in this file.

<a name="1.0.0.a1"></a>
## [1.0.0.a1] - 2024-04-03

This prerelease finishes updating the code to the new [`lymph`] package API. It also features a rewrite of the commands to predict and compute e.g. risks and prevalences.

[`lymph`]: https://lymph-model.readthedocs.io


### Bug Fixes

- ⚠ **BREAKING** Use modern lydata cols for t_stage matching.
- Wrong lnls in predict prevalences.
- ⚠ **BREAKING** Update prevalence prediction to new lymph API.
- (**sample**) Match T-stage mapping with lymph API.\
  The lymph model now accepts callables and dicts as T-stage mapping (but
  not `None`). I can hence simply pass the dictionary from the config to
  the loading function.
- (**data**) Stop dtype change during `concat`.\
  When a `DataFrame` with no `NaN`s was joined with one consisting _only_
  of `NaN`s, then it forced some weird kind of dtype conversion onty the
  respective column. Now, dtypes are converted _before_ the concatenation,
  fixing that issue.
- (**sample**) Skip 0 iter convergence check.
- (**sample**) Missing import.
- (**sample**) Only pass `side` to unilateral model.
- (**sample**) Display converged message nicely.
- (**utils**) Correct default args for `get_chain()`.
- Wrong posterior shape.
- (**predict**) Even out some bugs.
- Don't pycln accessor import.
- (**data**) Enhance failed due to copy on write.

### Documentation

- Start with basic sphinx setup.
- Start organizing top-level cmds with sphinx.
- Include all modules in docs.
- Update docstrings to reST format.
- Add document files for precompute subcmd.
- Allow links to lymph docs.
- Fix `temp_schedule` docstring.
- Shorten titles.
- (**predict**) Update prevalence module docstring.
- Refactor docs for new `compute` subcommand.
- Fix typos and missing modules.

### Features

- (**data**) Add simple data filter command. Fixes [#51].
- Customize log handler for better filename.
- (**sample**) Allow custom T-stage mapping.
- (**sample**) Allow to load `side` data.
- (**utils**) Allow `Unilateral.binary` in params.
- (**sample**) Display time elapsed during burnin.
- (**predict**) Add cmd to precompute state dists.
- (**precompute**) Add `priors` cmd. Related [#54].\
  This allows precomputing the state distributions of all three
  implemented lymph models.
- (**utils**) Allow keywords in modalities def.\
  One may now use a dict with keys `spec`, `sens`, and `kind` to define a
  modality in the YAML params.
- (**post**) Compute for multiple scenarios.\
  One may now compute the posteriors for a list of defined scenarios.
- Add class for storing scenarios.
- (**precompute**) Priors from list of scenarios.
- (**predict**) Finish prevalences cmd.
- (**data**) Implement custom pandas accessor.
- (**scenario**) Track laterality as well.
- (**compute**) Risk works with lymph v1, too, now.

### Testing

- (**data**) Ensure new joining works correctly.
- (**sample**) Check some sampling methods.
- Fix typos in tests.
- Update failing tests.

### Build

- Bump lymph-model to v1.0.
- Bump lymph version & add sphinx deps.

### Change

- ⚠ **BREAKING** (**sample**) Reimplement sampling command.
- (**precompute**) Use HDF5 cache. Fixes [#54].\
  The `priors` and `posteriors` commands now use a simple `HDF5FileCache`
  to avoid recomputing either of those quantities unnecessarily.
- (**precompute**) Make recursive. Related [#54].\
  The computation of priors and posteriors is now somewhat recursive. This
  will allow us to just call one function and it will automatically
  compute the priors, posteriors, and risks if necessary.
- (**prevs**) Start on updated `prevalences` cmd.
- Replace 'diagnose' & bump lymph to 1.2.0.
- (**precompute**) Posteriors only from priors.\
  Posteriors now require priors and cannot compute priors "along the way"
  from given samples. This is to make it clear which is an input file and
  which an output file. Otherwise, caching would have been even trickier.
- (**scenario**) Shorten hash to 6 digits.

### Ci

- Add readthedocs config file.
- Remove pdoc action.

### Merge

- Branch 'main' into 'dev'.
- Branch '51-filter-command' into 'dev'.
- Branch '53-use-sphinx-for-documentation' into 'dev'.
- Branch '54-add-precompute-commands' into 'dev'.

### Refac

- (**sample**) Better progress tracking.
- (**precompute**) Comp state dist in own submod.
- (**utils**) Move funcs out of `precompute`.
- Bundle adding scneario args to parser.
- (**compute**) Predict & precompute -> compute.\
  The `predict` and `precompute` commands are now bundled under the
  subcommand `compute`.


### Remove

- ⚠ **BREAKING** Midline_ext in create_patient_row for now.


<a name="1.0.0.a0"></a>
## [1.0.0.a0] - 2023-12-20

### Bug Fixes

- Update imports to new lymph version
- Remove references to `clean` command

### Miscellaneous Tasks

- [**breaking**] Lyprox to lymph convert not necessary anymore

### Build

- Bump lymph-model version to `>=1.0.0.a4`
- Bump type hints to Python 3.10

### Change

- [**breaking**] `evaluate`: command does not depend on lymph model anymore
- Simplify `log_state()` decorator
- [**breaking**] Change model initialization in some places
- [**breaking**] Use deorated function name for `log_state()` message

### Refac

- [**breaking**] Deduplicate data loading functions: `load_csv_table()` was removed and `load_data_for_model()` renamed to `load_patient_data()`
- Change function names & remove logger from decorated function calls

### Remove

- [**breaking**] Delete unnecessary functions


<a name="0.7.3"></a>
## [0.7.3] - 2023-08-29

### Bug Fixes
- **data:** `enhance` command is now deterministic, fixes [#40]
- **plot:** correct color keyword arguments & swap arguments in `save_figure` function, fixes [#45]
- **sample:** use global numpy random state, fixes [#31]

### Maintenance
- fix upper version bound of lymph-model package

### Testing
- **sample:** add test for determinism of sampling, related to [#31]


<a name="0.7.2"></a>
## [0.7.2] - 2023-07-31

### Bug Fixes
- `enhance`: fix bug introduced in [0.7.1]


<a name="0.7.1"></a>
## [0.7.1] - 2023-07-31

### Bug Fixes
- `enhance`: negative sublevels don't overwrite superlevels anymore. Fixes [#44].

### Maintenance
- bump pre-commit hooks


<a name="0.7.0"></a>
## [0.7.0] - 2023-06-26

### Bug Fixes
- add modalities from params in synthetic data generation

### Features
- add extensible & versatile logging decorator
- add `--log-level` option to top-level lyscripts command
- add log-level to `log_state` decorator

### Other
- all commands now use the logging library for status updates/ouputs. This fixes [#2].


<a name="0.6.9"></a>
## [0.6.9] - 2023-06-21

### Bug Fixes
- change the indentation length in the generated markdown data documentation to 4 spaces. Fixes [#41].


<a name="0.6.8"></a>
## [0.6.8] - 2023-05-30

### Bug Fixes
- flattening error in `lyproxify`
- more robust lyproxify working again

### Documentation
- add detail to docstring of `lyproxify` func

### Features
- add func to generate md docs from column map
- add two new dict modifying functions


<a name="0.6.7"></a>
## [0.6.7] - 2023-05-23

### Bug Fixes
- make flatten/unflatten funcs more consistent
- add `max_depth` option for `flatten` function
- bump isort version to avoid error

### Features
- add `unflatten` function


<a name="0.6.6"></a>
## [0.6.6] - 2022-12-01

### Bug Fixes
- pull another function out of a `rich` context, this time in the `join` command. Related to [#33].


<a name="0.6.5"></a>
## [0.6.5] - 2022-12-01

### Bug Fixes
- swap arguments in the `save_figure` call of the `corner` command
- pull a function using [`rich`] to report its status out of an enclosing [`rich`] context. This fixes [#33].


<a name="0.6.4"></a>
## [0.6.4] - 2022-12-01

### Bug Fixes
- `hist_kwargs` now overrides the default plot settings for `Histogram`. This fixes [#30]

### Features
- the `lyscripts sample` command now has an argument `--seed` with the aim of making sampling runs reproducible via a random number generator seed. However, it seems as if the [`emcee`] package does not properly support this as runs using the same seed still produce different results. Related to, but not resolving [#31].


<a name="0.6.3"></a>
## [0.6.3] - 2022-11-25

### Bug Fixes
- `lyproxify`: apply re-indexing only _after_ excluding patients
- fix `SettingWithCopyWarning` during re-indexing in `lyproxify`


<a name="0.6.2"></a>
## [0.6.2] - 2022-11-25

### Bug Fixes
- `lyproxify` cleans empty header cell names

### Documentation
- update lyproxify's `main` docstring
- improve `report_state` & `exclude_patients` documentation
- update top-level `lyproxify` help in README.md

### Features
- allow muting `report_state` decorator globally for a decorated function, while also allowing to override the verbosity per function call
- allow adding an index column during `lyproxify`
- add options to `lyproxify` for dropping rows and columns before starting transformation of raw data
- the `report_state` decorator can now be configured to exit the program when encountering an unexpected exception


<a name="0.6.1"></a>
## [0.6.1] - 2022-11-24

### Features
- add new command under `lyscripts data` to preprocess any raw data into a format that can be parsed by [LyProX]. Fixes [#25]


<a name="0.6.0"></a>
## [0.6.0] - 2022-11-23

### Bug Fixes
- display errors and stop, but don't reraise
- add & update main entry point for script use

### Code Refactoring
- use `lyscripts.utils` consistently across data commands
- use `lyscripts.utils` for `evaluate` script
- pull out method to compare prevalence for one sample
- write modular functions for loading YAML, CSV and HDF5 data
- make `lyscripts data join` command a bit more readable
- further modularize `lyscripts data ...` scripts
- standardize CSV saving process
- start to add `utils` for data commands
- put data commands in separate submodule, fixes [#5] (**BREAKING CHANGE!**)

### Documentation
- expand documentation on data, plot & predict subcommands
- enrich the module documentation of predict scripts
- update docstrings of data commands

### Features
- add YAML scenario output to prevalence app
- working version of prevalence app
- add prevalence plot to app
- allow constructing the `lyscripts.plot.utils.Histogram` and `lyscripts.plot.utils.Posterior` from plain data without HDF5 file (**BREAKING CHANGE!**)
- `lyscripts.temp_schedule` output does not have pretty border anymore, making copy & paste easier
- use generators for risk & prevalence prediction, fixes [#23]
- add more params widgets for prevalence app
- add t_stage, midline_ext, ... to prevalence app
- add `LyScriptsError` for passing up messages
- make smart decorators for status reporting
- implement setup of prevalence app
- start implementing streamlit apps

### Testing
- add GitHub action for tests
- fix missing import for corner doctests
- generally, the module is now partially covered by unit tests


<a name="0.5.11"></a>
## [0.5.11] - 2022-11-06

### Bug Fixes
- remove useless import & rename prediction `utils`
- histogram & respective posterior have same color
- fix two bugs detected during integration test:
  1. The custom enumerate with optional progress bar did not enumerate
  2. Function checking if midline extension matches did not work for some lymph classes
- fix wrong import in submodules `plot` & `predict`
- correct relative imports & remove unused functions
- fix small inconsistency in script call

### Code Refactoring
- use function for loading YAML in all scripts
- further modularize tasks, e.g. params loading
- rename test modules
- put function saving figures in separate utility
- replace common main tasks with `util` functions
- pull out function to extract model param labels
- make `utils` public and hence documented
- greatly simplify histogram plotting script
- pull shared functions into `_utils`
- update [`rich_argparse`] & add highlighting (fixes [#20])
- outsource rich enumeration of predictions
- make prevalence prediction much cleaner
- risk & prevalence share method to clean pattern

### Documentation
- update help in predict's docstrings

### Features
- write decorators for general tasks
- add nice helper functions to plot (fixes [#21])
- risk & prevalence can use thinned samples
- write neat recursive functions to flatten dictionaries

### Testing
- implement more `utils` tests
- add test to the `save_figure` utility
- add test to new params loader
- add small doctest to `get_size` plot utility
- add checks for plotting utils
- write simple tests for prevalence prediction
- add doctest & pytest for predict `utils`


<a name="0.5.10"></a>
## [0.5.10] - 2022-10-13

### Bug Fixes
- pick correct consensus method for enhancement ([#17])
- sample does not crash when `pools` not given ([#16])
- add thinning to convergence sampling, too ([#15])

### Documentation
- fix typos & add favicon to docs

<a name="0.5.9"></a>
## [0.5.9] - 2022-09-16

### Documentation
- don't use relative path for social card

### Features
- `sample` command has a new optional argument `--pools` with which one can adjust the number of multiprocessing pools used during the sampling procedure. Fixes [#13]

<a name="0.5.8"></a>
## [0.5.8] - 2022-09-12

### Bug Fixes
- The function `get_midline_ext_prob` in the prevalence prediction now
does not throw an error anymore when unilateral data is provided, but
returns `None` instead. Fixes [#11]

### Features
- add entry points to CLI. This enables one to call `lyscripts ...` directly, instead of having to use `python -m lyscripts ...` all the time.

### Documentation
- add social card to README
- remove `python -m` prefix from command usage in docstrings

<a name="0.5.7"></a>
## [0.5.7] - 2022-08-29

### Bug Fixes
- fix `enhance`'s issue with varying LNLs across modalities ([#8])

### Features
- add progress bar to `enhance` script

<a name="0.5.6"></a>
## [0.5.6] - 2022-08-29

### Bug Fixes
- can choose list of defined mods in params. This allows one to choose different lists of modalities for e.g. the `enhance` script and the `sampling` one.

### Documentation
- correct typos in the changed docstrings
- update docstring of changed scripts

<a name="0.5.5"></a>
## [0.5.5] - 2022-08-25

### Bug Fixes
- clean script was using deprecated lymph.utils. This script has now been incorporated into these scripts.

### Documentation
- update README and add docstrings about `enhance`

### Features
- add enhancement scipt that computes additional diagnostic modalities, combining existing ones.

<a name="0.5.4"></a>
## [0.5.4] - 2022-08-24

### Documentation
- add call signature to docs every subcommand's `main()`
- add badges, installation & usage to README
- fix pdoc issue with importing `__main__` files

### Maintenance
- make pyproject.toml look nice on PyPI
- tell git to ignore docs dir
- set up git-chglog for creating changelogs
- add pre-commit hook to check commit msg


<a name="0.5.3"></a>
## [0.5.3] - 2022-08-22

[Unreleased]: https://github.com/rmnldwg/lyscripts/compare/1.0.0.a1...HEAD
[1.0.0.a1]: https://github.com/rmnldwg/lyscripts/compare/1.0.0.a0...1.0.0.a1
[1.0.0.a0]: https://github.com/rmnldwg/lyscripts/compare/0.7.3...1.0.0.a0
[0.7.3]: https://github.com/rmnldwg/lyscripts/compare/0.7.2...0.7.3
[0.7.2]: https://github.com/rmnldwg/lyscripts/compare/0.7.1...0.7.2
[0.7.1]: https://github.com/rmnldwg/lyscripts/compare/0.7.0...0.7.1
[0.7.0]: https://github.com/rmnldwg/lyscripts/compare/0.6.9...0.7.0
[0.6.9]: https://github.com/rmnldwg/lyscripts/compare/0.6.8...0.6.9
[0.6.8]: https://github.com/rmnldwg/lyscripts/compare/0.6.7...0.6.8
[0.6.7]: https://github.com/rmnldwg/lyscripts/compare/0.6.6...0.6.7
[0.6.6]: https://github.com/rmnldwg/lyscripts/compare/0.6.5...0.6.6
[0.6.5]: https://github.com/rmnldwg/lyscripts/compare/0.6.4...0.6.5
[0.6.4]: https://github.com/rmnldwg/lyscripts/compare/0.6.3...0.6.4
[0.6.3]: https://github.com/rmnldwg/lyscripts/compare/0.6.2...0.6.3
[0.6.2]: https://github.com/rmnldwg/lyscripts/compare/0.6.1...0.6.2
[0.6.1]: https://github.com/rmnldwg/lyscripts/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/rmnldwg/lyscripts/compare/0.5.11...0.6.0
[0.5.11]: https://github.com/rmnldwg/lyscripts/compare/0.5.10...0.5.11
[0.5.10]: https://github.com/rmnldwg/lyscripts/compare/0.5.9...0.5.10
[0.5.9]: https://github.com/rmnldwg/lyscripts/compare/0.5.8...0.5.9
[0.5.8]: https://github.com/rmnldwg/lyscripts/compare/0.5.7...0.5.8
[0.5.7]: https://github.com/rmnldwg/lyscripts/compare/0.5.6...0.5.7
[0.5.6]: https://github.com/rmnldwg/lyscripts/compare/0.5.5...0.5.6
[0.5.5]: https://github.com/rmnldwg/lyscripts/compare/0.5.4...0.5.5
[0.5.4]: https://github.com/rmnldwg/lyscripts/compare/0.5.3...0.5.4
[0.5.3]: https://github.com/rmnldwg/lyscripts/compare/0.5.2...0.5.3

[#2]: https://github.com/rmnldwg/lyscripts/issues/2
[#5]: https://github.com/rmnldwg/lyscripts/issues/5
[#8]: https://github.com/rmnldwg/lyscripts/issues/8
[#11]: https://github.com/rmnldwg/lyscripts/issues/11
[#13]: https://github.com/rmnldwg/lyscripts/issues/13
[#15]: https://github.com/rmnldwg/lyscripts/issues/15
[#16]: https://github.com/rmnldwg/lyscripts/issues/16
[#17]: https://github.com/rmnldwg/lyscripts/issues/17
[#20]: https://github.com/rmnldwg/lyscripts/issues/20
[#21]: https://github.com/rmnldwg/lyscripts/issues/21
[#23]: https://github.com/rmnldwg/lyscripts/issues/23
[#25]: https://github.com/rmnldwg/lyscripts/issues/25
[#30]: https://github.com/rmnldwg/lyscripts/issues/30
[#31]: https://github.com/rmnldwg/lyscripts/issues/31
[#33]: https://github.com/rmnldwg/lyscripts/issues/33
[#40]: https://github.com/rmnldwg/lyscripts/issues/40
[#41]: https://github.com/rmnldwg/lyscripts/issues/41
[#44]: https://github.com/rmnldwg/lyscripts/issues/44
[#45]: https://github.com/rmnldwg/lyscripts/issues/45
[#51]: https://github.com/rmnldwg/lyscripts/issues/51
[#54]: https://github.com/rmnldwg/lyscripts/issues/54

[`emcee`]: https://emcee.readthedocs.io/en/stable/
[`rich`]: https://rich.readthedocs.io/en/latest/
[`rich_argparse`]: https://github.com/hamdanal/rich_argparse
[LyProX]: https://lyprox.org
