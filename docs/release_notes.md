# Release notes

## v0.4.3
- Fix the thresholds issue in `hml.metrics.MaxSignificance` by making it similar to the one returned by `sklearn.metrics.roc_curve`.
- Change `hml.datasets.SetDataset.show` to display figures using `seaborn`. 
- Drop the requirement of `executable` in `hml.generators.Madgraph5.from_output`.

## v0.4.2
- Fix parsing cuts like "muon0.charge != muon1.charge".
- Fix inconsistent model layers in `hml.approaches.networks.SimpleCNN`.
- Fix registering and saving custom observables.
- Add cross sections, luminosity and weights as parameters in `hml.metrics.MaxSignificance`.
- Improve the figure ratio in `hml.datasets.SetDataset.show`.

## v0.4.1
- Fix module overview image in README.
- Fix `GradientBoostedDecisionTree` to be compatible with different `sklearn` versions.
- Fix `hml.datasets.SetDataset.show` to display the correct rows and columns.
- Rename the `parse` and `register` functions to `parse_physics_object`, `parse_observable`, and `register_observable`.
- Update the installation document.

## v0.4.0
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