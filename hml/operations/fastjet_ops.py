from __future__ import annotations

import fastjet as fj


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
