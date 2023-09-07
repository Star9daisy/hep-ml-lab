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
51/51 - 6s - loss: 3.5999 - acc: 0.8404 - max_sig: 148.5871 - r50: 19.1179 - 6s/epoch - 117ms/step
Epoch 2/10
51/51 - 1s - loss: 0.8697 - acc: 0.8880 - max_sig: 204.6640 - r50: 22.9292 - 890ms/epoch - 17ms/step
Epoch 3/10
51/51 - 1s - loss: 0.7783 - acc: 0.8925 - max_sig: 205.9824 - r50: 40.2879 - 914ms/epoch - 18ms/step
Epoch 4/10
51/51 - 1s - loss: 0.7782 - acc: 0.8917 - max_sig: 204.7205 - r50: 29.8367 - 909ms/epoch - 18ms/step
Epoch 5/10
51/51 - 1s - loss: 0.8271 - acc: 0.8844 - max_sig: 216.8438 - r50: 29.9621 - 911ms/epoch - 18ms/step
Epoch 6/10
51/51 - 1s - loss: 0.6507 - acc: 0.8993 - max_sig: 224.2558 - r50: 47.2250 - 916ms/epoch - 18ms/step
Epoch 7/10
51/51 - 1s - loss: 0.6414 - acc: 0.8984 - max_sig: 228.0864 - r50: 45.7113 - 909ms/epoch - 18ms/step
Epoch 8/10
51/51 - 1s - loss: 0.6198 - acc: 0.9009 - max_sig: 230.9593 - r50: 52.4336 - 910ms/epoch - 18ms/step
Epoch 9/10
51/51 - 1s - loss: 0.6494 - acc: 0.9006 - max_sig: 225.9335 - r50: 35.6549 - 919ms/epoch - 18ms/step
Epoch 10/10
51/51 - 1s - loss: 0.5166 - acc: 0.9062 - max_sig: 226.5588 - r50: 64.2429 - 913ms/epoch - 18ms/step
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

results['name'] = [method1.name, method2.name, method3.name]
for k in results1.keys():
    results[k] = results1[k] + results2[k] + results3[k]

print("> Results:")
print(tabulate(results, headers="keys", floatfmt=".4f"))
```

<div class="result" markdown>

```
loss: 0.2572 - acc: 0.9561 - max_sig: 564.3209 - r50: 507.5595
loss: 4.4158 - acc: 0.8019 - max_sig: 237.7650 - r50: 30.1252
101/101 - 4s - loss: 3.5514 - acc: 0.4471 - max_sig: 92.3069 - r50: 1.2307 - 4s/epoch - 39ms/step
> Results:
name                     loss     acc    max_sig       r50
---------------------  ------  ------  ---------  --------
boosted_decision_tree  0.2572  0.9561   564.3209  507.5595
cut_and_count          4.4158  0.8019   237.7650   30.1252
toy_mlp                3.5514  0.4471    92.3069    1.2307
```

</div>
