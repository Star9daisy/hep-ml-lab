from pathlib import Path

import awkward as ak
import numba as nb
import numpy as np
from keras import utils
from keras.src.backend import config

from ..operations.awkward_ops import ak_from_h5, ak_to_h5


@nb.njit()
def add_records(builder, px, py, pz, e, pdg_id, is_from_w, is_in_leading_jet):
    for i in range(len(px)):
        builder.begin_record()
        builder.field("px").append(px[i])
        builder.field("py").append(py[i])
        builder.field("pz").append(pz[i])
        builder.field("e").append(e[i])
        builder.field("pdg_id").append(pdg_id[i])
        builder.field("is_from_w").append(is_from_w[i])
        builder.field("is_in_leading_jet").append(is_in_leading_jet[i])
        builder.end_record()


def extract_data(path):
    with open(path) as f:
        lines = f.readlines()

    events_builder = ak.ArrayBuilder()
    progress_bar = utils.Progbar(len(lines))

    for line in lines:
        values = line.split()
        px = np.array(values[::7], dtype=float)
        py = np.array(values[1::7], dtype=float)
        pz = np.array(values[2::7], dtype=float)
        e = np.array(values[3::7], dtype=float)
        pdg_id = np.array(values[4::7], dtype=int)
        is_from_w = np.array(values[5::7], dtype=int)
        is_in_leading_jet = np.array(values[6::7], dtype=int)

        events_builder.begin_list()
        add_records(events_builder, px, py, pz, e, pdg_id, is_from_w, is_in_leading_jet)
        events_builder.end_list()

        progress_bar.add(1)

    events = events_builder.snapshot()

    return events


def load_dataset(path="w_tagging"):
    """Load the w-tagging dataset from Zenodo.

    This dataset is from [Supervised jet clustering reference data](https://zenodo.org/record/3981290).

    Parameters
    ----------
    path : str, optional
        The path to the dataset directory (relative to `~/.keras/datasets`), by default "w_tagging".

    Returns
    -------
    events : ak.Array
        The events stored in an awkward record array.
    labels : ak.Array
        The labels stored in an awkward record array.
    """
    path = Path(config.keras_home()) / "datasets" / path
    path.mkdir(exist_ok=True, parents=True)

    qstar_path = utils.get_file(
        fname=path.name + "/qstar.txt",
        origin="https://zenodo.org/records/3981290/files/qstar.txt",
        file_hash="41829c855e1042fb335c790ef6ab72a7",
    )

    wboson_path = utils.get_file(
        fname=path.name + "/wboson.txt",
        origin="https://zenodo.org/records/3981290/files/wboson.txt",
        file_hash="c7dd129af8cc4c22e87972c57268fcb3",
    )

    if (path / "qstar.h5").exists():
        qstar_events = ak_from_h5(path / "qstar.h5")
    else:
        qstar_events = extract_data(qstar_path)
        ak_to_h5(qstar_events, path / "qstar.h5")

    if (path / "wboson.h5").exists():
        wboson_events = ak_from_h5(path / "wboson.h5")
    else:
        wboson_events = extract_data(wboson_path)
        ak_to_h5(wboson_events, path / "wboson.h5")

    events = ak.concatenate([qstar_events, wboson_events])
    labels = ak.zip(
        {"is_w": np.array([0] * len(qstar_events) + [1] * len(wboson_events))}
    )

    return events, labels
