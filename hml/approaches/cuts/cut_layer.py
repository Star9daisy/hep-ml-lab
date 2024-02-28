import re

import awkward as ak
import keras
import pandas as pd
from keras import initializers
from keras import ops

from hml.observables import get_observable


@keras.saving.register_keras_serializable()
class CutLayer(keras.Layer):
    def __init__(
        self,
        cut: str | None = None,
        count=0,
        cut_left: float = 0.0,
        cut_right: float = 0.0,
        case: int = 0,
        feature_id: int = 0,
        **kwargs,
    ):
        if cut is not None:
            super().__init__(name=cut, **kwargs)
        else:
            super().__init__(**kwargs)
            self.name = self.name.replace("cut_layer", "observable")

        self._cut = cut
        self._count = count
        self._cut_left = self.add_weight(
            shape=(),
            initializer=initializers.Constant(cut_left),
            trainable=False,
        )

        self._cut_right = self.add_weight(
            shape=(),
            initializer=initializers.Constant(cut_right),
            trainable=False,
        )

        self._case = self.add_weight(
            shape=(),
            initializer=initializers.Constant(case),
            trainable=False,
        )

        self.feature_id = feature_id

    @property
    def cut(self):
        if self._cut is not None:
            return self._cut
        else:
            if self.case == 0:
                return f"{self.name} <= {self.cut_left:.5f}"
            elif self.case == 1:
                return f"{self.name} >= {self.cut_left:.5f}"
            elif self.case == 2:
                return f"{self.cut_left:.5f} <= {self.name} <= {self.cut_right:.5f}"
            else:
                return f"{self.name} <= {self.cut_left:.5f} or {self.name} >= {self.cut_right:.5f}"

    @property
    def count(self):
        return int(ops.convert_to_numpy(self._count))

    @property
    def cut_left(self):
        return float(ops.convert_to_numpy(self._cut_left))

    @property
    def cut_right(self):
        return float(ops.convert_to_numpy(self._cut_right))

    @property
    def case(self):
        return int(ops.convert_to_numpy(self._case))

    def call(self, x):
        y_pred = ops.cond(
            ops.equal(self._case, 0),
            lambda: ops.where(x <= self._cut_left, 1.0, 0.0),
            lambda: ops.cond(
                ops.equal(self._case, 1),
                lambda: ops.where(x >= self._cut_left, 1.0, 0.0),
                lambda: ops.cond(
                    ops.equal(self._case, 2),
                    lambda: ops.where(
                        ops.logical_and(x >= self._cut_left, x <= self._cut_right),
                        1.0,
                        0.0,
                    ),
                    lambda: ops.where(
                        ops.logical_or(x <= self._cut_left, x >= self._cut_right),
                        1.0,
                        0.0,
                    ),
                ),
            ),
        )

        return y_pred

    def apply_cut(self, x, cut_mark=-1.0):
        x = ops.cast(x, "float32")
        if ops.ndim(x) == 2:
            x = ops.take(x, self.feature_id, axis=-1)

        y_pred = ops.cond(
            ops.equal(self._case, 0),
            lambda: ops.where(x <= self._cut_left, 1.0, cut_mark),
            lambda: ops.cond(
                ops.equal(self._case, 1),
                lambda: ops.where(x >= self._cut_left, 1.0, cut_mark),
                lambda: ops.cond(
                    ops.equal(self._case, 2),
                    lambda: ops.where(
                        ops.logical_and(x >= self._cut_left, x <= self._cut_right),
                        1.0,
                        cut_mark,
                    ),
                    lambda: ops.where(
                        ops.logical_or(x <= self._cut_left, x >= self._cut_right),
                        1.0,
                        cut_mark,
                    ),
                ),
            ),
        )
        return y_pred

    def compute_output_shape(self, input_shape):
        return input_shape

    def is_passed(self, event):
        # TODO: if cut does not have logical operators, it will be treated as a
        #       learnable cut. Calling this method will raise an error.
        if not isinstance(self._cut, str):
            raise TypeError(f"is_passed should be used when specify a cut manually")

        cut_exp = self._cut.strip()

        veto = False
        if "veto" in cut_exp:
            cut_exp = cut_exp.replace("veto", "")
            veto = True

        is_any = False
        if "[any]" in cut_exp:
            cut_exp = cut_exp.replace("[any]", "")
            is_any = True
        else:
            cut_exp = cut_exp.replace("[all]", "")

        cuts_per_obs = cut_exp.strip().split("and")
        cuts_per_obs = [i.strip().split("or") for i in cuts_per_obs]
        cuts_per_obs = [i for j in cuts_per_obs for i in j]
        cuts_per_obs = [i.strip().split("xor") for i in cuts_per_obs]
        cuts_per_obs = [i for j in cuts_per_obs for i in j]

        obs_pattern = r"\b(?!\d+\b)(?!\d*\.\d+\b)\S+\b"
        obs_names = [re.findall(obs_pattern, i)[0] for i in cuts_per_obs]
        obs_list = [get_observable(i).read_ttree(event) for i in obs_names]
        for obs in obs_list:
            if "var" in obs.shape:
                obs.value = ak.flatten(obs.value)

        for i in obs_names:
            cut_exp = cut_exp.replace(i, f"`{i}`")

        df = pd.DataFrame(
            {
                obs.name: [obs.value] if not isinstance(obs.value, list) else obs.value
                for obs in obs_list
            }
        )

        result = False
        if is_any:
            if len(df.query(cut_exp)) > 0:
                result = True
            else:
                self._count += 1
                result = False
        else:
            if len(df) == len(df.query(cut_exp)):
                result = True
            else:
                self._count += 1
                result = False

        if veto:
            self._count += 1
            result = not result

        return result

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "cut": self._cut,
                "count": self._count,
                "feature_id": self.feature_id,
            }
        )
        return config
