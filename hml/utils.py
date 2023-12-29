import re
from pathlib import Path

from bs4 import BeautifulSoup

from .types import PathLike


def get_madgraph5_run(output_dir: PathLike, name: str):
    output_dir = Path(output_dir)
    events_dir = output_dir / "Events"
    run_dir = events_dir / name

    if list(run_dir.glob("*_banner.txt")) != []:
        banner_file = list(run_dir.glob("*_banner.txt"))[0]
    elif events_dir.glob(f"{name}_banner.txt") != []:
        banner_file = list(events_dir.glob(f"{name}_banner.txt"))[0]
    else:
        raise FileNotFoundError("Banner file not found")

    crossx_file = output_dir / "crossx.html"

    with crossx_file.open() as f:
        soup = BeautifulSoup(f, "html.parser")

    table = soup.find("table")
    run = {}
    for row in table.find_all("tr")[1:]:  # type: ignore
        columns = row.find_all("td")
        if columns[0].text != name:
            continue

        # Name
        run["name"] = name

        # Collider
        collider_col = columns[1].text.split()
        lpp1, lpp2 = collider_col[:2]
        ebeam1, ebeam2 = collider_col[2], collider_col[4]
        run["collider"] = f"{lpp1}{lpp2}:{ebeam1}x{ebeam2}"

        # Banner
        banner_col = columns[2].text.split()
        run["tag"] = banner_col[0]

        with banner_file.open() as f:
            for line in f.readlines():
                if "iseed" in line:
                    run["seed"] = int(line.split("=")[0].strip())
                    break

        # Cross section and error
        cross_col = columns[3].text.split()
        cross = float(cross_col[0])
        error = float(cross_col[2])
        run["cross"] = cross
        run["error"] = error

        # N Events
        events_col = columns[4].text.split()
        run["n_events"] = int(events_col[0])

        # ROOT file path
        run["events"] = {}
        if list(run_dir.glob("*lhe*")) != []:
            run["events"]["lhe"] = list(run_dir.glob("*lhe*"))[0].as_posix()
        if list(run_dir.glob("*hepmc*")) != []:
            run["events"]["hepmc"] = list(run_dir.glob("*hepmc*"))[0].as_posix()
        if list(run_dir.glob("*.root")) != []:
            run["events"]["root"] = list(run_dir.glob("*.root"))[0].as_posix()

    return run


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
