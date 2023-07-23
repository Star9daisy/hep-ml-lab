from __future__ import annotations

from keras import Input, Model
from keras.layers import Dense

from .base import KerasMethod


class ToyMLP(KerasMethod):
    """Toy MLP model for testing purposes."""

    def __init__(self, input_shape: tuple | list, name: str = "toy_mlp"):
        # Define model structure
        inputs = Input(shape=input_shape)
        x = Dense(64, activation="relu")(inputs)
        x = Dense(32, activation="relu")(x)
        outputs = Dense(2, activation="softmax")(x)
        model = Model(inputs=inputs, outputs=outputs, name=name)
        metadata = {"input_shape": list(input_shape), "name": name}

        super().__init__(metadata, model)
