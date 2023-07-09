from __future__ import annotations

from typing import Any, Protocol

import numpy as np


class Method(Protocol):
    @property
    def name(self) -> str:
        ...  # pragma: no cover

    @property
    def n_parameters(self) -> int:
        ...  # pragma: no cover

    def compile(self, optimizer: Any, loss: Any, metrics: Any, *args, **kwargs) -> None:
        ...  # pragma: no cover

    def fit(self, x: Any, y: Any, *args, **kwargs) -> dict:
        ...  # pragma: no cover

    def predict(self, x: Any, *args, **kwargs) -> Any:
        ...  # pragma: no cover

    def evaluate(self, x: Any, y: Any, *args, **kwargs) -> dict:
        ...  # pragma: no cover

    def summary(self, *args, **kwargs) -> str | None:
        ...  # pragma: no cover

    def save(self, file_path: str, overwrite: bool, *args, **kwargs) -> None:
        ...  # pragma: no cover

    @classmethod
    def load(cls, file_path: str, *args, **kwargs) -> Method:
        ...  # pragma: no cover
