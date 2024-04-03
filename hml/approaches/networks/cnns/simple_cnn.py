from keras import Model
from keras.layers import (
    Conv2D,
    Dense,
    Dropout,
    GlobalAveragePooling2D,
    Input,
    MaxPooling2D,
)


class SimpleCNN:
    def __init__(self, input_shape, name="simple_cnn"):
        self.input_shape = input_shape
        self.name = name
        self.model = self._init_model()

    def _init_model(self):
        inputs = Input(shape=self.input_shape)
        x = Conv2D(filters=8, kernel_size=3, padding="same", activation="relu")(inputs)
        x = MaxPooling2D()(x)
        x = Conv2D(filters=16, kernel_size=3, padding="same", activation="relu")(x)
        x = MaxPooling2D()(x)
        x = Conv2D(filters=32, kernel_size=3, padding="same", activation="relu")(x)
        x = MaxPooling2D()(x)
        x = GlobalAveragePooling2D()(x)
        x = Dense(units=10, activation="relu")(x)
        x = Dropout(rate=0.5)(x)
        outputs = Dense(units=2, activation="softmax")(x)

        return Model(inputs=inputs, outputs=outputs, name=self.name)

    def compile(
        self,
        optimizer="rmsprop",
        loss=None,
        metrics=None,
        **kwargs,
    ):
        self.model.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=metrics,
            **kwargs,
        )

    def fit(
        self,
        x=None,
        y=None,
        batch_size=None,
        epochs=1,
        **kwargs,
    ):
        return self.model.fit(
            x,
            y,
            batch_size=batch_size,
            epochs=epochs,
            **kwargs,
        )

    def predict(self, x=None, **kwargs):
        return self.model.predict(x, **kwargs)

    def summary(self):
        return self.model.summary()

    def save(self, filepath, overwrite=True):
        self.model.save(filepath, overwrite=overwrite)
