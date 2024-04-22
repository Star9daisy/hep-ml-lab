from __future__ import annotations

from keras import ops


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

    except Exception:
        return ops.array([0])
