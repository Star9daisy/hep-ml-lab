from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Union

import pexpect
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

PathLike = Union[str, Path]


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
        self._processes = [i for i in processes]
        self.process_log += self.run_command(f"generate {processes[0]}")
        for process in processes[1:]:
            self.process_log += self.run_command(f"add process {process}")

    @property
    def processes(self) -> list[str]:
        # 1st case: generate() has been called
        try:
            return self._processes
        except AttributeError:
            pass

        # 2nd case: from_output() has been called
        try:
            crossx = self.output_dir / "crossx.html"
            with crossx.open() as f:
                soup = BeautifulSoup(f, "html.parser")
                title_col = soup.find_all("h2")[0].text.strip()
                processes = re.findall(r"^Results in the .+ for (.+)", title_col)[0]
                return processes.split(",")
        except AttributeError:
            raise AttributeError("No processes defined yet")

    def display_diagrams(
        self, diagram_dir: PathLike = "Diagrams", overwrite: bool = True
    ):
        self.diagram_dir = Path(diagram_dir)
        if self.diagram_dir.exists():
            if not overwrite:
                raise FileExistsError(f"{self.diagram_dir} already exists")
            else:
                shutil.rmtree(self.diagram_dir)

        self.diagram_dir.mkdir(parents=True)
        self.process_log += self.run_command(f"display diagrams {self.diagram_dir}")

        for eps in self.diagram_dir.glob("*.eps"):
            subprocess.run(f"ps2pdf {eps} {eps.with_suffix('.pdf')}", shell=True)

    def output(self, output_dir: PathLike | None = None, overwrite: bool = True):
        if output_dir is None:
            log = self.run_command("output")
            self.process_log += log

            match = re.findall(r"Output to directory (.+) done.", log)
            self.output_dir = Path(match[0]).resolve()
        else:
            self.output_dir = Path(output_dir).resolve()
            if self.output_dir.exists():
                if overwrite:
                    shutil.rmtree(self.output_dir)
                else:
                    raise FileExistsError(f"{self.output_dir} already exists")
            self.process_log += self.run_command(f"output {self.output_dir}")

            # try:
            #     if self.diagram_dir.exists():
            #         self.diagram_dir = self.diagram_dir.rename(self.DEFAULT_DIAGRAM_DIR)
            #         shutil.move(self.diagram_dir, self.output_dir / self.diagram_dir)
            # except AttributeError:
            self.display_diagrams(self.output_dir / self.DEFAULT_DIAGRAM_DIR)

        self.log_dir = self.output_dir / self.DEFAULT_LOG_DIR
        self.log_dir.mkdir()
        process_log_file = self.log_dir / "process.log"
        process_log_file = process_log_file.resolve()

        with process_log_file.open("w") as f:
            f.write(self.process_log)
        if self.verbose > 0:
            if process_log_file.is_relative_to(Path.cwd()):
                print(
                    "Process log saved to",
                    process_log_file.relative_to(Path.cwd()),
                )
            else:
                print("Process log saved to", process_log_file)

    def launch(
        self,
        shower="off",
        detector="off",
        madspin="off",
        settings={},
        decays=[],
        cards=[],
        multi_run=1,
        seed=None,
        dry=False,
    ):
        run_log = ""

        # In the middle: MadEvent CLI ends with '>'
        commands = f"launch -i {self.output_dir}\n"
        if multi_run == 1:
            commands += "generate_events\n"
        else:
            commands += f"multi_run {multi_run}\n"

        commands += f"shower={shower}\n"
        commands += f"detector={detector}\n"
        commands += f"madspin={madspin}\n"
        commands += "done\n"

        if seed is not None:
            settings["iseed"] = seed
        if settings != {}:
            commands += "\n".join([f"set {k} {v}" for k, v in settings.items()])
            commands += "\n"

        if decays != []:
            commands += "\n".join([f"decay {i}" for i in decays]) + "\n"

        default_pythia8_card = self.output_dir / "Cards/pythia8_card_default.dat"
        default_delphes_card = self.output_dir / "Cards/delphes_card_default.dat"
        resolved_cards = []
        if seed is not None:
            if shower == "on" or shower == "pythia8":
                pythia8_card = None
                for card in cards:
                    if "pythia8" in card:
                        pythia8_card = card

                if pythia8_card is None:
                    pythia8_card = default_pythia8_card

                    with NamedTemporaryFile(
                        delete=False, prefix="pythia8_card_"
                    ) as temp:
                        temp.write(pythia8_card.read_text().encode())
                        temp.write(b"\n! Modified by hep-ml-lab")
                        temp.write(
                            f"\nRandom:setSeed = on\nRandom:seed = {seed}\n".encode()
                        )

                else:
                    with open(pythia8_card, "r") as f:
                        lines = f.readlines()
                        set_seed = False
                        found_seed = False
                        for i, line in enumerate(lines):
                            if line.startswith("Random:setSeed = on"):
                                set_seed = True
                            if line.startswith("Random:seed"):
                                found_seed = True
                                lines[i] = f"Random:seed = {seed}\n"
                                break

                        if not set_seed:
                            lines.append("Random:setSeed = on\n")
                            lines.append(f"Random:seed = {seed}\n")
                        elif not found_seed:
                            lines.append(f"Random:seed = {seed}\n")

                    with NamedTemporaryFile(
                        delete=False, prefix="pythia8_card_"
                    ) as temp:
                        temp.write("".join(lines).encode())

                    resolved_cards.append(temp.name)

            if detector == "on" or detector == "delphes":
                delphes_card = None
                for card in cards:
                    if "delphes" in card:
                        delphes_card = card

                if delphes_card is None:
                    delphes_card = default_delphes_card

                    with NamedTemporaryFile(
                        delete=False, prefix="delphes_card_"
                    ) as temp:
                        temp.write(f"set RandomSeed {seed}\n".encode())
                        temp.write(delphes_card.read_text().encode())

                else:
                    with open(delphes_card, "r") as f:
                        lines = f.readlines()
                        found_seed = False
                        for i, line in enumerate(lines):
                            if line.startswith("set RandomSeed"):
                                found_seed = True
                                lines[i] = f"set RandomSeed {seed}\n"
                                break

                        if not found_seed:
                            lines.insert(0, f"set RandomSeed {seed}\n")

                    with NamedTemporaryFile(
                        delete=False, prefix="delphes_card_"
                    ) as temp:
                        temp.write("".join(lines).encode())

                resolved_cards.append(temp.name)

        if resolved_cards != []:
            commands += "\n".join(resolved_cards) + "\n"
        else:
            commands += "\n".join(cards) + "\n"
        commands += "done\n"

        if dry:
            return commands

        run_log += self.run_command(commands, end_marker=r">$")

        # In the end: Back to Madgraph CLI
        run_log += self.run_command("exit")

        run_name = re.findall(r"survey  (.+) \r\n", run_log)[0]
        run_log_file = self.log_dir / f"{run_name}.log"
        run_log_file = run_log_file.resolve()
        with run_log_file.open("w") as f:
            f.write(run_log)

        if self.verbose > 0:
            if run_log_file.is_relative_to(Path.cwd()):
                print("Run log saved to", run_log_file.relative_to(Path.cwd()))
            else:
                print("Run log saved to", run_log_file)

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

    def summary(self):
        console = Console()

        if self.output_dir.is_relative_to(Path.cwd()):
            output_dir = self.output_dir.relative_to(Path.cwd())
        else:
            output_dir = self.output_dir
        table = Table(title="\n".join(self.processes), caption=f"Output: {output_dir}")

        table.add_column("#", justify="right")
        table.add_column("Name")
        table.add_column("Collider")
        table.add_column("Tag")
        table.add_column("Cross section (pb)", justify="center")
        table.add_column("N events", justify="right")
        table.add_column("Seed", justify="right")

        for i, run in enumerate(self.runs):
            table.add_row(
                f"{i}",
                f"{run.name}[{len(run.sub_runs)}]",
                f"{run.collider}",
                f"{run.tag}",
                f"{run.cross:.3e} +- {run.error:.3e}",
                f"{run.n_events:,}",
                f"{run.seed}",
            )

        console.print(table)

    @classmethod
    def from_output(cls, output_dir: PathLike, executable: PathLike) -> Madgraph5:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            raise FileNotFoundError(f"Output directory {output_dir} does not exist")

        output_dir = output_dir.resolve()
        mg5 = cls(executable, verbose=0)
        mg5.verbose = 1
        mg5.output_dir = output_dir

        return mg5


class Madgraph5Run:
    def __init__(self, output_dir: PathLike, name: str):
        self.output_dir = Path(output_dir)
        self._events_dir = self.output_dir / "Events"
        self._run_dir = self._events_dir / name

        self._info = self._get_info(output_dir, name)
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
        return self._info["n_events"]

    @property
    def sub_runs(self) -> list[Madgraph5Run]:
        return [Madgraph5Run(self.output_dir, i.name) for i in self._subs]

    def events(self, file_format="root"):  # type: ignore
        if file_format == "root":
            root_files = []
            # events = ROOT.TChain("Delphes")  # type: ignore
            if self.sub_runs != []:
                for run in self.sub_runs:
                    for root_file in run.directory.glob("*.root"):
                        root_files.append(f"{root_file.as_posix()}:Delphes")
            else:
                for root_file in self.directory.glob("*.root"):
                    root_files.append(f"{root_file.as_posix()}:Delphes")

            # keys = uproot.open(root_files[0]).keys()
            # keys = [key for key in keys if "fBits" not in key]

            # events = uproot.concatenate(root_files, filter_name=keys)
            events = root_files
        else:
            raise ValueError(f"File format {file_format} not supported yet.")

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

    def _get_info(self, output_dir: PathLike, name: str):
        output_dir = Path(output_dir)
        events_dir = output_dir / "Events"
        run_dir = events_dir / name

        if list(run_dir.glob("*_banner.txt")) != []:
            banner_file = list(run_dir.glob("*_banner.txt"))[0]
        elif list(events_dir.glob(f"{name}_banner.txt")) != []:
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
