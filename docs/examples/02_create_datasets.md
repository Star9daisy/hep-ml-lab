# Create datasets

This guide demonstrates how to use HML and Observable to build a Representation and create a dataset for future use. With Observable, you can create and use observables not only with specific classes but also with simple strings.

Start by importing the necessary modules:

```python
from hml.generators import Madgraph5
from hml.observables import get_observable
from hml.representations import Set
from hml.datasets import TabularDataset
from hml.utils import Filter
from keras.utils import Progbar
import numpy as np
import matplotlib.pyplot as plt
```

<div class="result" markdown>

```
Welcome to JupyROOT 6.24/02
```

</div>

## Load generated events

As the previous guide showed, HML can handle three cases. Here, we use the `Madgraph5` class to fetch runs from the output directory:

```python
zjj = Madgraph5.from_output("./data/pp2zz_z2jj_z2vlvl")
qcd = Madgraph5.from_output("./data/qcd")
```

We'll use `.runs[0].events` to refer to the root file from Delphes in the event loop.

## Preselection and Representation

For the processes, we choose three observables: mass and n-subjettiness ratio of the leading fat jet, and the angular distance between the leading and subleading jets. To ensure we can obtain the observables, it’s necessary to preselect or filter events based on the number of fat jets and jets:

```python
preselections = Filter(["FatJet.Size > 0", "Jet.Size > 1"])
```

- `FatJet.Size` is the observable `Size` associated with the physics object `FatJet`. This observable refers to a collection of objects. In a root file, it applies to an entire branch. The physics object corresponds to the branch name.
- An observable is always linked to one or more physics objects. This concept inspired HML to create its own observable parsing system: `<physics_object>-<another>.<observable>`. The `physics_object` is any branch defined in your root file. Multiple objects are separated by `-`. For a single object, specify the index with `_`, for example, `Jet_0`, `Muon_1`, and so on.

Now, we use the 1D data container `Set` to hold these three observables for all events:

```python
zjj_set = Set(
    [
        get_observable("FatJet_0.Mass"),
        get_observable("FatJet_0.TauMN", m=2, n=1),
        get_observable("Jet_0-Jet_1.DeltaR"),
    ]
)

qcd_set = Set(
    [
        get_observable("FatJet_0.Mass"),
        get_observable("FatJet_0.TauMN", m=2, n=1),
        get_observable("Jet_0-Jet_1.DeltaR"),
    ]
)
```

- The pattern mentioned above can fetch an observable class anonymously.
- Each observable has several aliases: for instance, `TauMN` is an alias for `NSubjettinessRatio`, `pt, pT, PT` is an alias for `Pt`.
- Fetch observables with an external parameter to initialize them correctly.

## Event loop

Next, we loop over the events, preselect the valid ones and prepare data in `Set`:

```python
zjj_bar = Progbar(zjj.runs[0].n_events)
for i, event in enumerate(zjj.runs[0].events):
    if preselections.read_event(event).passed():
        zjj_set.read_event(event)

    zjj_bar.update(i+1)

qcd_bar = Progbar(qcd.runs[0].n_events)
for i, event in enumerate(qcd.runs[0].events):
    if preselections.read_event(event).passed():
        qcd_set.read_event(event)

    qcd_bar.update(i+1)

```

<div class="result" markdown>

```
1000/1000 [==============================] - 1s 889us/step
1000/1000 [==============================] - 1s 1ms/step
```

</div>

To confirm our choice of observables is powerful enough to differentiate the signal and background, we plot three distributions:

```python
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[0].hist(zjj_set.to_numpy()[:, 0], alpha=0.5, label="Z -> jj")
axs[0].hist(qcd_set.to_numpy()[:, 0], alpha=0.5, label="QCD dijets")
axs[0].set_title(zjj_set.names[0])

axs[1].hist(zjj_set.to_numpy()[:, 1], alpha=0.5, label="Z -> jj")
axs[1].hist(qcd_set.to_numpy()[:, 1], alpha=0.5, label="QCD dijets")
axs[1].set_title(zjj_set.names[1])

axs[2].hist(zjj_set.to_numpy()[:, 2], alpha=0.5, label="Z -> jj")
axs[2].hist(qcd_set.to_numpy()[:, 2], alpha=0.5, label="QCD dijets")
axs[2].set_title(zjj_set.names[2])
axs[2].legend()

plt.tight_layout()
plt.show()
```

<div class="result" markdown>

![observable_distributions](../images/observable_distributions.png)

</div>

## Pack things up

Lastly, we create our dataset:

```python
samples = np.array(zjj_set.values + qcd_set.values, "float32")
targets = np.array([1] * len(zjj_set.values) + [0] * len(qcd_set.values), "int32")
dataset = TabularDataset(
    samples=samples,
    targets=targets,
    feature_names=zjj_set.names,
    target_names=["Z -> jj", "QCD dijets"],
    description="Z -> jj vs QCD dijets",
)

dataset.save("./data/zjj_vs_qcd")
```

- `samples` represent all data points, while `targets` represent the integer number assigned to each class.
- Utilize `feature_names` and `target_names` to enhance the readability of your data.
- Include a brief `description` for your dataset.

Check the doc to learn more about [observables](../api-reference/hml.observables.md), [representations](../api-reference/hml.representations.md) and [datasets](../api-reference/hml.datasets.md).
