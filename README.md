# HEP ML Lab (HML)
![codecov](https://codecov.io/gh/Star9daisy/hep-ml-lab/branch/main/graph/badge.svg?token=6VWJi5ct6c)

❗ This framework is currently undergoing **rapid iteration**. Any comments and suggestions are welcome.

## Introduction
HEP ML Lab (HML) is an end-to-end framework for applying machine learning (ML)
to high energy physics (HEP) research. It provides a set of interfaces for data generation, model training and evaluation. It is designed to be modular and
extensible so that you can easily customize it for your own research.

## Installation
```python
pip install hep-ml-lab
```

## Usage
Check out the [documents](https://star9daisy.github.io/hep-ml-lab/).

## Module overview
- `hml.generators`: API of Madgraph5 for simulating colliding events;
- `hml.theories`: Particle physics models;
- `hml.observables`: General observables in jet physics;
- `hml.representations`: Different data structure used to represent an event;
- `hml.datasets`: Existing datasets and helper classes for creating new datasets;
- `hml.methods`: Cuts, trees and networks for classification;
- `hml.metrics`: Metrics used in classical signal vs background analysis;

## Updates
### v0.2.1
- Add `summary` to `hml.generators.Madgraph5` to print a summary of all run.
- Add `remove` to `hml.generators.Madgraph5` to remove a run.
- Add `clean` to `hml.generators.Madgraph5` to remove the output directory.