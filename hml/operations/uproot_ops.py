from __future__ import annotations

import awkward as ak
import numba as nb
import vector

vector.register_awkward()


@nb.njit(cache=True)
def find_eflow_in_refs(eflow, refs):  # pragma: no cover
    """Find the constituent reference indices in an eflow branch.

    This operation is used to retrieve the jet constituents. Jet constituents are
    a reference to the "EFlowTrack", "EFlowPhoton", and "EFlowNeutralHadron" branches
    in the Delphes output.

    The reference is a 2d record array with the shape (n, var, var), which means
    n events with variable-length jets and variable-length constituents per jet.
    The corresponding branch, however, is a 1d record array. To related the two,
    we need to find the "fUniqueID" of the jet constituents in the reference array.

    Parameters
    ----------
    eflow: awkward array, shape (n, var)
        EFlowTrack, EFlowPhoton, or EFlowNeutralHadron array.
    refs: awkward array, shape (n, var, var)
        Reference array of all jet constituents.

    Return
    ------
    indices: list
        List of indices of constituents in the eflow array.
    """
    indices = []

    for record_a, record_b in zip(eflow, refs):
        indices_per_a = []

        for i in range(len(record_b)):
            indices_per_b = []

            for j in range(len(record_b[i])):
                for k in range(len(record_a)):
                    if record_b[i][j] == record_a[k]:
                        indices_per_b.append(k)
            indices_per_a.append(indices_per_b)

        indices.append(indices_per_a)

    return indices


@nb.njit(cache=True)
def take_momentum4d(array, indices):  # pragma: no cover
    """Take the 4-momentum of the constituents in the eflow array.

    Parameters
    ----------
    array: awkward array, shape (n, var)
        EFlowTrack, EFlowPhoton, or EFlowNeutralHadron array.
    indices: list
        List of indices of constituents in the eflow array.

    Return
    ------
    momentum4d: tuple
        Tuple of 4-momentum components (pt, eta, phi, mass).
    """
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


def branch_to_momentum4d(events, branch, with_id=False):
    """Convert a Delphes branch to a 4-momentum array.

    Some branches in the Delphes output do not have full 4-momentum information,
    e.g., "Jet" has PT, Eta, Phi, Mass but no Px, Py, Pz, E. This function converts
    the branch to the registered "Momentum4D" array supported by the vector library.

    Parameters
    ----------
    events:
        Events opened by uproot.
    branch: str
        Branch name to be converted, e.g., "Jet"
    with_id: bool
        Whether to include the "fUniqueID" in the 4-momentum array, which is used
        to find the constituents in the eflow branches.

    Return
    ------
    momenta: Momentum4D
        4-momentum array with the shape (n, var).
    """
    eta = events[f"{branch}.Eta"].array()
    phi = events[f"{branch}.Phi"].array()

    if f"{branch}.PT" in events:
        pt = events[f"{branch}.PT"].array()
    elif f"{branch}.ET" in events:
        pt = events[f"{branch}.ET"].array()
    elif f"{branch}.MET" in events:
        pt = events[f"{branch}.MET"].array()
    else:
        raise ValueError(f"Cannot find the PT branch for {branch}")

    if f"{branch}.Mass" in events:
        mass = events[f"{branch}.Mass"].array()
    else:
        mass = ak.zeros_like(eta)

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

    if with_id:
        momenta["id"] = events[f"{branch}.fUniqueID"].array()

    return momenta


def constituents_to_momentum4d(events, branch):
    """Convert the constituents in a Delphes branch to a 4-momentum array.

    Parameters
    ----------
    events:
        Events opened by uproot.
    branch: str
        Branch name to be converted, e.g., "Jet.Constituents"

    Return
    ------
    constituents: Momentum4D
        4-momentum array with the shape (n, var, var).
    """
    refs = events[branch].array()["refs"]
    tracks = branch_to_momentum4d(events, "EFlowTrack", with_id=True)
    photons = branch_to_momentum4d(events, "EFlowPhoton", with_id=True)
    neutrals = branch_to_momentum4d(events, "EFlowNeutralHadron", with_id=True)

    matches = []
    for i in [tracks, photons, neutrals]:
        indices = ak.from_iter(find_eflow_in_refs(i.id, refs))
        pt, eta, phi, mass = take_momentum4d(i, indices)
        matches.append(
            ak.zip(
                {
                    "pt": pt,
                    "eta": eta,
                    "phi": phi,
                    "mass": mass,
                },
                with_name="Momentum4D",
            )
        )

    constituents = ak.concatenate(matches, -1)
    constituents = ak.values_astype(constituents, "float32")

    return constituents
