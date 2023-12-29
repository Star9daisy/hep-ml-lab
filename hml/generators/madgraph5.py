from __future__ import annotations

import ROOT

from ..types import Path, PathLike
from ..utils import get_madgraph5_run

_ = ROOT.gSystem.Load("libDelphes")  # type: ignore


class Madgraph5:
    ...


class Madgraph5Run:
    def __init__(self, output_dir: PathLike, name: str):
        self.output_dir = Path(output_dir)
        self._events_dir = self.output_dir / "Events"
        self._run_dir = self._events_dir / name

        self._info = get_madgraph5_run(output_dir, name)
        self._subs = []
        for i in self._events_dir.glob(f"{name}_*"):
            if i.is_dir():
                self._subs.append(i)

    @property
    def directory(self) -> Path:
        return self._run_dir

    @property
    def name(self) -> str:
        return self._info["name"]

    @property
    def collider(self) -> str:
        return self._info["collider"]

    @property
    def tag(self) -> str:
        return self._info["tag"]

    @property
    def seed(self) -> int:
        return self._info["seed"]

    @property
    def cross(self) -> float:
        return self._info["cross"]

    @property
    def error(self) -> float:
        return self._info["error"]

    @property
    def n_events(self) -> int:
        n_events = self.events().GetEntries()
        return n_events

    @property
    def sub_runs(self) -> list[Madgraph5Run]:
        return [Madgraph5Run(self.output_dir, i.name) for i in self._subs]

    def events(self, file_format="root") -> ROOT.TChain | Any:  # type: ignore
        if file_format == "root":
            events = ROOT.TChain("Delphes")  # type: ignore
            if self.sub_runs != []:
                for run in self.sub_runs:
                    for root_file in run.directory.glob("*.root"):
                        events.Add(root_file.as_posix())
            else:
                for root_file in self.directory.glob("*.root"):
                    events.Add(root_file.as_posix())
        else:
            raise NotImplementedError(f"File format {file_format} not supported yet.")

        return events

    def __repr__(self) -> str:
        head = self.name
        if self.sub_runs != []:
            head += f" ({len(self.sub_runs)} sub runs)"
        return (
            f"Madgraph5Run {head}:\n"
            f"- collider: {self.collider}\n"
            f"- tag: {self.tag}\n"
            f"- seed: {self.seed}\n"
            f"- cross: {self.cross}\n"
            f"- error: {self.error}\n"
            f"- n_events: {self.n_events}"
        )
