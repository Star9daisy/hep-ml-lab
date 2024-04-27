from __future__ import annotations

import keras
from keras import Model
from keras.layers import (
    Conv2D,
    Dense,
    Dropout,
    GlobalAveragePooling2D,
    Input,
    MaxPooling2D,
)


@keras.saving.register_keras_serializable()
class SimpleCNN(Model):
    def __init__(self, input_shape, name="simple_cnn", **kwargs):
        super().__init__(name=name, **kwargs)
        self.input_shape = input_shape
        self.conv1 = Conv2D(8, 3, padding="same", activation="relu")
        self.conv2 = Conv2D(16, 3, padding="same", activation="relu")
        self.conv3 = Conv2D(32, 3, padding="same", activation="relu")
        self.max_pool = MaxPooling2D()
        self.global_avg_pool = GlobalAveragePooling2D()
        self.dropout = Dropout(0.5)
        self.dense1 = Dense(2, activation="softmax")

        self.call(Input(shape=input_shape))

    def call(self, x):
        x = self.conv1(x)
        x = self.max_pool(x)
        x = self.conv2(x)
        x = self.max_pool(x)
        x = self.conv3(x)
        x = self.max_pool(x)
        x = self.global_avg_pool(x)
        return self.dense1(x)

    def get_config(self):
        base_config = super().get_config()
        config = {"input_shape": self.input_shape}
        return {**base_config, **config}
