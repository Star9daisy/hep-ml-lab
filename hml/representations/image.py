from importlib import import_module

import matplotlib.pyplot as plt
import numpy as np
from fastjet import ClusterSequence
from fastjet import JetDefinition
from fastjet import PseudoJet

from hml.observables import get_observable
from hml.utils import get_jet_algorithm


class Image:
    def __init__(self, height, width, channel=None):
        self.height = get_observable(height) if isinstance(height, str) else height
        self.width = get_observable(width) if isinstance(width, str) else width

        if channel is not None:
            self.channel = (
                get_observable(channel) if isinstance(channel, str) else channel
            )
        else:
            self.channel = None

        self.been_pixelated = None
        self.been_read = False
        self.registered_methods = []
        self.recorded_operations = []
        self.status = True

    def read_ttree(self, event):
        self.been_pixelated = None
        self.been_read = False
        self.status = True

        self.event = event
        self.height.read_ttree(event)
        self.width.read_ttree(event)
        self.channel.read_ttree(event) if self.channel is not None else None
        self.been_read = True

        for method, kwargs in self.registered_methods:
            getattr(self, method)(**kwargs)

        return self

    def with_subjets(self, constituents, algorithm, r, min_pt):
        if self.been_read:
            px = get_observable(f"{constituents}.Px").read_ttree(self.event).value[0]
            py = get_observable(f"{constituents}.Py").read_ttree(self.event).value[0]
            pz = get_observable(f"{constituents}.Pz").read_ttree(self.event).value[0]
            e = get_observable(f"{constituents}.E").read_ttree(self.event).value[0]

            particles = [PseudoJet(px[i], py[i], pz[i], e[i]) for i in range(len(px))]
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
            origin_height = get_observable(f"{origin}.{self.height.__class__.__name__}")
            origin_width = get_observable(f"{origin}.{self.width.__class__.__name__}")

            obj = origin_height.physics_object.branch
            index = origin_height.physics_object.index

            if obj != "SubJet":
                raise ValueError(f"{obj} is not supported yet!")

            if len(self.subjets) < index + 1:
                self.status = False
                return self

            origin_height._value = [
                getattr(self.subjets[index], origin_height.__class__.__name__.lower())()
            ]
            origin_width._value = [
                getattr(self.subjets[index], origin_width.__class__.__name__.lower())()
            ]

            self.origin_height = origin_height
            self.origin_width = origin_width

            translated_height = self.height.to_numpy() - origin_height.to_numpy()
            translated_width = self.width.to_numpy() - origin_width.to_numpy()
            self.height._value = translated_height.tolist()
            self.width._value = translated_width.tolist()

            self.recorded_operations.append(("translate", {"origin": origin}))
        else:
            self.registered_methods.append(("translate", {"origin": origin}))

        return self

    def rotate(self, axis="SubJet1", orientation=-90):
        if self.been_read:

            axis_height = get_observable(f"{axis}.{self.height.__class__.__name__}")
            axis_width = get_observable(f"{axis}.{self.width.__class__.__name__}")

            obj = axis_height.physics_object.branch
            index = axis_height.physics_object.index

            if obj != "SubJet":
                raise ValueError(f"{obj} is not supported yet!")

            if len(self.subjets) < index + 1:
                self.status = False
                return self

            axis_height._value = [
                getattr(self.subjets[index], axis_height.__class__.__name__.lower())()
            ]
            axis_width._value = [
                getattr(self.subjets[index], axis_width.__class__.__name__.lower())()
            ]

            delta_h = axis_height.to_numpy() - self.origin_height.to_numpy()
            delta_w = axis_width.to_numpy() - self.origin_width.to_numpy()
            angle = orientation - np.arctan2(delta_h, delta_w) * 180 / np.pi
            angle = np.deg2rad(angle)

            rotation_matrix = np.array(
                [
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)],
                ]
            )
            points = np.vstack([self.width.to_numpy(), self.height.to_numpy()])
            rotated_points = np.dot(rotation_matrix, points)
            self.width._value = (
                rotated_points[0]
                .reshape(self.width.to_numpy(squeeze=False).shape)
                .tolist()
            )
            self.height._value = (
                rotated_points[1]
                .reshape(self.height.to_numpy(squeeze=False).shape)
                .tolist()
            )

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

        if self.been_read:
            if self.status is False:
                return self

            self.h_bins = np.linspace(*range[0], size[0] + 1)
            self.w_bins = np.linspace(*range[1], size[1] + 1)

            pixelated_values = self.continuous_to_center(
                self.height.to_numpy(), self.h_bins
            )
            pixelated_values = pixelated_values.reshape(
                self.height.to_numpy(squeeze=False).shape
            )
            self.height._value = pixelated_values.tolist()

            pixelated_values = self.continuous_to_center(
                self.width.to_numpy(), self.w_bins
            )
            pixelated_values = pixelated_values.reshape(
                self.width.to_numpy(squeeze=False).shape
            )
            self.width._value = pixelated_values.tolist()

            self.recorded_operations.append(
                ("pixelate", {"size": size, "range": range})
            )

        else:
            self.registered_methods.append(("pixelate", {"size": size, "range": range}))

        return self

    def continuous_to_center(self, values, bins):
        out_values = np.empty_like(values)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        bin_indices = np.digitize(values, bins)

        for i, index in enumerate(bin_indices):
            if index == 0 or index == len(bins):
                out_values[i] = np.nan
            else:
                out_values[i] = bin_centers[index - 1]

        return out_values

    @property
    def values(self):
        if self.been_pixelated is not None and self.been_read:
            if self.channel is not None:
                hist, _, _ = np.histogram2d(
                    self.width.to_numpy(),
                    self.height.to_numpy(),
                    bins=(self.w_bins, self.h_bins),
                    weights=self.channel.to_numpy(),
                )
            else:
                hist, _, _ = np.histogram2d(
                    self.width.to_numpy(),
                    self.height.to_numpy(),
                    bins=(self.w_bins, self.h_bins),
                )
            return hist

        return self.height.to_numpy(), self.width.to_numpy()

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
                x=self.width.to_numpy(),
                y=self.height.to_numpy(),
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
                x=self.width.to_numpy(),
                y=self.height.to_numpy(),
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
            plt.pcolormesh(self.w_bins, self.h_bins, self.values.T, norm=norm)

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
            "w_bins": (
                self.w_bins.tolist() if self.been_pixelated and self.been_read else None
            ),
            "h_bins": (
                self.h_bins.tolist() if self.been_pixelated and self.been_read else None
            ),
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
