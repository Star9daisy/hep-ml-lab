import fastjet as fj
import matplotlib.pyplot as plt
import numpy as np

from hml.utils import get_jet_algorithm, get_observable


class Image:
    def __init__(self, height, width, channel):
        self.height = get_observable(height)
        self.width = get_observable(width)
        self.channel = get_observable(channel) if channel is not None else None

        self.is_translated = None
        self.is_pixelized = None

    def read(self, event):
        self.event = event
        self.height.read(event)
        self.width.read(event)
        self.channel.read(event) if self.channel is not None else None

    def with_subjets(self, constituents, algorithm, r, min_pt):
        px = get_observable(f"{constituents}.Px").read(self.event).value[0]
        py = get_observable(f"{constituents}.Py").read(self.event).value[0]
        pz = get_observable(f"{constituents}.Pz").read(self.event).value[0]
        e = get_observable(f"{constituents}.E").read(self.event).value[0]

        particles = [fj.PseudoJet(px[i], py[i], pz[i], e[i]) for i in range(len(px))]
        subjet_def = fj.JetDefinition(get_jet_algorithm(algorithm), r)
        self.cluster = fj.ClusterSequence(particles, subjet_def)
        self.subjets = self.cluster.inclusive_jets(min_pt)

    def translate(self, origin="SubJet0"):
        origin_height = get_observable(f"{origin}.{self.height.__class__.__name__}")
        origin_width = get_observable(f"{origin}.{self.width.__class__.__name__}")

        obj, index, _ = origin_height.objs[0]["main"]

        if obj != "SubJet":
            raise ValueError(f"{obj} is not supported yet!")

        origin_height._value = [
            getattr(self.subjets[index], origin_height.__class__.__name__.lower())()
        ]
        origin_width._value = [
            getattr(self.subjets[index], origin_width.__class__.__name__.lower())()
        ]

        self.origin_height = origin_height
        self.origin_width = origin_width

        self.height._value = (
            self.height.to_numpy(keepdims=True) - origin_height.to_numpy()
        ).tolist()
        self.width._value = (
            self.width.to_numpy(keepdims=True) - origin_width.to_numpy()
        ).tolist()

        self.is_translated = True

    def rotate(self, axis="SubJet1", orientation=-90):
        axis_height = get_observable(f"{axis}.{self.height.__class__.__name__}")
        axis_width = get_observable(f"{axis}.{self.width.__class__.__name__}")

        obj, index, _ = axis_height.objs[0]["main"]

        if obj != "SubJet":
            raise ValueError(f"{obj} is not supported yet!")

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
            rotated_points[0].reshape(self.width.to_numpy(keepdims=True).shape).tolist()
        )
        self.height._value = (
            rotated_points[1]
            .reshape(self.height.to_numpy(keepdims=True).shape)
            .tolist()
        )

    def pixelize(self, size, range):
        self.h_bins = np.linspace(*range[0], size[0] + 1)
        self.w_bins = np.linspace(*range[1], size[1] + 1)

        pixelized_values = self.continuous_to_center(
            self.height.to_numpy(), self.h_bins
        )
        pixelized_values = pixelized_values.reshape(
            self.height.to_numpy(keepdims=True).shape
        )
        self.height._value = pixelized_values.tolist()

        pixelized_values = self.continuous_to_center(self.width.to_numpy(), self.w_bins)
        pixelized_values = pixelized_values.reshape(
            self.width.to_numpy(keepdims=True).shape
        )
        self.width._value = pixelized_values.tolist()

        self.is_pixelized = True

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
        if self.is_pixelized is not None:
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
    ):
        plt.figure(dpi=64)

        if not self.is_pixelized:
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
            plt.pcolormesh(self.w_bins, self.h_bins, self.values.T)

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
