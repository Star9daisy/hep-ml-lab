from keras import Model
from keras.layers import Dense


class ToyMLP(Model):
    def __init__(self, input_shape: tuple, name: str = "toy_mlp", **kwargs):
        super().__init__(name=name, **kwargs)
        self.dense1 = Dense(64, activation="relu", input_shape=input_shape)
        self.dense2 = Dense(32, activation="relu")
        self.dense3 = Dense(2, activation="softmax")

    def call(self, x):
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        return x
