from __future__ import annotations

import keras
from keras import initializers, ops


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
