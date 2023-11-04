from __future__ import annotations

import os
import pty
import shutil
import subprocess
import tempfile
from dataclasses import dataclass

import ROOT
from rich.console import Console
from rich.table import Table

from .types import Any, DetectorOption, Path, PathLike, ShowerOption

_ = ROOT.gSystem.Load("libDelphes")  # type: ignore


class Madgraph5:
    """Wrapper class for Madgraph5.

    It uses commands from MadEvent (`launch -i` in Madgraph5 CLI) to launch runs
    sequentially. It also provides a summary of the runs similar to the website
    provided by Madgraph5.

    Parameters
    ----------
    processes : list[str]
        List of processes to generate.
    executable : PathLike, optional
        Path to the Madgraph5 executable, by default "mg5_aMC".
    model : PathLike, optional
        Path to the model or the name of the model, by default "sm".
    definitions : dict[str, Any], optional
        Dictionary of definitions to pass to Madgraph5, by default {}.
    output : PathLike, optional
        Path to the output directory, by default "madevent".
    log_dir : PathLike, optional
        Path to the log directory relative to the output, by default "Logs".

    The relation between the parameters and the Madgraph5 commands is as follows:

    | Parameters  | Commands or options              |
    | ----------- | -------------------------------- |
    | model       | import model command             |
    | definitions | define command                   |
    | processes   | generate & add process commands  |
    | output      | output command                   |
    """

    def __init__(
        self,
        processes: list[str],
        executable: PathLike = "mg5_aMC",
        model: PathLike = "sm",
        definitions: dict[str, Any] = {},
        output: PathLike = "madevent",
        log_dir: PathLike = "Logs",
    ) -> None:
        # Set properties ----------------------------------------------------- #
        self.executable = executable
        self.model = model
        self.definitions = definitions
        self.processes = processes
        self.output = Path(output)

        self.commands = {
            "pre": [
                *[f"import model {self.model}"],
                *[f"define {k} = {v}" for k, v in self.definitions.items()],
                *[f"generate {self.processes[0]}"],
                *[f"add process {p}" for p in self.processes[1:]],
                *[f"output {self.output}"],
            ],
        }

        # Create output directory -------------------------------------------- #
        command_file = self._cmds_to_file(self.commands["pre"])

        if not self.output.exists():
            # Run Madgraph5
            process = subprocess.Popen(
                f"{self.executable} {command_file}",
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Remove py.py file
            while process.poll() is None:
                if Path("py.py").exists():
                    Path("py.py").unlink()

            # Check if there's an error message in stderr
            # Note:
            # when importing a model like heft that needs to be downloaded,
            # the success message is wrongly printed in stderr. This is why we
            # check for the word "error" in stderr.
            _, stderr = process.communicate()
            if "error" in stderr.decode().lower():
                # if stderr:
                raise RuntimeError(stderr.decode())

        # After output directory is created, set log directory
        self.log_dir = log_dir

    def launch(
        self,
        shower: ShowerOption = "off",
        detector: DetectorOption = "off",
        settings: dict[str, Any] = {},
        cards: list[PathLike] = [],
        multi_run: int = 1,
        verbose: int = 1,
    ):
        """The launch command in Madgraph5 CLI.

        Parameters
        ----------
        shower : ShowerOption, optional
            Shower tool to use, currently supports "off" and "pythia8", by
            default "off".
        detector : DetectorOption, optional
            Detector tool to use, currently supports "off" and "delphes", by
            default "off".
        settings : dict[str, Any], optional
            Dictionary of settings to pass to Madgraph5, by default {}.
        cards : list[PathLike], optional
            List of cards to pass to Madgraph5, by default [].
        multi_run : int, optional
            Number of runs to launch, by default 1.
        verbose : int, optional
            Verbosity level, 0 for quiet, 1 for simple, by default 1.

        The relation between the parameters and the Madgraph5 commands is as
        follows:

        | shower      | shower option                                     |
        | detector    | detector option                                   |
        | settings    | set command                                       |
        | cards       | card paths directly passed when configuring cards |
        """

        if shower not in ["off", "pythia8"]:
            raise ValueError(f"Unknown shower tool {shower}")
        if detector not in ["off", "delphes"]:
            raise ValueError(f"Unknown detector tool {detector}")

        self.shower = shower
        self.detector = detector
        self.settings = settings
        self.cards = [Path(card).resolve() for card in cards]
        self.multi_run = multi_run

        # -------------------------------------------------------------------- #
        commands = [
            *[f"launch -i {self.output}"],
            *[f"multi_run {self.multi_run}"],
            *[f"shower={self.shower}"],
            *[f"detector={self.detector}"],
            *[f"set {k} {v}" for k, v in self.settings.items()],
            *[f"{card}" for card in self.cards],
        ]
        command_file = self._cmds_to_file(commands)

        # -------------------------------------------------------------------- #
        n_runs = len(list((self.output / "Events").glob("*_banner.txt")))
        run_name = f"run_{n_runs+1:02d}"
        log_file = self.log_dir / f"{run_name}.log"
        self.commands[run_name] = commands

        # -------------------------------------------------------------------- #
        with open(log_file, "w") as f:
            _, child = pty.openpty()
            process = subprocess.Popen(
                f"{self.executable} {command_file}",
                shell=True,
                stdin=child,
                stdout=f,
                stderr=child,
            )

        # -------------------------------------------------------------------- #
        self._check_status(log_file, process, verbose)
        os.close(child)

        # -------------------------------------------------------------------- #
        _, stderr = process.communicate()
        if stderr:
            raise RuntimeError(stderr.decode())  # pragma: no cover

        # -------------------------------------------------------------------- #
        return Madgraph5MultiRun.from_name(run_name, self.output)

    @property
    def executable(self) -> Path:
        return self._executable

    @executable.setter
    def executable(self, value: PathLike):
        if (_executable := shutil.which(value)) is None:
            raise EnvironmentError(f"{value} is not a valid executable")

        self._executable = Path(_executable).resolve()

    @property
    def model(self) -> PathLike:
        return self._model

    @model.setter
    def model(self, value: PathLike):
        self._model = value

    @property
    def definitions(self) -> dict[str, Any]:
        return self._definitions

    @definitions.setter
    def definitions(self, value: dict[str, Any]):
        self._definitions = value

    @property
    def processes(self) -> list[str]:
        return self._processes

    @processes.setter
    def processes(self, value: list[str]):
        self._processes = value

    @property
    def output(self) -> Path:
        return self._output

    @output.setter
    def output(self, value: PathLike):
        _output = Path(value).resolve()
        self._output = _output

    @property
    def log_dir(self) -> Path:
        return self._log_dir

    @log_dir.setter
    def log_dir(self, value: PathLike):
        _log_dir = self.output / value
        _log_dir.mkdir(exist_ok=True)
        self._log_dir = _log_dir

    @property
    def runs(self) -> list[Madgraph5MultiRun]:
        """List of runs in the output directory."""
        runs = []
        for i in self.output.glob("Events/run_*"):
            if i.is_dir() and i.name.count("_") == 1:
                runs.append(Madgraph5MultiRun.from_name(i.name, self.output))

        return runs

    @classmethod
    def from_output(cls, output: PathLike, executable: PathLike = "mg5_aMC"):
        """Create a Madgraph5 instance from an existing output directory."""
        output = Path(output).resolve()
        if not output.exists():
            raise FileNotFoundError(f"{output} does not exist.")

        proc_card = output / "Cards/proc_card_mg5.dat"

        model = "sm"
        definitions = {}
        processes = []

        with proc_card.open() as f:
            for line in f.readlines():
                if line.startswith("import model"):
                    model = line.split()[2]
                if line.startswith("define"):
                    key, value = line.replace("define ", "").split("=")
                    definitions[key.strip()] = value.strip()

                if line.startswith("generate"):
                    processes.append(line.replace("generate ", "").strip())

                if line.startswith("add process"):
                    processes.append(line.replace("add process ", "").strip())

        return cls(
            processes=processes,
            executable=executable,
            model=model,
            definitions=definitions,
            output=output,
        )

    def summary(self):
        """Print a summary of the runs in the output directory."""
        console = Console()
        table = Table(
            title="\n".join(self.processes),
            caption=f"Output: {self.output}",
        )

        table.add_column("#", justify="right")
        table.add_column("Name")
        table.add_column("Tag")
        table.add_column("Cross section (pb)", justify="center")
        table.add_column("N events", justify="right")
        table.add_column("Seed", justify="right")

        for i, multi_run in enumerate(self.runs):
            table.add_row(
                f"{i}",
                f"{multi_run.name}[{len(multi_run.runs)}]",
                f"{multi_run.tag}",
                f"{multi_run.cross_section:.3e}",
                f"{multi_run.n_events:,}",
                f"{multi_run.seed}",
            )

        console.print(table)

    def _cmds_to_file(self, cmds: list[str]) -> str:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write("\n".join(cmds))
            temp_file_path = temp_file.name
        return temp_file_path

    def _check_status(
        self,
        log_file: Path,
        process: subprocess.Popen,
        verbose=1,
    ) -> None:
        # -------------------------------------------------------------------- #
        status_markers = {
            "Running Survey": "Running Survey",
            "Running Pythia8": "Running Pythia8",
            "Running Delphes": "Running Delphes",
            "storing files": "Storing files",
        }

        current_run = 1
        last_position = 0
        last_known_status = -1  # This will help to avoid repeating the same status.

        # Determine the index of the "storing files" status, since it's the
        # repeating endpoint for each run
        storing_files_idx = list(status_markers.keys()).index("storing files")

        # -------------------------------------------------------------------- #
        # Monitor the process and the log file
        while True:
            if Path("py.py").exists():
                Path("py.py").unlink()

            # Check the log file for status updates
            with open(log_file, "r") as f:
                f.seek(last_position)
                content = f.read()
                last_position = f.tell()

                for idx, (marker, status) in enumerate(status_markers.items()):
                    if marker in content and idx > last_known_status:
                        if verbose:
                            print(status)
                        if idx == storing_files_idx:
                            current_run += 1
                            if current_run > self.multi_run:
                                last_known_status = idx
                            else:
                                last_known_status = -1
                            if verbose:
                                print()
                        else:
                            last_known_status = idx

            # Check if process is still running
            if process.poll() is not None:  # Process has finished
                if verbose:
                    print("Done")
                break


@dataclass
class Madgraph5Run:
    """A single run of Madgraph5.

    Single run includes complete information about the run. It is usually
    launced by the `launch` command in Madgraph5 CLI or the `generate_events`
    command in MadEvent CLI.

    Parameters
    ----------
    name : str
        Name of the run, e.g. "run_01", "run_02_0".
    tag : str
        Tag of the run, by default "" (not the same as "tag_1" in Madgraph5).
    directory : PathLike
        Path to the directory of the run.
    seed : int
        Random seed of the run.
    n_events : int
        Number of events in the run parsed from the banner file and the root
        files. The latter shall prevail.
    cross_section : float
        Cross section of the run.
    collider : str
        Collider configurations of the run.
    events : ROOT.TChain
        TChain of the root files in the run.
    """

    name: str
    tag: str
    directory: Path
    seed: int
    n_events: int
    cross_section: float
    collider: str
    events: ROOT.TChain  # type: ignore

    @classmethod
    def from_directory(cls, directory: PathLike):
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory} does not exist.")

        name = directory.name
        if len(banners := list(directory.glob("*_banner.txt"))) == 0:
            raise FileNotFoundError(f"No banner found in {directory}")
        else:
            banner = banners[0]

        lpps = {"1": "p", "2": "e"}
        tag = ""
        n_events = 0
        seed = 0
        lpp1, lpp2 = "", ""
        ebeam1, ebeam2 = 0.0, 0.0
        cross_section = 0.0
        events = ROOT.TChain("Delphes")  # type: ignore
        for root_file in directory.glob("*.root"):
            events.Add(str(root_file))

        with banner.open() as f:
            for line in f.readlines():
                if "run_tag" in line:
                    tag = line.split("=")[0].strip()

                if "nevents" in line:
                    n_events = int(line.split("=")[0].strip())
                    if n_events != events.GetEntries():
                        n_events = events.GetEntries()  # pragma: no cover

                if "iseed" in line:
                    seed = int(line.split("=")[0].strip())

                if "lpp1" in line:
                    lpp1 = lpps.get(line.split("=")[0].strip(), "")

                if "lpp2" in line:
                    lpp2 = lpps.get(line.split("=")[0].strip(), "")

                if "ebeam1" in line:
                    ebeam1 = float(line.split("=")[0].strip())

                if "ebeam2" in line:
                    ebeam2 = float(line.split("=")[0].strip())

                if "Integrated weight (pb)" in line:
                    cross_section = float(line.split()[-1].strip())

        collider = f"{lpp1}{lpp2}: {ebeam1}x{ebeam2}"

        return cls(
            name, tag, directory, seed, n_events, cross_section, collider, events
        )


@dataclass
class Madgraph5MultiRun:
    """A run launched by multi_run of MadEvent.

    A multi-run is a collection of runs launched by the `multi_run` command in
    MadEvent CLI that is launched by the `launch -i` command in Madgraph5 CLI.
    It usually contains one "run_xx" directory, one "run_xx_banner.txt" file,
    and several "run_xx_y" single runs.

    Parameters
    ----------
    name : str
        Name of the run, e.g. "run_01".
    tag : str
        Tag of the run, by default "" (not the same as "tag_1" in Madgraph5).
    seed : int
        Random seed of the run.
    n_events : int
        Number of events in the run parsed from the banner file and the root
        files. The latter shall prevail.
    cross_section : float
        Cross section of the run.
    collider : str
        Collider configurations of the run.
    events : ROOT.TChain
        TChain of the root files in the run.
    runs : list[Madgraph5Run]
        The single runs in the multi-run.
    """

    name: str
    tag: str
    seed: int
    n_events: int
    cross_section: float
    collider: str
    events: ROOT.TChain  # type: ignore
    runs: list[Madgraph5Run]

    @classmethod
    def from_name(cls, name: str, output: PathLike = "madevent"):
        """Create a multi-run from the name of the run and the output directory."""
        output = Path(output)
        if not output.exists():
            raise FileNotFoundError(f"{output} does not exist.")

        events_dir = output / "Events"
        if len(banners := list(events_dir.glob(f"{name}_banner.txt"))) == 0:
            raise FileNotFoundError(f"No run named {name} found in {output}")
        else:
            banner = banners[0]

        runs = [i for i in events_dir.glob(f"{name}_*") if i.is_dir()]
        runs = sorted(runs, key=lambda x: int(x.name.split("_")[-1]))
        runs = [Madgraph5Run.from_directory(run) for run in runs]

        lpps = {"1": "p", "2": "e"}
        tag = ""
        n_events = 0
        seed = 0
        lpp1, lpp2 = "", ""
        ebeam1, ebeam2 = 0.0, 0.0
        cross_section = 0.0
        events = ROOT.TChain("Delphes")  # type: ignore
        for root_file in events_dir.glob(f"{name}_*/*.root"):
            events.Add(str(root_file))

        with banner.open() as f:
            for line in f.readlines():
                if "run_tag" in line:
                    tag = line.split("=")[0].strip()

                if "nevents" in line:
                    n_events = int(line.split("=")[0].strip())
                    if n_events != events.GetEntries() and events.GetEntries() != 0:
                        n_events = events.GetEntries()

                if "iseed" in line:
                    seed = int(line.split("=")[0].strip())

                if "lpp1" in line:
                    lpp1 = lpps.get(line.split("=")[0].strip(), "")

                if "lpp2" in line:
                    lpp2 = lpps.get(line.split("=")[0].strip(), "")

                if "ebeam1" in line:
                    ebeam1 = float(line.split("=")[0].strip())

                if "ebeam2" in line:
                    ebeam2 = float(line.split("=")[0].strip())

                if "Integrated weight (pb)" in line:
                    cross_section = float(line.split()[-1].strip())

        collider = f"{lpp1}{lpp2}: {ebeam1}x{ebeam2}"

        return cls(
            name,
            tag,
            seed,
            n_events,
            cross_section,
            collider,
            events,
            runs,
        )
