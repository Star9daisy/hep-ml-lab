import sys
from io import StringIO
from typing import Any, Protocol

from keras.utils.layer_utils import count_params


class Model(Protocol):
    def compile(self, optimizer: Any, loss: Any, metrics: Any):
        pass

    def fit(self, x_train: Any, y_train: Any):
        pass

    def summary(self):
        pass

    def save(self, path: str, suffix: str):
        pass


class KerasModel:
    def __init__(self, model, name="keras_model"):
        self.model = model
        self.name = model.name if not name else name

    def compile(self, *args, **kwargs):
        self.model.compile(*args, **kwargs)

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)

    def predict(self, x, *args, **kwargs):
        y_prob = self.model.predict(x, *args, **kwargs)
        y_pred = y_prob.argmax(1)
        return y_pred

    def predict_proba(self, x, *args, **kwargs):
        y_prob = self.model.predict(x, *args, **kwargs)
        return y_prob

    @property
    def description(self):
        stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        self.model.summary()
        sys.stdout = stdout
        return output_buffer.getvalue()

    @property
    def n_parameters(self):
        trainable_params = count_params(self.model.trainable_weights)
        return trainable_params
