from __future__ import annotations

import awkward as ak
import numba as nb
import vector

vector.register_awkward()


@nb.njit(cache=True)
def find_1d_in_2d(a, b):  # pragma: no cover
    index_array = []

    for record_a, record_b in zip(a, b):
        indices_per_a = []

        for i in range(len(record_b)):
            indices_per_b = []
            for j in range(len(record_b[i])):
                for k in range(len(record_a)):
                    if record_b[i][j] == record_a[k]:
                        indices_per_b.append(k)

            indices_per_a.append(indices_per_b)
        index_array.append(indices_per_a)

    return index_array


def branches_to_momentum4d(events, branch, with_id=False):
    eta = events[f"{branch}.Eta"].array()
    phi = events[f"{branch}.Phi"].array()

    if f"{branch}.PT" in events:
        pt = events[f"{branch}.PT"].array()
        mass = events[f"{branch}.Mass"].array()
    else:
        pt = events[f"{branch}.ET"].array()
        mass = ak.zeros_like(pt)

    if with_id:
        id_ = events[f"{branch}.fUniqueID"].array()
        momenta = ak.zip(
            {
                "id": id_,
                "pt": pt,
                "eta": eta,
                "phi": phi,
                "mass": mass,
            },
            with_name="Momentum4D",
        )
        momenta["pt"] = ak.values_astype(momenta["pt"], "float32")
        momenta["eta"] = ak.values_astype(momenta["eta"], "float32")
        momenta["phi"] = ak.values_astype(momenta["phi"], "float32")
        momenta["mass"] = ak.values_astype(momenta["mass"], "float32")

    else:
        momenta = ak.zip(
            {
                "pt": pt,
                "eta": eta,
                "phi": phi,
                "mass": mass,
            },
            with_name="Momentum4D",
        )
        momenta = ak.values_astype(momenta, "float32")

    return momenta


@nb.njit(cache=True)
def take_2d_from_1d(array, indices):  # pragma: no cover
    pt = []
    eta = []
    phi = []
    mass = []

    for record, indices_at_1 in zip(array, indices):
        pt.append(
            [[record[i].pt for i in indices_at_2] for indices_at_2 in indices_at_1]
        )
        phi.append(
            [[record[i].phi for i in indices_at_2] for indices_at_2 in indices_at_1]
        )
        eta.append(
            [[record[i].eta for i in indices_at_2] for indices_at_2 in indices_at_1]
        )
        mass.append(
            [[record[i].mass for i in indices_at_2] for indices_at_2 in indices_at_1]
        )

    return pt, eta, phi, mass


def get_constituents(events, branch):
    refs = events[branch].array()["refs"]
    tracks = branches_to_momentum4d(events, "EFlowTrack", with_id=True)
    photons = branches_to_momentum4d(events, "EFlowPhoton", with_id=True)
    neutrals = branches_to_momentum4d(events, "EFlowNeutralHadron", with_id=True)

    matched_tracks = ak.zip(
        dict(
            zip(
                ["pt", "eta", "phi", "mass"],
                take_2d_from_1d(tracks, ak.from_iter(find_1d_in_2d(tracks.id, refs))),
            )
        ),
        with_name="Momentum4D",
    )

    matched_photons = ak.zip(
        dict(
            zip(
                ["pt", "eta", "phi", "mass"],
                take_2d_from_1d(photons, ak.from_iter(find_1d_in_2d(photons.id, refs))),
            )
        ),
        with_name="Momentum4D",
    )

    matched_neutrals = ak.zip(
        dict(
            zip(
                ["pt", "eta", "phi", "mass"],
                take_2d_from_1d(
                    neutrals, ak.from_iter(find_1d_in_2d(neutrals.id, refs))
                ),
            )
        ),
        with_name="Momentum4D",
    )

    constituents = ak.concatenate(
        [matched_tracks, matched_photons, matched_neutrals], axis=-1
    )
    constituents = ak.values_astype(constituents, "float32")

    return constituents
