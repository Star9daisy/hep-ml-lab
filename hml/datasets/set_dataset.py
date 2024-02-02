import json
import zipfile
from io import BytesIO

import numpy as np
import pandas as pd
from numpy.lib.npyio import NpzFile
from sklearn.model_selection import train_test_split

from hml.representations import Set
from hml.types import Observable, PathLike
from hml.utils import get_observable


class SetDataset:
    def __init__(self, *observables: str | Observable):
        self.set = Set(*observables)
        self._samples = []
        self._targets = []
        self.been_split = False
        self.train = None
        self.test = None
        self.val = None
        self.seed = None

        self._data = None
        self._been_read = False

    def read_ttree(self, event, target):
        self.set.read_ttree(event)
        self._samples.append(self.set.values)
        self._targets.append([target])

    def split(self, train, test, val=None, seed=None):
        train *= 10
        test *= 10
        samples = self.samples
        targets = self.targets

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

            self.val = SetDataset(*self.set.observables)
            self.val._samples = x_val
            self.val._targets = y_val

        self.train = SetDataset(*self.set.observables)
        self.train._samples = x_train
        self.train._targets = y_train
        self.test = SetDataset(*self.set.observables)
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
        if self._samples == [] and not self._been_read:
            with self._data as split_zf:
                split_data = np.load(BytesIO(split_zf.read()))
                self._samples = split_data["samples"]
                self._targets = split_data["targets"]

            self._been_read = True

        return np.array(self._samples, dtype=np.float32)

    @property
    def targets(self):
        if self._targets == [] and not self._been_read:
            with self._data as split_zf:
                split_data = np.load(BytesIO(split_zf.read()))
                self._samples = split_data["samples"]
                self._targets = split_data["targets"]

            self._been_read = True

        return np.array(self._targets, dtype=np.int32)

    @property
    def feature_names(self):
        return self.set.names

    def to_numpy(self):
        return np.hstack([self.samples, self.targets])

    def to_pandas(self):
        df = pd.DataFrame(self.samples, columns=self.feature_names)
        df["Target"] = self.targets
        return df

    @property
    def config(self):
        config = self.set.config
        config.update(
            {
                "been_split": self.been_split,
                "seed": self.seed,
            }
        )

        return config

    @classmethod
    def from_config(cls, config):
        set = Set.from_config(config)

        instance = cls(*set.observables)
        instance.been_split = config["been_split"]
        instance.seed = config["seed"]

        return instance
