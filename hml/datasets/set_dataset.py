from __future__ import annotations

import json
import zipfile
from functools import reduce
from io import BytesIO

import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from hml.approaches import Cut
from hml.observables import Observable
from hml.representations import Set


class SetDataset:
    def __init__(self, observables: list[str | Observable]):
        self.set = Set(observables)
        self.been_split = False
        self.seed = None

        self._samples = []
        self._targets = []
        self.train = None
        self.test = None
        self.val = None

        self._data = None
        self._been_read = False

    def read(self, events, target, cuts: list[str | Cut] | None = None):
        self.set.read(events)
        if cuts is not None:
            compiled_cuts = []
            for i in cuts:
                if isinstance(i, str):
                    compiled_cuts.append(Cut(i).read(events).value)
                else:
                    compiled_cuts.append(i.read(events).value)

            mask = reduce(np.logical_and, compiled_cuts)
            set_values = self.set.values[mask]
        else:
            set_values = self.set.values

        if isinstance(self._samples, list):
            self._samples = set_values
        else:
            self._samples = ak.concatenate([self._samples, set_values])

        if isinstance(self._targets, list):
            self._targets = ak.values_astype(
                ak.Array([target] * len(set_values)), "int32"
            )
        else:
            self._targets = ak.concatenate(
                [
                    self._targets,
                    ak.values_astype(ak.Array([target] * len(set_values)), "int32"),
                ]
            )

    def split(self, train, test, val=None, seed=None):
        train *= 10
        test *= 10
        samples = self.samples
        targets = self.targets
        self.seed = seed

        if val is None:
            if train + test != 10:
                raise ValueError("train + test must be 1")

        x_train, x_test, y_train, y_test = train_test_split(
            samples,
            targets,
            test_size=test / 10,
            random_state=seed,
        )

        if val is not None:
            val *= 10
            if train + test + val != 10:
                raise ValueError("train + test + val must be 1")

            x_train, x_val, y_train, y_val = train_test_split(
                x_train,
                y_train,
                test_size=val / (train + val),
                random_state=seed,
            )

            self.val = SetDataset(self.set.observables)
            self.val._samples = x_val
            self.val._targets = y_val

        self.train = SetDataset(self.set.observables)
        self.train._samples = x_train
        self.train._targets = y_train
        self.test = SetDataset(self.set.observables)
        self.test._samples = x_test
        self.test._targets = y_test

        self.been_split = True

    def save(self, filepath="dataset.ds"):
        configs = self.config
        configs_json = json.dumps(configs)

        npz_data = BytesIO()
        np.savez(npz_data, samples=self.samples, targets=self.targets)
        npz_data.seek(0)

        with zipfile.ZipFile(filepath, "w") as zf:
            zf.writestr("configs.json", configs_json)
            zf.writestr("data.npz", npz_data.read())

            if self.been_split:
                npz_train = BytesIO()
                self.train.save(npz_train)
                npz_train.seek(0)
                zf.writestr("train.ds", npz_train.read())

                npz_test = BytesIO()
                self.test.save(npz_test)
                npz_test.seek(0)
                zf.writestr("test.ds", npz_test.read())

                if self.val is not None:
                    npz_val = BytesIO()
                    self.val.save(npz_val)
                    npz_val.seek(0)
                    zf.writestr("val.ds", npz_val.read())

    @classmethod
    def load(cls, filepath, lazy=True):
        zf = zipfile.ZipFile(filepath)
        # Extract and read configs JSON
        with zf.open("configs.json") as json_file:
            configs = json.load(json_file)

        dataset = cls.from_config(configs)
        dataset._filepath = filepath
        dataset._data = zf.open("data.npz")

        # Extract and load .npz file
        if not lazy:
            with dataset._data as split_zf:
                split_data = np.load(BytesIO(split_zf.read()))
                dataset._samples = split_data["samples"]
                dataset._targets = split_data["targets"]
                dataset._been_read = True

        # Extract and load train, test, and val .npz files
        if configs["been_split"]:
            dataset.train = cls.load(zf.open("train.ds"), lazy=lazy)
            dataset.test = cls.load(zf.open("test.ds"), lazy=lazy)

            if "val.ds" in [i.filename for i in zf.filelist]:
                dataset.val = cls.load(zf.open("val.ds"), lazy=lazy)

        return dataset

    @property
    def samples(self):
        if len(self._samples) == 0 and not self._been_read and self._data is not None:
            split_data = np.load(BytesIO(self._data.read()))
            self._samples = split_data["samples"]
            self._data.seek(0)

        if len(self._samples) > 0 and len(self._targets) > 0:
            self._been_read = True

        # return np.array(self._samples, dtype=np.float32)
        nan_float32 = np.array(np.nan, dtype=np.float32)
        return ak.to_numpy(ak.fill_none(self._samples, nan_float32))
        # return ak.to_numpy(self._samples, allow_missing=False)

    @property
    def targets(self):
        if len(self._targets) == 0 and not self._been_read and self._data is not None:
            split_data = np.load(BytesIO(self._data.read()))
            self._targets = split_data["targets"]
            self._data.seek(0)

        if len(self._samples) > 0 and len(self._targets) > 0:
            self._been_read = True

        # return np.array(self._targets, dtype=np.int32)
        nan_float32 = np.array(np.nan, dtype=np.float32)
        return ak.to_numpy(ak.fill_none(self._targets, nan_float32))
        # return ak.to_numpy(self._targets, allow_missing=False)

    @property
    def feature_names(self):
        return self.set.names

    def to_numpy(self):
        return np.hstack([self.samples, self.targets[:, None]])

    def to_pandas(self):
        df = pd.DataFrame(self.samples.tolist(), columns=self.feature_names)
        df["Target"] = self.targets
        return df

    @property
    def config(self):
        config = self.set.config
        config.update(
            {
                "class_name": self.__class__.__name__,
                "been_split": self.been_split,
                "seed": self.seed,
            }
        )

        return config

    @classmethod
    def from_config(cls, config):
        set = Set.from_config(config)

        instance = cls(set.observables)
        instance.been_split = config["been_split"]
        instance.seed = config["seed"]

        return instance

    def show(self, n_feature_per_line=3, n_samples=-1, target=None):
        if n_samples != -1:
            samples = self.samples[:n_samples]
        else:
            samples = self.samples

        n_features = len(self.feature_names)
        n_rows = (n_features + n_feature_per_line - 1) // n_feature_per_line
        plt.figure(figsize=(4 * n_feature_per_line, 3 * n_rows))
        for i, name in enumerate(self.feature_names):
            ax = plt.subplot(n_rows, n_feature_per_line, i + 1)

            if target is None:
                for i_target in np.unique(self.targets):
                    ax.hist(
                        samples[np.squeeze(self.targets == i_target)][:, i],
                        bins=50,
                        histtype="step",
                        label=f"Target {i_target}",
                    )
            else:
                ax.hist(
                    samples[np.squeeze(self.targets == i_target)][:, i],
                    bins=50,
                    histtype="step",
                    label=f"Target {i_target}",
                )
            ax.set_title(name)

        plt.legend()
        plt.tight_layout()
        plt.show()
