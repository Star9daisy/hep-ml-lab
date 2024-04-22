from __future__ import annotations

import json
import zipfile
from functools import reduce
from io import BytesIO

import awkward as ak
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

from hml.approaches import Cut
from hml.representations import Image


class ImageDataset:
    def __init__(self, representation: Image):
        self.image = representation
        self._samples = [] if self.image.been_pixelated else [[], []]
        self._targets = []
        self.been_split = False
        self.train = None
        self.test = None
        self.val = None
        self.seed = None

        self._data = None
        self._been_read = None

    def read(self, events, target, cuts: list[str | Cut] | None = None):
        self.image.read(events)
        if cuts is not None:
            compiled_cuts = []
            for i in cuts:
                if isinstance(i, str):
                    compiled_cuts.append(Cut(i).read(events).value)
                else:
                    compiled_cuts.append(i.read(events).value)
            mask = reduce(np.logical_and, compiled_cuts)

            if self.image.been_pixelated:
                image_values = self.image.values[mask]
            else:
                image_values = [self.image.values[0][mask], self.image.values[1][mask]]
        else:
            image_values = self.image.values

        if self.image.status:
            if isinstance(self._samples, list):
                self._samples = image_values
            else:
                self._samples = ak.concatenate([self._samples, image_values])

            if self.image.been_pixelated:
                if isinstance(self._targets, list):
                    self._targets = ak.values_astype(
                        ak.Array([target] * len(image_values)), "int32"
                    )
                else:
                    self._targets = ak.concatenate(
                        [
                            self._targets,
                            ak.values_astype(
                                ak.Array([target] * len(image_values)), "int32"
                            ),
                        ]
                    )

            else:
                if isinstance(self._targets, list):
                    self._targets = ak.values_astype(
                        ak.Array([target] * len(image_values[0])), "int32"
                    )
                else:
                    self._targets = ak.concatenate(
                        [
                            self._targets,
                            ak.values_astype(
                                ak.Array([target] * len(image_values[0])), "int32"
                            ),
                        ]
                    )
                # self._samples[0].append(self.image.values[0])
                # self._samples[1].append(self.image.values[1])

        # if cut is not None:
        #     self._cut = cut
        #     self._targets = self._targets[cut]
        #     if self.image.been_pixelated:
        #         self._samples = self._samples[cut]
        #     else:
        #         self._samples = list(self._samples)
        #         self._samples[0] = self._samples[0][cut]
        #         self._samples[1] = self._samples[1][cut]

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
        else:
            dataset._been_read = False

        # Extract and load train, test, and val .npz files
        if configs["been_split"]:
            dataset.train = cls.load(zf.open("train.ds"), lazy=lazy)
            dataset.test = cls.load(zf.open("test.ds"), lazy=lazy)

            if "val.ds" in [i.filename for i in zf.filelist]:
                dataset.val = cls.load(zf.open("val.ds"), lazy=lazy)

        return dataset

    @property
    def samples(self):
        if self._been_read is False and self._data is not None:
            split_data = np.load(BytesIO(self._data.read()))
            self._samples = split_data["samples"]
            self._data.seek(0)

            if np.array(self._samples).size > 0 and np.array(self._targets).size > 0:
                self._been_read = True

        if self.image.been_pixelated:
            return np.array(self._samples, dtype=np.float32)
        else:
            height = ak.from_iter(self._samples[0])
            width = ak.from_iter(self._samples[1])

            # 1D non-pixelated data should come from a loaded dataset
            if height.ndim == 1:
                height = ak.to_numpy(height)
                width = ak.to_numpy(width)

            # 2D non-pixelated data should come from an event loop
            else:
                height = ak.to_numpy(ak.flatten(height))
                width = ak.to_numpy(ak.flatten(width))

            return height, width

    @property
    def targets(self):
        if self._been_read is False and self._data is not None:
            split_data = np.load(BytesIO(self._data.read()))
            self._targets = split_data["targets"]
            self._data.seek(0)

            if np.array(self._samples).size > 0 and np.array(self._targets).size > 0:
                self._been_read = True

        return np.array(self._targets, dtype=np.int32)

    @property
    def features(self):
        return {
            "height": self.image.height.name,
            "width": self.image.width.name,
            "channel": self.image.channel.name if self.image.channel else None,
        }

    def show(
        self,
        limits=None,
        show_pixels=False,
        grid=True,
        norm=None,
        n_samples=-1,
        target=None,
    ):
        if target is not None and self.image.been_pixelated:
            samples = self.samples[np.squeeze(self.targets) == target]

        else:
            samples = self.samples

        plt.figure()

        if not self.image.been_pixelated:
            plt.scatter(
                x=samples[1][:n_samples],
                y=samples[0][:n_samples],
                c="k",
                s=10,
                marker="o",
            )

            # Restrict the range of axes.
            if limits is not None:
                plt.xlim(limits[0])
                plt.ylim(limits[1])

        else:
            # Use pcolormesh instead of imshow so that the actual values of bins
            # are shown.
            plt.pcolormesh(
                self.image.w_bins,
                self.image.h_bins,
                samples[:n_samples].sum(0).T,
                norm=norm,
            )

            # Turn on colorbar to show the range of values.
            plt.colorbar()

            if show_pixels:
                # Turn off ticks and labels.
                plt.tick_params(
                    bottom=False,
                    left=False,
                    labelbottom=False,
                    labelleft=False,
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

    @property
    def config(self):
        config = self.image.config
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
        image = Image.from_config(config)

        instance = cls(image)
        instance.been_split = config["been_split"]
        instance.seed = config["seed"]

        return instance
