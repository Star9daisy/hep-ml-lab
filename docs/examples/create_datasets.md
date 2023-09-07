# Create datasets

This notebook shows how to convert events of ROOT branches into different representations to prepare
a sample and collect them into a dataset.

## Introduction to representations

Data representations are data structures to store data. There are usually three representations in
high energy physics: Set, Image, and Graph.

Set is a 1D representation of events, which contains a set of observables of physics objects.
Observables are designed variables to refect the properties of events. For example, the invariant
mass of dijet indicate the middle particle; N-subjettiness indicates the number of subjets in a jet.
Representing events in Set is actively used in a large number of phenomenological studies.
Observables as high-level low-dimensional features are usually designed with physics insight and
expertise. Set is usually used in traditional machine learning methods, such as cut-based analysis,
decision tree, and so on.

Image is a 2D (gray scale) or 3D (RGB) representation. From the aspect of detectors, they are like
a giant camera to take pictures of final stable particles. Then these particles naturally form a 2D
image whose pixel intensity is the energy deposit of particles or other particle-related features,
and width and height are $\eta-\phi$ (pseudorapidity and azimuthal angle plane). Image could reflect
the spatial characteristics of events, which is suitable for convolutional neural networks (CNNs).
Its information is more complete than Set, but it is usually a sparse matrix, which is not storeage
efficient.

Graph is a 2D representation. A graph consists of nodes and edges. Here nodes are particles and
edges are the relationship between particles (e.g. the distance between particles in $\eta-\phi$
plane). Graph as a low-level high-dimensional representation, contains all the details of events,
which makes it most suitable for fully exploring potential of new physics and machine learning
techniques. Graph is usually used in graph neural networks (GNNs).

## Generate events for signal and background

To get started, create events for signal (pp > ZZ > jjveve) and background
(pp > jj) using HML MG5 API:

```py title="notebook.ipynb"
signal_generator = Madgraph5(
    executable="mg5_aMC",
    processes=["p p > z z, z > j j, z > ve ve~"],
    output="./data/pp2zz",
    shower="Pythia8",
    detector="Delphes",
    settings={"htjmin": 400}
)

background_generator = Madgraph5(
    executable="mg5_aMC",
    processes=["p p > j j / z"],
    output="./data/pp2jj",
    shower="Pythia8",
    detector="Delphes",
    settings={"htjmin": 400}
)

signal_generator.launch(show_status=False)
signal_generator.summary()
background_generator.launch(show_status=False)
background_generator.summary()
```

<div class="result" markdown>

```
                  p p > z z, z > j j, z > ve ve~                   
┏━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name     ┃ Tag   ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_1[1] │ tag_1 │ 7.703e-04 +- 3.118e-06 │   10,000 │   42 │
└───┴──────────┴───────┴────────────────────────┴──────────┴──────┘
                        Output: data/pp2zz                         
                           p p > j j / z                           
┏━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name     ┃ Tag   ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_1[1] │ tag_1 │ 5.685e+04 +- 1.283e+02 │   10,000 │   42 │
└───┴──────────┴───────┴────────────────────────┴──────────┴──────┘
                        Output: data/pp2jj                         
```

## Loop over events

Madgraph5 of HML has `runs` attribute and each `run` has `events` attribute to
access the output events in `.root` files. Runs are actually parsed by `MG5Run`
class, which is initialized by the run directory. 

!!! note
    If you prefer to separate the events generation and dataset creation into
    two scripts, it's a better idea to use `MG5Run` to access all the
    information of a run, otherwise using the `runs` attribute of `Madgraph5` is
    enough.

Declare a `Representation` object to extract information during the event loop:

```py title="notebook.ipynb"
from hml.representations import Set
from hml.observables import Pt, M, DeltaR

representation = Set(
    [
        Pt("Jet1"),
        Pt("Jet2"),
        DeltaR("Jet1", "Jet2"),
        M("FatJet1"),
    ]
)
```

Use two lists to store data and target, where data is the representation of
events and target is the label of events (1 for signal and 0 for background):

```py title="notebook.ipynb"
sig_run = signal_generator.runs[0]
bkg_run = background_generator.runs[0]

data, target = [], []

for event in sig_run.events:
    if event.Jet_size >= 2 and event.FatJet_size >= 1:
        representation.from_event(event)
        data.append(representation.values)
        target.append(1)

for event in bkg_run.events:
    if event.Jet_size >= 2 and event.FatJet_size >= 1:
        representation.from_event(event)
        data.append(representation.values)
        target.append(0)
```

## Create datasets

```py title="notebook.ipynb"
import numpy as np
from hml.datasets import Dataset


data = np.array(data, dtype=np.float32)
target = np.array(target, dtype=np.int32)

dataset = Dataset(
    data,
    target,
    feature_names=representation.names,
    target_names=["pp2jj", "pp2zz"],
    description="Z vs QCD jets",
    dir_path="./data/z_vs_qcd",
)
```

!!! note
    The `Dataset` class is a wrapper of `sklearn.datasets.base.Bunch` and
    provides some useful methods to save and load datasets.

Save the dataset to `./data/z_vs_qcd`:
    
```py title="notebook.ipynb"
dataset.save()
```