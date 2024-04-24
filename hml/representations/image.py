from __future__ import annotations

from importlib import import_module

import awkward as ak
import matplotlib.pyplot as plt
import numba as nb
import numpy as np
import vector
from fastjet import ClusterSequence, JetDefinition

from hml.observables import parse_observable
from hml.operations import get_jet_algorithm

vector.register_awkward()


class Image:
    def __init__(self, height, width, channel=None):
        self.height = parse_observable(height) if isinstance(height, str) else height
        self.width = parse_observable(width) if isinstance(width, str) else width

        if channel is not None:
            self.channel = (
                parse_observable(channel) if isinstance(channel, str) else channel
            )
        else:
            self.channel = None

        self.been_pixelated = None
        self.been_read = False
        self.registered_methods = []
        self.recorded_operations = []
        self.status = True

    def read(self, events):
        self.been_pixelated = None
        self.been_read = False
        self.status = True

        self.event = events
        self.height.read(events)
        self.height._value = ak.flatten(self.height._value, axis=-1)
        self.width.read(events)
        self.width._value = ak.flatten(self.width._value, axis=-1)

        if self.channel is not None:
            self.channel.read(events)
            self.channel._value = ak.flatten(self.channel._value, axis=-1)
        self.been_read = True

        for method, kwargs in self.registered_methods:
            getattr(self, method)(**kwargs)

        return self

    def with_subjets(self, constituents, algorithm, r, min_pt):
        if self.been_read:
            px = parse_observable(f"{constituents}.Px").read(self.event).value
            py = parse_observable(f"{constituents}.Py").read(self.event).value
            pz = parse_observable(f"{constituents}.Pz").read(self.event).value
            e = parse_observable(f"{constituents}.E").read(self.event).value

            px = ak.flatten(px, -1)
            py = ak.flatten(py, -1)
            pz = ak.flatten(pz, -1)
            e = ak.flatten(e, -1)

            particles = ak.zip(
                {"px": px, "py": py, "pz": pz, "e": e}, with_name="Momentum4D"
            )
            subjet_def = JetDefinition(get_jet_algorithm(algorithm), r)
            self.cluster = ClusterSequence(particles, subjet_def)
            self.subjets = self.cluster.inclusive_jets(min_pt)

            self.recorded_operations.append(
                (
                    "with_subjets",
                    {
                        "constituents": constituents,
                        "algorithm": algorithm,
                        "r": r,
                        "min_pt": min_pt,
                    },
                )
            )
        else:
            self.registered_methods.append(
                (
                    "with_subjets",
                    {
                        "constituents": constituents,
                        "algorithm": algorithm,
                        "r": r,
                        "min_pt": min_pt,
                    },
                )
            )

        return self

    def translate(self, origin="SubJet0"):
        if self.been_read:
            origin_height = parse_observable(
                f"{origin}.{self.height.__class__.__name__}"
            )
            origin_width = parse_observable(f"{origin}.{self.width.__class__.__name__}")

            obj = origin_height.physics_object.branch
            index = origin_height.physics_object.index

            if obj != "SubJet":
                raise ValueError(f"{obj} is not supported yet!")

            if len(self.subjets) < index + 1:
                self.status = False
                return self

            origin_height._value = ak.to_regular(
                ak.pad_none(
                    getattr(self.subjets, origin_height.__class__.__name__.lower())[
                        :, : index + 1
                    ],
                    1,
                )
            )

            origin_width._value = ak.to_regular(
                ak.pad_none(
                    getattr(self.subjets, origin_width.__class__.__name__.lower())[
                        :, : index + 1
                    ],
                    1,
                )
            )

            self.origin_height = origin_height
            self.origin_width = origin_width

            translated_height = self.height.value - origin_height.value
            if self.height.__class__.__name__ == "Phi":
                translated_height = np.mod(translated_height + np.pi, 2 * np.pi) - np.pi

            translated_width = self.width.value - origin_width.value
            if self.width.__class__.__name__ == "Phi":
                translated_width = np.mod(translated_width + np.pi, 2 * np.pi) - np.pi

            self.height._value = translated_height
            self.width._value = translated_width

            self.recorded_operations.append(("translate", {"origin": origin}))
        else:
            self.registered_methods.append(("translate", {"origin": origin}))

        return self

    def rotate(self, axis="SubJet1", orientation=-90):
        if self.been_read:
            axis_height = parse_observable(f"{axis}.{self.height.__class__.__name__}")
            axis_width = parse_observable(f"{axis}.{self.width.__class__.__name__}")

            obj = axis_height.physics_object.branch
            index = axis_height.physics_object.index

            if obj != "SubJet":
                raise ValueError(f"{obj} is not supported yet!")

            if len(self.subjets) < index + 1:
                self.status = False
                return self

            axis_height._value = ak.to_regular(
                ak.pad_none(
                    getattr(self.subjets, axis_height.__class__.__name__.lower())[
                        :, index : index + 1
                    ],
                    1,
                )
            )
            axis_width._value = ak.to_regular(
                ak.pad_none(
                    getattr(self.subjets, axis_width.__class__.__name__.lower())[
                        :, index : index + 1
                    ],
                    1,
                )
            )

            delta_h = axis_height.value - self.origin_height.value
            delta_w = axis_width.value - self.origin_width.value
            angle = orientation - np.arctan2(delta_h, delta_w) * 180 / np.pi
            angle = np.deg2rad(angle)

            # rotation_matrix = np.array(
            #     [
            #         [np.cos(angle), -np.sin(angle)],
            #         [np.sin(angle), np.cos(angle)],
            #     ]
            # )  # (2, 2)
            # points = np.vstack(
            #     [self.width.to_numpy(), self.height.to_numpy()]
            # )  # (2, n)
            # rotated_points = np.dot(rotation_matrix, points)  # (2, n)
            angle = ak.values_astype(ak.fill_none(angle, np.nan), "float32")
            x = self.width.value
            y = self.height.value
            x_prime = np.cos(angle) * x - np.sin(angle) * y
            y_prime = np.sin(angle) * x + np.cos(angle) * y

            self.width._value = x_prime
            self.height._value = y_prime

            self.recorded_operations.append(
                ("rotate", {"axis": axis, "orientation": orientation})
            )

        else:
            self.registered_methods.append(
                ("rotate", {"axis": axis, "orientation": orientation})
            )

        return self

    def pixelate(self, size, range):
        self.been_pixelated = True
        self.h_bins = np.linspace(*range[0], size[0] + 1)
        self.w_bins = np.linspace(*range[1], size[1] + 1)

        if self.been_read:
            if self.status is False:
                return self

            self.height._value = self.continuous_to_center(
                self.height.value, self.h_bins
            )
            # pixelated_values = self.continuous_to_center(
            #     self.height.to_numpy(), self.h_bins
            # )
            # pixelated_values = pixelated_values.reshape(
            #     self.height.to_numpy(squeeze=False).shape
            # )
            # self.height._value = pixelated_values.tolist()

            self.width._value = self.continuous_to_center(self.width.value, self.w_bins)

            # pixelated_values = self.continuous_to_center(
            #     self.width.to_numpy(), self.w_bins
            # )
            # pixelated_values = pixelated_values.reshape(
            #     self.width.to_numpy(squeeze=False).shape
            # )
            # self.width._value = pixelated_values.tolist()

            self.recorded_operations.append(
                ("pixelate", {"size": size, "range": range})
            )

        else:
            self.registered_methods.append(("pixelate", {"size": size, "range": range}))

        return self

    def continuous_to_center(self, values, bins):
        def _transform_func(layout, **kwargs):
            if layout.is_numpy:
                out_values = np.empty_like(layout.data)
                bin_centers = (bins[:-1] + bins[1:]) / 2
                bin_indices = np.digitize(layout.data, bins)

                for i, index in enumerate(bin_indices):
                    if index == 0 or index == len(bins):
                        out_values[i] = np.nan
                    else:
                        out_values[i] = bin_centers[index - 1]

                return ak.contents.NumpyArray(out_values)

        return ak.transform(_transform_func, values)

    @property
    def values(self):
        widths = ak.fill_none(self.width.value, np.nan)
        heights = ak.fill_none(self.height.value, np.nan)
        total = len(widths)

        if self.been_pixelated is not None and self.been_read:
            if self.channel is not None:
                weights = ak.fill_none(self.channel.value, np.nan)
                hist = calculate_histograms(
                    widths, heights, self.w_bins, self.h_bins, total, weights
                )
            else:
                hist = calculate_histograms(
                    widths, heights, self.w_bins, self.h_bins, total
                )
            return hist

        return self.height.value, self.width.value

    def show(
        self,
        as_point=False,
        limits=None,
        show_pixels=False,
        grid=True,
        norm=None,
    ):
        plt.figure()

        if not self.been_pixelated:
            plt.scatter(
                x=ak.flatten(self.width.value, None),
                y=ak.flatten(self.height.value, None),
                c="k",
                s=10,
                marker="o",
            )

            # Restrict the range of axes.
            if limits is not None:
                plt.xlim(limits[0])
                plt.ylim(limits[1])

        elif as_point:
            plt.scatter(
                x=ak.flatten(self.width.value, None),
                y=ak.flatten(self.height.value, None),
                c="k",
                s=10,
                marker="s",
            )
            plt.xlim(self.w_bins[0], self.w_bins[-1])
            plt.ylim(self.h_bins[0], self.h_bins[-1])

            plt.gca().set_aspect("equal")

        else:
            # Use pcolormesh instead of imshow so that the actual values of bins
            # are shown.
            plt.pcolormesh(self.w_bins, self.h_bins, self.values.sum(0).T, norm=norm)

            # Turn on colorbar to show the range of values.
            plt.colorbar()

            if show_pixels:
                # Turn off ticks and labels.
                plt.tick_params(
                    bottom=False, left=False, labelbottom=False, labelleft=False
                )
                plt.xticks(self.w_bins)
                plt.yticks(self.h_bins)

            # Set aspect ratio to be equal so that every pixel is square.
            # Ignore the actual values of bins since here is just a schematic.
            plt.gca().set_aspect("equal")

        # Turn on grid to show pixel boundaries.
        if grid:
            plt.grid(alpha=0.5)

        plt.show()

    @property
    def config(self):
        return {
            "height_config": {
                "class_name": self.height.__class__.__name__,
                "config": self.height.config,
            },
            "width_config": {
                "class_name": self.width.__class__.__name__,
                "config": self.width.config,
            },
            "channel_config": (
                {
                    "class_name": self.channel.__class__.__name__,
                    "config": self.channel.config if self.channel is not None else None,
                }
                if self.channel is not None
                else None
            ),
            "registered_methods": (
                self.registered_methods
                if not self.been_read
                else self.recorded_operations
            ),
            "been_pixelated": self.been_pixelated,
            "w_bins": (self.w_bins.tolist() if self.been_pixelated else None),
            "h_bins": (self.h_bins.tolist() if self.been_pixelated else None),
        }

    @classmethod
    def from_config(cls, config):
        module = import_module("hml.observables")

        height_class_name = config["height_config"]["class_name"]
        height_class = getattr(module, height_class_name)
        height = height_class.from_config(config["height_config"]["config"])

        width_class_name = config["width_config"]["class_name"]
        width_class = getattr(module, width_class_name)
        width = width_class.from_config(config["width_config"]["config"])

        if config["channel_config"] is not None:
            channel_class_name = config["channel_config"]["class_name"]
            channel_class = getattr(module, channel_class_name)
            channel = channel_class.from_config(config["channel_config"]["config"])
        else:
            channel = None

        instance = cls(height, width, channel)

        instance.registered_methods = config["registered_methods"]
        instance.been_pixelated = config["been_pixelated"]
        instance.w_bins = (
            np.array(config["w_bins"]) if config["w_bins"] is not None else None
        )
        instance.h_bins = (
            np.array(config["h_bins"]) if config["h_bins"] is not None else None
        )

        return instance


@nb.njit
def histogram2d_numba_weighted(x, y, bins, xrange, yrange, weights):
    hist = np.zeros((bins[0], bins[1]), dtype=np.float64)

    x_bin_width = (xrange[1] - xrange[0]) / bins[0]
    y_bin_width = (yrange[1] - yrange[0]) / bins[1]

    for i in range(len(x)):
        if xrange[0] <= x[i] < xrange[1] and yrange[0] <= y[i] < yrange[1]:
            x_bin = int((x[i] - xrange[0]) / x_bin_width)
            y_bin = int((y[i] - yrange[0]) / y_bin_width)

            # Ensure the indices are within the range of the histogram
            x_bin = min(x_bin, bins[0] - 1)
            y_bin = min(y_bin, bins[1] - 1)

            hist[x_bin, y_bin] += weights[i]

    return hist


@nb.njit
def histogram2d_numba(x, y, bins, xrange, yrange):
    """
    A simplified version of numpy.histogram2d compatible with Numba.

    Parameters:
    - x, y: Arrays of the same length containing the x and y coordinates of the points.
    - bins: A tuple (x_bins, y_bins) specifying the number of bins in each dimension.
    - xrange: A tuple (x_min, x_max) specifying the minimum and maximum range on the x-axis.
    - yrange: A tuple (y_min, y_max) specifying the minimum and maximum range on the y-axis.

    Returns:
    - A 2D histogram array.
    """
    hist = np.zeros((bins[0], bins[1]), dtype=np.float64)

    x_bin_width = (xrange[1] - xrange[0]) / bins[0]
    y_bin_width = (yrange[1] - yrange[0]) / bins[1]

    for i in range(len(x)):
        if xrange[0] <= x[i] < xrange[1] and yrange[0] <= y[i] < yrange[1]:
            x_bin = int((x[i] - xrange[0]) / x_bin_width)
            y_bin = int((y[i] - yrange[0]) / y_bin_width)

            # Ensure the indices are within the range of the histogram
            x_bin = min(x_bin, bins[0] - 1)
            y_bin = min(y_bin, bins[1] - 1)

            hist[x_bin, y_bin] += 1

    return hist


@nb.njit
def calculate_histograms(widths, heights, w_bins, h_bins, total, weights=None):
    # Assuming widths and heights are flat NumPy arrays of the same length
    # and that missing data has been handled prior to this call.

    hists = np.zeros(
        (total, len(w_bins) - 1, len(h_bins) - 1)
    )  # Pre-allocate based on expected sizes
    if weights is not None:
        for i in range(total):
            hist = histogram2d_numba_weighted(
                widths[i],  # Assuming these are now slices or individual arrays
                heights[i],
                bins=(len(w_bins) - 1, len(h_bins) - 1),
                xrange=(w_bins[0], w_bins[-1]),
                yrange=(h_bins[0], h_bins[-1]),
                weights=weights[i],
            )
            hists[i] = hist
    else:
        for i in range(total):
            hist = histogram2d_numba(
                widths[i],  # Assuming these are now slices or individual arrays
                heights[i],
                bins=(len(w_bins) - 1, len(h_bins) - 1),
                xrange=(w_bins[0], w_bins[-1]),
                yrange=(h_bins[0], h_bins[-1]),
            )
            hists[i] = hist

    return hists
