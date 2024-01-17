import json
import zipfile
from io import BytesIO

import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

from hml.representations import Image


class ImageDataset:
    def __init__(self, representation: Image):
        self.image = representation
        self._samples = []
        self._targets = []
        self.been_split = False
        self.train = None
        self.test = None
        self.val = None
        self.seed = None

        self._data = None
        self._been_read = False

    def read(self, event, target):
        self.image.read(event)
        if self.image.status:
            self._samples.append(self.image.values)
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

            self.val = ImageDataset(representation=self.image)
            self.val._samples = x_val
            self.val._targets = y_val

        self.train = ImageDataset(representation=self.image)
        self.train._samples = x_train
        self.train._targets = y_train
        self.test = ImageDataset(representation=self.image)
        self.test._samples = x_test
        self.test._targets = y_test

        self.been_split = True

    def save(self, filepath="dataset.ds"):
        configs = {
            "height": self.image.height,
            "width": self.image.width,
            "channel": self.image.channel,
            "registered_methods": self.image.registered_methods,
            "been_split": self.been_split,
            "seed": self.seed,
        }
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

        dataset = cls(*configs["observables"])
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
    def features(self):
        return {
            "height": self.image.height,
            "width": self.image.width,
            "channel": self.image.channel,
        }

    def show(
        self,
        show_pixels=False,
        grid=True,
        norm=None,
        n_samples=10000,
    ):
        plt.figure()
        # Use pcolormesh instead of imshow so that the actual values of bins
        # are shown.
        plt.pcolormesh(
            self.image.w_bins,
            self.image.h_bins,
            self.samples[:n_samples].sum(0).T,
            norm=norm,
            cmap="jet",
        )

        # Turn on colorbar to show the range of values.
        plt.colorbar()

        if show_pixels:
            # Turn off ticks and labels.
            plt.tick_params(
                bottom=False, left=False, labelbottom=False, labelleft=False
            )
            plt.xticks(self.image.w_bins)
            plt.yticks(self.image.h_bins)

        # Set aspect ratio to be equal so that every pixel is square.
        # Ignore the actual values of bins since here is just a schematic.
        plt.gca().set_aspect("equal")

        # Turn on grid to show pixel boundaries.
        if grid:
            plt.grid(alpha=0.5)

        plt.show()
