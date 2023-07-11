# HEP ML Lab (HML)
[![codecov](https://codecov.io/gh/Star9daisy/hep-ml-lab/branch/main/graph/badge.svg?token=6VWJi5ct6c)](https://codecov.io/gh/Star9daisy/hml)

❗ This framework is currently undergoing **rapid iteration**. Any comments and suggestions are welcome.

## Introduction

HEP ML Lab (HML) is an end-to-end framework for applying machine learning (ML) to high energy physics (HEP)
research. It provides a set of interfaces for data generation, model training and evaluation. It is designed to
be modular and extensible so that you can easily customize it for your own research.

## Module overview

Here is a brief overview of the modules in HML:

- `hml.generators`: API of Madgraph5 for simulating colliding events;
- `hml.theories`: Particle physics models;
- `hml.observables`: General observables in jet physics;
- `hml.representations`: Different data structure used to represent an event;
- `hml.datasets`: Existing datasets and helper classes for creating new datasets;
- `hml.methods`: Cuts, trees and networks for classification;
- `hml.metrics`: Metrics used in classical signal vs background analysis;
