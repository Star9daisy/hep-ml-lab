from __future__ import annotations

import copy
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import cppyy
import ROOT

ROOT.gSystem.Load("libDelphes")


class Madgraph5:
    """Wrapper of Madgraph5 CLI to simulate colliding events.

    Madgraph5 is a wrapper class of Madgraph5 CLI. It mainly provides functionalities to generate
    events, run parton shower and detector simulation, and access to the launched runs.

    Parameters
    ----------
    executable:
        The executable file of Madgraph5.
    processes:
        The processes to be generated.
    output_dir:
        The directory where the events will be outputted.
    model:
        The particle physics model to be used.
    definitions:
        The definitions of multiparticle.
    shower:
        The parton shower tool to be used.
    detector:
        The detector simulation tool to be used.
    settings:
        The phase space and parameter settings.
    cards:
        Shower and detector configuration cards.

    Parameters correspond to commands in Madgraph5 CLI or options after launching generation in
    Madgraph5.

    | Parameters  | Madgraph5 commands or options    |
    |-------------|----------------------------------|
    | processes   | generate & add process commands  |
    | output_dir  | output command                   |
    | model       | import model command             |
    | definitions | define command                   |
    | shower      | shower option                    |
    | detector    | detector option                  |
    | settings    | set command                      |
    | cards       | paths of cards                   |
    """

    def __init__(
        self,
        executable: str | Path,
        output: str | Path,
        model: str = "sm",
        definitions: dict[str, str] = {},
        processes: str | list[str] = "",
        shower: str = "Pythia8",
        detector: str = "Delphes",
        settings: dict[str, Any] = {},
        cards: list[str | Path] = [],
    ) -> None:
        self._executable = Path(executable)
        self._output = Path(output)
        self._model = model
        self._definitions = definitions

        if isinstance(processes, list):
            self._processes = processes
        else:
            self._processes = [processes]

        self.shower = shower
        self.detector = detector
        self.settings = settings
        self.cards = [Path(card) for card in cards]

    @property
    def executable(self) -> Path:
        """The executable file of Madgraph5."""
        return self._executable

    @property
    def output(self) -> Path:
        """The directory where all generation information is stored."""
        return self._output

    @property
    def model(self) -> str:
        """The particle physics theory model to be used."""
        return self._model

    @property
    def definitions(self) -> dict[str, str]:
        """The definitions of multiparticle."""
        return self._definitions

    @property
    def processes(self) -> list[str]:
        """The processes to be generated."""
        return self._processes

    @property
    def commands(self) -> list[str]:
        """Commands converted from parameters to be executed in Madgraph5."""
        return self._parameters_to_commands()

    @property
    def runs(self) -> list[MG5Run]:
        """Madgraph5 runs after finishing event generation."""
        all_run_dir = self.output_dir / "Events"
        run_dirs = all_run_dir.glob("run_*")
        mg5_runs = [MG5Run(i) for i in run_dirs]
        return mg5_runs

    def launch(self, new_output: bool = False, show_status: bool = True) -> None:
        """Launch Madgraph5 to generate events.

        Parameters
        ----------
        new_output:
            If True, remove the existing output directory and generate new events, else create a new
            run.
        show_status:
            If True, print the status of the launched run, else launch silently.
        """

        executable = shutil.which(self.executable)
        if not executable:
            raise EnvironmentError(f"No Madgraph executable file found for '{self.executable}'")

        if self.output_dir.exists():
            if new_output:
                shutil.rmtree(self.output_dir)
                self.output_dir.mkdir(parents=True)
                temp_file_path = self._commands_to_file(self.commands)
            else:
                temp_file_path = self._commands_to_file([f"launch {self.output_dir}"])
        else:
            self.output_dir.mkdir(parents=True)
            temp_file_path = self._commands_to_file(self.commands)

        # Launch Madgraph5 and redirect output to a log file
        with open(f"{self.output_dir}.log", "w") as f:
            process = subprocess.Popen(
                f"{executable} {temp_file_path}",
                shell=True,
                stdout=f,
                stderr=subprocess.STDOUT,
            )

        # Check and print status
        status = ""
        while status != "Done" or process.poll() is None:
            last_status = self._check_status(status)
            if last_status != status:
                if show_status and last_status != "":
                    print(last_status)
                status = last_status
            time.sleep(0.1)

        # Remove py.py file
        if Path("py.py").exists():
            Path("py.py").unlink()

    def _commands_to_file(self, commands: list[str]) -> str:
        """Write commands to a temporary file and return the path of the file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write("\n".join(commands))
            temp_file_path = temp_file.name
        return temp_file_path

    def _check_status(self, last_status: str) -> str:
        """Check the status of the launched run."""
        with open(f"{self.output_dir}.log", "r") as f:
            contents = f.readlines()
        for line in contents[::-1]:
            if line.startswith("Generating"):
                last_status = "Generating events..."
                break
            elif "Running Pythia8" in line:
                last_status = "Running Pythia8..."
                break
            elif "Running Delphes" in line:
                last_status = "Running Delphes..."
                break
            elif "INFO: storing files" in line:
                last_status = "Storing files..."
                break
            elif line.startswith("INFO: Done"):
                last_status = "Done"
                break

        return last_status

    def _parameters_to_commands(self) -> list[str]:
        """Convert parameters to a list of Madgraph5 commands."""
        # Model
        commands = [f"import model {str(self.model)}"]

        # Definitions
        if self.definitions:
            commands += [f"define {k} = {v}" for k, v in self.definitions.items()]
            commands += [""]

        # Processes
        if isinstance(self.processes, str):
            commands += [f"generate {self.processes}"]
        elif isinstance(self.processes, list):
            commands += [f"generate {self.processes[0]}"]
            commands += [f"add process {p}" for p in self.processes[1:]]
        else:
            raise TypeError("processes must be str or list[str]")

        # Output
        commands += [f"output {Path(self.output_dir).absolute()}"]

        # Launch
        commands += ["launch"]

        # Shower
        if self.shower:
            commands += [f"    shower={self.shower}"]

        # Detector
        if self.detector:
            commands += [f"    detector={self.detector}"]

        # Settings
        if self.settings:
            commands += [f"    set {k} {v}" for k, v in self.settings.items()]

        # Cards
        if self.cards:
            commands += [f"    {c.absolute()}" for c in self.cards]

        return commands


@dataclass
class MG5Run:
    """MG5Run stores the information of a Madgraph5 run.

    Parameters
    ----------
    directory: str | Path
        The directory path to a run.

    Attributes
    ----------
    directory: Path
        The directory path to a run.
    banner: Path
        The path to the banner file of a run.
    tag: str
        The tag of a run.
    cross_section: float
        The cross section of a run.
    n_events: int
        The number of events generated in a run.
    n_subruns: int
        The number of subruns in a run.
    events: TCahin
        The events generated in a run.
    """

    directory: str | Path
    banner: Path = field(default_factory=Path, init=False, repr=False)
    tag: str = field(default="", init=False)
    cross_section: float = field(default=0.0, init=False)
    n_events: int = field(default=0, init=False)
    n_subruns: int = field(default=0, init=False, repr=False)
    events: cppyy.gbl.TChain = field(init=False, repr=False)

    def __post_init__(self):
        self.directory = Path(self.directory)
        self.banner = self.directory.parent / f"{self.directory.name}_banner.txt"

        self.events = ROOT.TChain("Delphes")
        for file in self.directory.parent.glob(f"{self.directory.name}*/*.root"):
            self.n_subruns += 1
            self.events.Add(file.as_posix())

        with open(self.banner) as file:
            contents = file.readlines()
        for line in contents:
            if line.endswith("name of the run \n"):
                self.tag = line.split()[0]
        for line in contents[::-1]:
            if line.startswith("#  Number of Events"):
                self.n_events = int(line.split()[-1])
            if line.startswith("#  Integrated weight"):
                self.cross_section = float(line.split()[-1])
