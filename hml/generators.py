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


    Examples
    --------
    >>> from hml.generators import Madgraph5
    Welcome to JupyROOT 6.24/02
    >>> g = Madgraph5(
            processes="p p > z j, z > j j",
            output_dir="./data/pp2zjj",
            shower="Pythia8",
            detector="Delphes",
            settings={"nevents": 1000, "iseed": 42}
        )
    >>> g.launch()
    Generating events...
    Running Pythia8...
    Running Delphes...
    """

    def __init__(
        self,
        executable: str,
        processes: str | list[str],
        output_dir: str | Path,
        model: str = "sm",
        definitions: dict[str, str] | None = None,
        shower: str | None = None,
        detector: str | None = None,
        settings: dict[str, Any] | None = None,
        cards: list[str | Path] | None = None,
    ) -> None:
        self.executable = executable
        self.processes = processes
        self.output_dir = Path(output_dir)
        self.model = model
        self.definitions = definitions
        self.shower = shower
        self.detector = detector
        self.settings = settings
        self.cards = [Path(card) for card in cards] if cards else None

    @property
    def commands(self) -> list[str]:
        """Commands converted from parameters to be executed in Madgraph5."""
        return self._params_to_cmds()

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

        # Save cmds to a temporary file
        def _cmds_to_file(cmds: list[str]) -> str:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
                temp_file.write("\n".join(cmds))
                temp_file_path = temp_file.name
            return temp_file_path

        if self.output_dir.exists():
            if new_output:
                shutil.rmtree(self.output_dir)
                self.output_dir.mkdir(parents=True)
                temp_file_path = _cmds_to_file(self.commands)
            else:
                temp_file_path = _cmds_to_file([f"launch {self.output_dir}"])
        else:
            self.output_dir.mkdir(parents=True)
            temp_file_path = _cmds_to_file(self.commands)

        # Launch Madgraph5
        def _check_status(last_status: str) -> str:
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
                elif line.startswith("INFO: Done"):
                    last_status = ""
                    break

            return last_status

        with open(f"{self.output_dir}.log", "w") as f:
            process = subprocess.Popen(
                f"{executable} {temp_file_path}",
                shell=True,
                stdout=f,
                stderr=subprocess.STDOUT,
            )

        # Check and print status
        status = ""
        while process.poll() is None:
            last_status = _check_status(status)
            if last_status != status:
                if show_status and last_status != "":
                    print(last_status)
                status = last_status
            time.sleep(1)

        # Remove py.py file
        if Path("py.py").exists():
            Path("py.py").unlink()

    def _params_to_cmds(self) -> list[str]:
        # Model
        cmds = [f"import model {str(self.model)}"]

        # Definitions
        if self.definitions:
            cmds += [f"define {k} = {v}" for k, v in self.definitions.items()]
            cmds += [""]

        # Processes
        if isinstance(self.processes, str):
            cmds += [f"generate {self.processes}"]
        elif isinstance(self.processes, list):
            cmds += [f"generate {self.processes[0]}"]
            cmds += [f"add process {p}" for p in self.processes[1:]]
        else:
            raise TypeError("processes must be str or list[str]")

        # Output
        cmds += [f"output {Path(self.output_dir).absolute()}"]

        # Launch
        cmds += ["launch"]

        # Shower
        if self.shower:
            cmds += [f"    shower={self.shower}"]

        # Detector
        if self.detector:
            cmds += [f"    detector={self.detector}"]

        # Settings
        if self.settings:
            cmds += [f"    set {k} {v}" for k, v in self.settings.items()]

        # Cards
        if self.cards:
            cmds += [f"    {c.absolute()}" for c in self.cards]

        return cmds


@dataclass
class MG5Run:
    """MG5Run stores the information of a Madgraph5 run.

    Parameters
    ----------
    run_dir:
        The directory path to a run.
    run_tag:
        The tag of a run.
    cross_section:
        The cross section of the process in a run.
    events:
        The events generated in a run.
    """

    run_dir: str | Path
    run_tag: str = field(init=False, default="tag_1")
    cross_section: float = field(init=False)
    events: cppyy.gbl.TTree = field(init=False)

    def __post_init__(self):
        self.run_dir = Path(self.run_dir)

        # Search for the banner file
        banner_file = list(self.run_dir.glob("*banner.txt"))[0]

        # Get the run tag from the banner file name and the run name
        _prefix = self.run_dir.name + "_"
        _suffix = "_banner.txt"
        self.run_tag = banner_file.name.replace(_prefix, "").replace(_suffix, "")

        # Search for cross section from the bottom of the banner file
        with open(banner_file, "r") as f:
            contents = f.readlines()
        self.cross_section = 0.0
        for line in contents[::-1]:
            if line.startswith("#  Integrated weight (pb)"):
                self.cross_section = float(line.split()[-1])
                break

        # Read the events from the .root file via ROOT.TFile
        event_file = self.run_dir / f"{self.run_tag}_delphes_events.root"
        event_file = ROOT.TFile(str(event_file))
        self.events = copy.deepcopy(event_file.Get("Delphes"))
