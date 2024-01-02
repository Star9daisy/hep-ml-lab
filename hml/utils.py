from .types import Observable


def get_observable(name: str, **kwargs):
    if len(parts := name.split(".")) == 1:
        physics_object, classname = "", parts[0]
    else:
        physics_object, classname = parts

    if classname not in Observable.ALL_OBSERVABLES:
        raise ValueError(f"Observable {classname} not found")

    return Observable.ALL_OBSERVABLES[classname](
        physics_object=physics_object, **kwargs
    )


def save_dataset():
    ...


def load_dataset():
    ...


def split_dataset():
    ...


def save_approach():
    ...


def load_approach():
    ...


def get_metric():
    ...
