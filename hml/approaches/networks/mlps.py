import keras


@keras.saving.register_keras_serializable()
class ToyMultilayerPerceptron(keras.Model):
    def __init__(self, n_classes: int = 2, **kwargs):
        super().__init__(**kwargs)
        self.n_classes = n_classes
        self.dense_1 = keras.layers.Dense(10, activation="relu")
        self.dense_2 = keras.layers.Dense(10, activation="relu")
        self.dense_3 = keras.layers.Dense(n_classes, activation="softmax")

    def call(self, inputs):
        x = self.dense_1(inputs)
        x = self.dense_2(x)
        x = self.dense_3(x)
        return x
