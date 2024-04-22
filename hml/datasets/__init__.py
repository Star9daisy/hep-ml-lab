from __future__ import annotations

import json
import zipfile

from .graph_dataset import GraphDataset
from .image_dataset import ImageDataset
from .set_dataset import SetDataset


def load_dataset(filepath, lazy=True):
    zf = zipfile.ZipFile(filepath)
    # Extract and read configs JSON
    with zf.open("configs.json") as json_file:
        configs = json.load(json_file)

    if configs["class_name"] == "SetDataset":
        ds = SetDataset.load(filepath, lazy=lazy)
    else:
        ds = ImageDataset.load(filepath, lazy=lazy)

    return ds
