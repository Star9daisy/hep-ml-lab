import re


def parse_branch(branch: str):
    if re.match(r"^([A-Za-z]+)$", branch):
        branch += ":"

    if match := re.match(r"^([A-Za-z]+)(\d+)$", branch):
        obj, index = match.groups()
        start = int(index)
        stop = start + 1
    elif match := re.match(r"^([A-Za-z]+)(\d*:?\d*)$", branch):
        obj, agnostic_index = match.groups()
        indices = agnostic_index.split(":")
        if indices[0] == "" and indices[1] == "":
            start = 0
            stop = None
        elif indices[0] == "" and indices[1] != "":
            start = 0
            stop = int(indices[1])
        elif indices[0] != "" and indices[1] == "":
            start = int(indices[0])
            stop = None
        else:
            start = int(indices[0])
            stop = int(indices[1])
    else:
        return

    return obj, start, stop


def parse_physics_object(physics_object: str):
    output = []
    for phyobj_name in physics_object.split(","):
        item = {}

        if "." not in phyobj_name:
            item["main"] = parse_branch(phyobj_name)
            output.append(item)
        else:
            main, sub = phyobj_name.split(".")
            item["main"] = parse_branch(main)
            item["sub"] = parse_branch(sub)
            output.append(item)
    return output


def get_observable():
    ...


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
