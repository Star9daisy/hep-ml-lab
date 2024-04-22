from __future__ import annotations

import keras
from keras import Model
from keras.layers import Dense, Input


@keras.saving.register_keras_serializable()
class SimpleMLP(Model):
    def __init__(self, input_shape, name="simple_mlp", **kwargs):
        super().__init__(name=name, **kwargs)
        self.input_shape = input_shape
        self.dense1 = Dense(units=32, activation="relu")
        self.dense2 = Dense(units=64, activation="relu")
        self.dense3 = Dense(units=32, activation="relu")
        self.dense4 = Dense(units=2, activation="softmax")

        self.call(Input(shape=input_shape))

    def call(self, x):
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        return self.dense4(x)

    def get_config(self):
        base_config = super().get_config()
        config = {"input_shape": self.input_shape}
        return {**base_config, **config}
