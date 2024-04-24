# History

### v0.4.0
This version refactors most of the codebase to make it compatible with the array
(from `awkward` and `uproot`) representation of the data.

## v0.3.0.1
- Fix a bug that Madgraph5 may run into an infinite loop caused by HML keeping
  removing py.py file during initialization.
- Fix nan value not implemented in Fileter.
- Fix the wrong order of runs when using `hml.generators.Madgraph5.runs` and
  `hml.generators.Madgraph5.summary`.
- Fix the typo "g1" in quickstart.

## v0.3.0
- New Madgraph5 API now is closer to the original Madgraph5 CLI.
- New Observable parsing system makes it easier to use and define new observables.
- New CutAndCout and BoostedDecisionTree in Keras style.

## v0.2.2
- Change output structure of `hml.generators.Madgraph5` to ensure reproducibility.
- Refactor `hml.generators.Madgraph5` and `hml.generators.MG5Run` to make
  them more robust.
## v0.2.1
- Add `summary` to `hml.generators.Madgraph5` to print a summary of all run.
- Add `remove` to `hml.generators.Madgraph5` to remove a run.
- Add `clean` to `hml.generators.Madgraph5` to remove the output directory.