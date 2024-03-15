import fastjet as fj
from keras import ops

from hml.observables import Observable


def ops_histogram_fixed_width(values, value_range, nbins, dtype="int32"):
    value_min, value_max = value_range
    bin_edges = ops.linspace(value_min, value_max, nbins + 1)
    lower = bin_edges[:-1]  # type: ignore
    upper = bin_edges[1:]  # type: ignore

    return ops.fori_loop(
        0,
        nbins,
        lambda i, s: ops.scatter_update(
            s,
            [[i]],
            [
                ops.count_nonzero(
                    ops.where(
                        ops.logical_and(lower[i] <= values, values <= upper[i]),
                        1.0,
                        0.0,
                    )
                )
            ],
        ),
        ops.zeros((nbins,), dtype=dtype),
    )


def ops_unique(tensor):
    sorted_tensor, sorted_indices = ops.sort(tensor), ops.argsort(tensor)
    selection = ops.not_equal(sorted_tensor[1:], sorted_tensor[:-1])  # type: ignore
    selection = ops.add(ops.squeeze(ops.where(selection), 0), 1)
    unique_indices = ops.append([0], selection)

    try:
        unique_elements = ops.take(sorted_tensor, unique_indices)
        unique_indices = ops.take(sorted_indices, unique_indices)
        return unique_elements
    except:
        return ops.array([0])


def get_jet_algorithm(name: str):
    JET_ALGORITHMS = {
        "kt": fj.kt_algorithm,
        "cambridge": fj.cambridge_algorithm,
        "antikt": fj.antikt_algorithm,
        "genkt": fj.genkt_algorithm,
        "cambridge_for_passive": fj.cambridge_for_passive_algorithm,
        "genkt_for_passive": fj.genkt_for_passive_algorithm,
        "ee_kt": fj.ee_kt_algorithm,
        "ee_genkt": fj.ee_genkt_algorithm,
        "plugin": fj.plugin_algorithm,
        "undefined": fj.undefined_jet_algorithm,
    }

    return JET_ALGORITHMS.get(name, fj.undefined_jet_algorithm)
