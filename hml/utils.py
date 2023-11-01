from __future__ import annotations

import re
from collections import OrderedDict

from .observables import get_observable


class Filter:
    def __init__(self, cuts: list[str]) -> None:
        self.cuts = cuts
        self.stat = OrderedDict({cut: 0 for cut in cuts})

    def read(self, event):
        self.event = event
        return self

    def passed(self):
        def _replace_with_value(match):
            observable_name = match.group(0)  # complete match
            value = get_observable(observable_name).read_event(self.event).value

            if value is not None:
                return str(value)
            else:
                return "np.nan"

        for cut in self.cuts:
            modified_string = re.sub(
                r"\b(?!\d+\b)([\w\d_]+)\.([\w\d_]+)\b", _replace_with_value, cut
            )
            if eval(modified_string) is False:
                self.stat[cut] += 1
                return False

        return True
