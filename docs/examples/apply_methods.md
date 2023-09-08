# Apply methods

In this notebook we will show how to load dataset saved in the previous notebook
and apply built-in methods on it. Finally we summarize their performance into a
table

## Introduction to built-in methods

Currently `hml` have three types of methods: cuts, trees, and (neural) networks.

With `hml.methods.cuts.CutAndCount`, we apply a series of cuts on the input data
to select as many signal events and as few background events as possible. Each
cut reduces the number of background events and inevitably also signal events.
The goal usually is to find a set of cuts that maximizes the significance.

The boosted decision tree is one of trees methods. It is a machine learning
method commonly used in high energy physics. The name "boosted" comes from the
idea to combine weak classifiers into a strong one. 

The neural network now only contains a simple fully connected neural network
named `ToyMLP`.

## Load the dataset

First we load the dataset from the previous notebook.

``` py title="notebook.ipynb"
from hml.datasets import Dataset
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
```

To load dataset, we use the class method `load` of `Dataset` class. The method
takes the dataset directory as input and returns a `Dataset` object.

``` py title="notebook.ipynb"
# Split the data into training and testing sets
dataset = Dataset.load("./data/z_vs_qcd")

x_train, x_test, y_train, y_test = train_test_split(
    dataset.data, dataset.target, test_size=0.2, random_state=42
)

# Convert the labels to categorical
y_train = to_categorical(y_train, dtype="int32")
y_test = to_categorical(y_test, dtype="int32")

# Show the shape of the training and testing sets
print("> Train and test shapes:")
print("x_train shape:", x_train.shape, "y_train shape:", y_train.shape)
print("x_test shape:", x_test.shape, "y_test shape:", y_test.shape)
print(f"> target names: {dataset.target_names}")
```

<div class="result" markdown>

```
> Train and test shapes:
x_train shape: (12889, 4) y_train shape: (12889, 2)
x_test shape: (3223, 4) y_test shape: (3223, 2)
> target names: ['pp2jj', 'pp2zz']
```

</div>

## Apply methods

Then we apply a boosted decision tree. It comes from `scikit-learn` package
originally. The `compile` method takes loss function name, optimizer name, and a
list of metrics as input. Here we use default parameters as in `scikit-learn`.

``` py title="notebook.ipynb"
from hml.methods import CutAndCount, BoostedDecisionTree, ToyMLP
from keras.losses import CategoricalCrossentropy
from keras.metrics import CategoricalAccuracy
from hml.metrics import MaxSignificance, RejectionAtEfficiency
```

``` py title="notebook.ipynb"
method1 = BoostedDecisionTree(n_estimators=10)
method1.compile(
    metrics=[
        CategoricalAccuracy(name="acc"),
        MaxSignificance(name="max_sig"),
        RejectionAtEfficiency(name="r50"),
    ]
)

print("> Training model:")
history = method1.fit(x_train, y_train)
```

<div class="result" markdown>

```
> Training model:
Iter 1/10 - loss: 1.2124 - acc: 0.8815 - max_sig: 193.1740 - r50: 356.5397
Iter 2/10 - loss: 1.0794 - acc: 0.9131 - max_sig: 254.9458 - r50: 122.9463
Iter 3/10 - loss: 0.9685 - acc: 0.9283 - max_sig: 310.2836 - r50: 293.0483
Iter 4/10 - loss: 0.8748 - acc: 0.9358 - max_sig: 354.9109 - r50: 180.5289
Iter 5/10 - loss: 0.7942 - acc: 0.9413 - max_sig: 383.2777 - r50: 256.5062
Iter 6/10 - loss: 0.7231 - acc: 0.9455 - max_sig: 418.4313 - r50: 270.7895
Iter 7/10 - loss: 0.6598 - acc: 0.9492 - max_sig: 451.7975 - r50: 230.0276
Iter 8/10 - loss: 0.6051 - acc: 0.9516 - max_sig: 489.0055 - r50: 352.1394
Iter 9/10 - loss: 0.5573 - acc: 0.9538 - max_sig: 523.7005 - r50: 307.0688
Iter 10/10 - loss: 0.5143 - acc: 0.9557 - max_sig: 556.1749 - r50: 367.5613
```

</div>

``` py title="notebook.ipynb"
method2 = CutAndCount()
method2.compile(
    loss=CategoricalCrossentropy(),
    metrics=[
        CategoricalAccuracy(name="acc"),
        MaxSignificance(name="max_sig"),
        RejectionAtEfficiency(name="r50"),
    ],
)
print("> Training model:")
history = method2.fit(x_train, y_train)
```

<div class="result" markdown>

```
> Training model:
Cut 1/4 - loss: 2.0946 - acc: 0.8700 - max_sig: 109.0580 - r50: 7.3591
Cut 2/4 - loss: 2.1672 - acc: 0.8678 - max_sig: 168.8623 - r50: 14.2052
Cut 3/4 - loss: 3.7816 - acc: 0.8337 - max_sig: 204.4822 - r50: 21.2865
Cut 4/4 - loss: 4.4206 - acc: 0.8067 - max_sig: 231.2802 - r50: 28.3538
```

</div>

``` py title="notebook.ipynb"
method3 = ToyMLP(input_shape=(x_train.shape[1],))
method3.compile(
    loss=CategoricalCrossentropy(),
    metrics=[
        CategoricalAccuracy(name="acc"),
        MaxSignificance(name="max_sig"),
        RejectionAtEfficiency(name="r50"),
    ],
)

print("> Training model:")
history = method3.fit(x_train, y_train, epochs=10, batch_size=256, verbose=2)
```

<div class="result" markdown>

```
> Training model:
Epoch 1/10
51/51 - 6s - loss: 1.4079 - acc: 0.8544 - max_sig: 125.3569 - r50: 17.0191 - 6s/epoch - 114ms/step
Epoch 2/10
51/51 - 1s - loss: 0.7214 - acc: 0.8857 - max_sig: 212.3330 - r50: 37.1405 - 888ms/epoch - 17ms/step
Epoch 3/10
51/51 - 1s - loss: 0.7479 - acc: 0.8806 - max_sig: 232.3429 - r50: 34.9558 - 841ms/epoch - 16ms/step
Epoch 4/10
51/51 - 1s - loss: 0.6934 - acc: 0.8820 - max_sig: 224.1893 - r50: 52.4336 - 882ms/epoch - 17ms/step
Epoch 5/10
51/51 - 1s - loss: 0.5860 - acc: 0.8959 - max_sig: 243.3809 - r50: 68.5670 - 874ms/epoch - 17ms/step
Epoch 6/10
51/51 - 1s - loss: 0.6265 - acc: 0.8904 - max_sig: 223.1910 - r50: 72.7648 - 847ms/epoch - 17ms/step
Epoch 7/10
51/51 - 1s - loss: 0.5457 - acc: 0.9022 - max_sig: 216.2077 - r50: 79.2329 - 830ms/epoch - 16ms/step
Epoch 8/10
51/51 - 1s - loss: 0.5250 - acc: 0.9019 - max_sig: 230.6327 - r50: 100.4355 - 860ms/epoch - 17ms/step
Epoch 9/10
51/51 - 1s - loss: 0.4902 - acc: 0.9090 - max_sig: 243.8243 - r50: 113.1893 - 858ms/epoch - 17ms/step
Epoch 10/10
51/51 - 1s - loss: 0.4611 - acc: 0.9078 - max_sig: 246.4039 - r50: 99.0404 - 851ms/epoch - 17ms/step

```

</div>

## Compare the performance

Finally we compare the performance of the three methods. We use the `evaluate`
to evaluate the performance via the loss and metrics we specified in the
`compile` method. The `evaluate` method returns a dictionary of the loss and
metrics.

Here we use the `tabulate` function from `tabulate` package to summarize the
performance into a table.

``` py title="notebook.ipynb"
from tabulate import tabulate

results1 = method1.evaluate(x_test, y_test)
results2 = method2.evaluate(x_test, y_test)
results3 = method3.evaluate(x_test, y_test, verbose=2)
results = {}
```

<div class="result" markdown>

```
loss: 0.2572 - acc: 0.9568 - max_sig: 580.2705 - r50: 491.3567
loss: 4.4158 - acc: 0.7977 - max_sig: 244.1590 - r50: 31.8965
101/101 - 2s - loss: 0.2068 - acc: 0.9383 - max_sig: 112.4101 - r50: 161.9975 - 2s/epoch - 16ms/step
```

</div>

``` py title="notebook.ipynb"
from rich.table import Table

table = Table("name", "loss", "acc", "max_sig", "r50")
names = ["BDT", "CutAndCount", "ToyMLP"]
for res, name in zip([results1, results2, results3], names):
    table.add_row(name, *[f"{v[0]:.4f}" for v in res.values()])

table
```

<div class="result" markdown>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">┏━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃<span style="font-weight: bold"> name        </span>┃<span style="font-weight: bold"> loss   </span>┃<span style="font-weight: bold"> acc    </span>┃<span style="font-weight: bold"> max_sig  </span>┃<span style="font-weight: bold"> r50      </span>┃
┡━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ BDT         │ 0.2572 │ 0.9568 │ 580.2705 │ 491.3567 │
│ CutAndCount │ 4.4158 │ 0.7977 │ 244.1590 │ 31.8965  │
│ ToyMLP      │ 0.2068 │ 0.9383 │ 112.4101 │ 161.9975 │
└─────────────┴────────┴────────┴──────────┴──────────┘
</pre>

</div>

---

Check [cuts](../../api-reference/hml.methods/cuts),
[trees](../../api-reference/hml.methods/trees), and
[mlps](../../api-reference/hml.methods/networks/mlps) for more details.
