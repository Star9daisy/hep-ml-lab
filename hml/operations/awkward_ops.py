from __future__ import annotations

from pathlib import Path

import awkward as ak
import h5py
import numpy as np


def ak_to_h5(array: ak.Array, path: str | Path):
    """Save an Awkward Array to an HDF5 file.

    Parameters
    ----------
    array : ak.Array
        The array to save.
    path : str or Path
        The path to the HDF5 file.

    Examples
    --------
    >>> import awkward as ak
    >>> from hml.operations import ak_to_h5
    >>> array = ak.Array([[1, 2, 3], [], [4, 5], [], [], [6, 7, 8, 9]])
    >>> ak_to_h5(array, "/tmp/array.h5")
    """
    with h5py.File(path, "w") as file:
        group = file.create_group("awkward")

        form, length, _ = ak.to_buffers(ak.to_packed(array), container=group)
        group.attrs["form"] = form.to_json()
        group.attrs["length"] = length


def ak_from_h5(path: str | Path):
    """Load an Awkward Array from an HDF5 file.

    Parameters
    ----------
    path : str or Path
        The path to the HDF5 file.

    Examples
    --------
    >>> from hml.operations import ak_to_h5, ak_from_h5
    >>> array = ak.Array([[1, 2, 3], [], [4, 5], [], [], [6, 7, 8, 9]])
    >>> ak_to_h5(array, "/tmp/array.h5")
    >>> array = ak_from_h5("/tmp/array.h5")
    """
    with h5py.File(path, "r") as file:
        group = file.require_group("awkward")

        array = ak.from_buffers(
            ak.forms.from_json(group.attrs["form"]),
            group.attrs["length"],
            {k: np.asarray(v) for k, v in group.items()},
        )

    return array
