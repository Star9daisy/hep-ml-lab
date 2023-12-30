from __future__ import annotations

import re
import shutil
import subprocess

import pexpect
import ROOT

from ..types import Path, PathLike
from ..utils import get_madgraph5_run

_ = ROOT.gSystem.Load("libDelphes")  # type: ignore


class Madgraph5:
    def __init__(
        self,
        executable: PathLike,
        verbose: int = 1,
    ):
        self.executable = executable
        self.child = pexpect.spawn(f"{self.executable.as_posix()}")
        self.process_log = ""
        self.DEFAULT_LOG_DIR = Path("Logs")
        self.DEFAULT_DIAGRAM_DIR = Path("Diagrams")
        self.verbose = verbose

        self.process_log += self.run_command("")

    @property
    def executable(self) -> Path:
        return self._executable

    @executable.setter
    def executable(self, value: PathLike):
        if (_executable := shutil.which(value)) is None:
            raise FileNotFoundError(f"Could not find Madgraph5 executable {value}")

        self._executable = Path(_executable).resolve()

    @property
    def home(self) -> Path:
        return self.executable.parent.parent

    @property
    def version(self) -> str:
        _version = "unknown"
        with (self.home / "VERSION").open() as f:
            for line in f.readlines():
                if line.startswith("version") and _version == "unknown":
                    _version = line.split("=")[1].strip()

        return _version

    def __repr__(self):
        return f"Madgraph5 v{self.version}"

    def run_command(
        self,
        command: str,
        start_marker: str = r"\r\n",
        end_marker: str = r"MG5_aMC>$",
        timeout: int | None = None,
    ) -> str:
        output = ""
        self.child.sendline(command)
        while True:
            if self.child.expect([start_marker, end_marker], timeout) == 1:  # type: ignore
                break

            middle_output = self.child.before.decode()
            output += middle_output + "\r\n"
            if self.verbose > 0:
                print(middle_output)

        self.clean_pypy()
        return output

    def clean_pypy(self):
        py_py = Path("py.py")
        if py_py.exists():
            py_py.unlink()

    def import_model(self, model: PathLike):
        self.process_log += self.run_command(f"import model {model}")

    def define(self, expression: str):
        self.process_log += self.run_command(f"define {expression}")

    def generate(self, *processes: str):
        self.process_log += self.run_command(f"generate {processes[0]}")
        for process in processes[1:]:
            self.process_log += self.run_command(f"add process {process}")

    def display_diagrams(self, diagram_dir: PathLike = "Diagrams"):
        self.diagram_dir = Path(diagram_dir)
        if self.diagram_dir.exists():
            raise FileExistsError(f"{self.diagram_dir} already exists")

        self.diagram_dir.mkdir(parents=True)
        self.process_log += self.run_command(f"display diagrams {self.diagram_dir}")

        for eps in self.diagram_dir.glob("*.eps"):
            subprocess.run(f"ps2pdf {eps} {eps.with_suffix('.pdf')}", shell=True)

    def output(self, output_dir: PathLike | None = None, overwrite: bool = True):
        if output_dir is None:
            log = self.run_command(f"output")
            self.process_log += log

            match = re.findall(r"Output to directory (.+) done.", log)
            self.output_dir = Path(match[0])
        else:
            self.output_dir = Path(output_dir)
            if self.output_dir.exists():
                if overwrite:
                    shutil.rmtree(self.output_dir)
                else:
                    raise FileExistsError(f"{self.output_dir} already exists")
            self.process_log += self.run_command(f"output {self.output_dir}")

        try:
            if self.diagram_dir.exists():
                self.diagram_dir = self.diagram_dir.rename(self.DEFAULT_DIAGRAM_DIR)
                shutil.move(self.diagram_dir, self.output_dir / self.diagram_dir)
        except AttributeError:
            self.display_diagrams(self.output_dir / self.DEFAULT_DIAGRAM_DIR)

        self.log_dir = self.output_dir / self.DEFAULT_LOG_DIR
        self.log_dir.mkdir()
        process_log_file = self.log_dir / "process.log"

        with process_log_file.open("w") as f:
            f.write(self.process_log)
        if self.verbose > 0:
            print("Process log saved to", process_log_file.relative_to(Path.cwd()))

    def launch(
        self,
        shower="off",
        detector="off",
        settings={},
        cards=[],
        multi_run=1,
        seed=0,
        output_dir: PathLike | None = None,
    ):
        run_log = ""
        if self.output_dir is None:
            if output_dir is None:
                raise ValueError("No output directory specified")
            else:
                self.output_dir = Path(output_dir)
                self.log_dir = self.output_dir / self.DEFAULT_LOG_DIR
                self.log_dir.mkdir()

        # In the middle: MadEvent CLI ends with '>'
        commands = f"launch -i {self.output_dir}\n"
        if multi_run == 1:
            commands += "generate_events\n"
        else:
            commands += f"multi_run {multi_run}\n"

        commands += f"shower={shower}\n"
        commands += f"detector={detector}\n"
        commands += "done\n"

        settings["iseed"] = seed
        if settings != {}:
            commands += "\n".join([f"set {k} {v}" for k, v in settings.items()])
            commands += "\n"

        if cards != []:
            commands += "\n".join(cards) + "\n"
        commands += "done\n"

        run_log += self.run_command(commands, end_marker=r">$")

        # In the end: Back to Madgraph CLI
        run_log += self.run_command("exit")

        run_name = re.findall(r"survey  (.+) \r\n", run_log)[0]
        run_log_file = self.log_dir / f"{run_name}.log"
        with run_log_file.open("w") as f:
            f.write(run_log)
        print(f"Run log saved to", run_log_file.relative_to(Path.cwd()))

    @property
    def runs(self) -> list[Madgraph5Run]:
        run_paths = []
        for i in self.output_dir.glob("Events/run_*"):
            if i.is_dir() and i.name.count("_") == 1:
                run_paths.append(i)

        # Sort the runs by their number
        run_paths = sorted(run_paths, key=lambda x: int(x.name.split("_")[-1]))
        runs = [Madgraph5Run(self.output_dir, i.name) for i in run_paths]

        return runs

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
        if n_events == 0:
            n_events = self._info["n_events"]

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
