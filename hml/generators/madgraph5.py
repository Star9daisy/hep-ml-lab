from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

import pexpect
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

theme = Theme(
    {
        "sect": "white",  # section
        "info": "blue",  # informatiom
        "done": "green",  # done
        "ques": "yellow",  # question
        "error": "red",  # error
        "warn": "yellow",  # warning
        "hint": "italic yellow",  # hint
        "path": "cyan underline",  # path
        "number": "cyan",  # number
    },
    inherit=False,
)

c = Console(force_jupyter=False, theme=theme)


class Madgraph5:
    def __init__(
        self,
        executable: Path | str | None = None,
        verbose: int = 1,
    ) -> None:
        self.verbose = verbose
        self.executable = executable

    @property
    def executable(self) -> Path:
        if self._executable is None:
            c.print("[error]✘ `executable` has not been set yet.\n")
            c.print(
                "[hint]! You could set it like this:\n"
                "  generator = Madgraph5(executable='path/to/mg5_aMC')"
            )
            raise ValueError

        return self._executable

    @executable.setter
    def executable(self, value: Path | str | None) -> None:
        if value is None:
            self._executable = None

        elif isinstance(value, (Path, str)):
            # Check if the executable is valid
            if (exe_path := shutil.which(str(value))) is None:
                c.print(f"[error]✘ Could not find {value}")
                c.print(
                    "[hint]! The executable is the path you enter in the terminal"
                    " to run Madgraph5. Make sure the path is correct."
                )
                raise FileNotFoundError

            # Make the executable path absolute
            self._executable = Path(exe_path).resolve()

            # Start the child process
            self._child = self._init_child()

        else:
            raise TypeError(f"Expected Path or str, got {type(value).__name__}")

    @property
    def verbose(self) -> int:
        return self._verbose

    @verbose.setter
    def verbose(self, value: int) -> None:
        if isinstance(value, int) and value >= 0:
            self._verbose = value

        else:
            raise ValueError(f"Expected int >= 0, got {value}")

    def _init_child(self) -> pexpect.spawn | None:
        child = pexpect.spawn(self.executable.as_posix())

        child.expect("VERSION [\d\.]+")
        version = re.search(r"[\d\.]+", child.after.decode()).group(0)
        self._version = version
        print(f"Madgraph5_aMC@NLO v{version}") if self.verbose else None

        child.expect("MG5_aMC>$")

        self.clean_pypy()

        return child

    @property
    def child(self) -> pexpect.spawn:
        if not hasattr(self, "_child"):
            c.print("[error]✘ The MadGraph5 child process has not been started yet.\n")
            c.print(
                "[hint]! You could start it by setting `executable` properly:\n"
                "  generator.executable = 'path/to/mg5_aMC'"
            )
            raise AttributeError

        return self._child

    @property
    def home(self) -> Path:
        if self._executable is not None:
            return self.executable.parent.parent

    @property
    def version(self) -> str | None:
        if hasattr(self, "_version"):
            return self._version

    @property
    def output_dir(self) -> Path:
        if not hasattr(self, "_output_dir"):
            c.print("[error]✘ No output directory has been set yet.")
            c.print(
                "[hint]! You could only view the runs after `output`:\n"
                "  generator.output('path/to/output_dir')"
            )
            raise AttributeError

        return self._output_dir

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

    @property
    def processes(self) -> list[str]:
        # 1st case: generate() has been called
        if hasattr(self, "_processes"):
            return self._processes

        # 2nd case: from_output() has been called
        try:
            crossx = self.output_dir / "crossx.html"
            with crossx.open() as f:
                soup = BeautifulSoup(f, "html.parser")
                title_col = soup.find_all("h2")[0].text.strip()
                processes = re.findall(r"^Results in the .+ for (.+)", title_col)[0]
                return processes.split(",")
        except AttributeError:
            c.print("[error]✘ No processes have been generated yet.")
            c.print(
                "[hint]! You could generate some like this:\n"
                "  generator.generate(['p p > t t~'])"
            )
            raise AttributeError

    def clean_pypy(self):
        py_py = Path("py.py")
        if py_py.exists():
            py_py.unlink()

    def import_model(self, model: str | Path) -> None:
        self.child.sendline(f"import model {model}")
        while True:
            self.child.expect("\r\n")

            if "Error" in self.child.before.decode():
                c.print("[error]✘ Error importing model.")
                c.print(self.child.before.decode())
                raise ValueError

            try:
                self.child.expect("MG5_aMC>$", timeout=0.1)
            except pexpect.exceptions.TIMEOUT:
                continue

            for line in self.child.before.decode().split("\r\n"):
                if line.startswith("INFO: Restrict model"):
                    model_dir = Path(line.split(" ")[-3]).absolute().parent

                    try:
                        model_dir_str = f"./{model_dir.relative_to(Path.cwd())}"
                    except ValueError:
                        model_dir_str = model_dir.as_posix()

                    print(f"Model in {model_dir_str}")

            break

        self.clean_pypy()

    def define(self, multi_particles: list[str]):
        for particle in multi_particles:
            self.child.sendline(f"define {particle}")
            self.child.expect("MG5_aMC>$")

            if "error" in self.child.before.decode():
                c.print("[error]✘ Error defining particle.")
                c.print(self.child.before.decode())
                raise ValueError

            for line in self.child.before.decode().splitlines():
                if line.startswith("Defined multiparticle"):
                    print(line)

    def generate(self, processes: list[str]) -> None:
        self._processes = processes
        self.child.sendline(f"generate {processes[0]}")
        self.child.expect("MG5_aMC>$")

        if "error" in self.child.before.decode():
            c.print("[error]✘ Error generating process.")
            c.print(self.child.before.decode())
            raise ValueError

        if len(processes) == 1:
            message = re.search(
                r"Total: \d+ processes with \d+ diagrams",
                self.child.before.decode(),
            ).group(0)
            print(message)

        else:
            for process in processes[1:]:
                self.child.sendline(f"add process {process}")
            self.child.expect("MG5_aMC>$")

            if "error" in self.child.before.decode():
                c.print("[error]✘ Error generating process.")
                c.print(self.child.before.decode())
                raise ValueError
            else:
                message = re.search(
                    r"Total: \d+ processes with \d+ diagrams",
                    self.child.before.decode(),
                ).group(0)
                print(message)

        self.clean_pypy()

    def display_diagrams(self, diagrams_dir="Diagrams", overwrite=True):
        diagrams_dir = Path(diagrams_dir).resolve()
        if diagrams_dir.exists():
            if overwrite:
                shutil.rmtree(diagrams_dir)
            else:
                c.print(f"[error]✘ Directory '{diagrams_dir}' already exists.")
                c.print(
                    "[hint]! If the generator is defined as g = Madgraph5(...),\n"
                    "You could overwrite the existing directory like this:\n"
                    "g.display_diagrams(overwrite=True)"
                )

                raise FileExistsError

        diagrams_dir.mkdir(parents=True)

        self.child.sendline(f"display diagrams {diagrams_dir.as_posix()}")
        self.child.expect("MG5_aMC>$")

        if "error" in self.child.before.decode():
            c.print("[error]✘ Error displaying diagrams.")
            c.print(self.child.before.decode())
            raise ValueError
        else:
            try:
                diagrams_dir_str = f"./{diagrams_dir.relative_to(Path.cwd())}"
            except ValueError:
                diagrams_dir_str = diagrams_dir.as_posix()

            for eps in diagrams_dir.glob("*.eps"):
                subprocess.run(f"ps2pdf {eps} {eps.with_suffix('.pdf')}", shell=True)
                eps.unlink()

            n_diagrams = len(list(diagrams_dir.glob("*.pdf")))
            print(
                f"{n_diagrams} diagrams saved in {diagrams_dir_str}"
            ) if self.verbose else None

        self.clean_pypy()

    def output(self, output_dir=None):
        if output_dir is None:
            self.child.sendline("output")
        else:
            self.child.sendline(f"output {output_dir} -f")
        self.child.expect("MG5_aMC>$")

        if "error" in self.child.before.decode():
            c.print("[error]✘ Error outputing to directory.")
            c.print(self.child.before.decode())
            raise ValueError
        else:
            path = Path(
                re.findall(
                    r"Output to directory (/[\w\.-]+(?:/[\w\.-]+)*)",
                    self.child.before.decode(),
                )[0]
            )
            self.display_diagrams(diagrams_dir=path / "Diagrams")

            self._output_dir = path
            try:
                output_dir_str = f"./{path.relative_to(Path.cwd())}"
            except ValueError:
                output_dir_str = path.as_posix()

            print(f"Output saved in {output_dir_str}") if self.verbose else None

        self.clean_pypy()

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
        config_commands = [
            f"launch -i {self.output_dir}",
            "generate_events" if multi_run == 1 else f"multi_run {multi_run}",
            f"shower={shower}",
            f"detector={detector}",
            f"madspin={madspin}",
            "done",
        ]

        if "iseed" not in settings:
            settings["iseed"] = seed if seed is not None else 0

        config_commands += [f"set {key} {value}" for key, value in settings.items()]
        config_commands += [f"decay {decay}" for decay in decays]

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

        config_commands += resolved_cards if resolved_cards != [] else cards

        if dry:
            return config_commands

        for command in config_commands:
            self.child.sendline(command)
            while True:
                self.child.expect("\r\n")

                try:
                    self.child.expect(">$", timeout=0.1)
                except pexpect.exceptions.TIMEOUT:
                    continue

                if (
                    "not valid option" in self.child.before.decode()
                    or "invalid" in self.child.before.decode()
                ):
                    print(self.child.before.decode().split("\r\n")[0])
                    raise ValueError

                break

        self.child.sendline("done")
        current_run_index = 0
        while True:
            self.child.expect("\r\n")

            if self.child.before.decode().startswith("Generating"):
                run_name = self.child.before.decode().split(" ")[-1]
                print(run_name + "...", end="") if self.verbose else None

            if "Running Survey" in self.child.before.decode():
                print("survey...", end="") if self.verbose else None

            if "Running Pythia8" in self.child.before.decode():
                print("pythia8...", end="") if self.verbose else None

            if "Running Delphes" in self.child.before.decode():
                print("delphes...", end="") if self.verbose else None

            if "storing files of previous run" in self.child.before.decode():
                print("storing...", end="") if self.verbose else None

            # if self.child.before.decode().startswith("INFO: Done"):
            if "INFO: Done" in self.child.before.decode():
                print("✔") if self.verbose else None
                current_run_index += 1

                if current_run_index != multi_run:
                    continue
                else:
                    self.child.expect(">$")
                    break

        self.child.sendline("quit")
        self.child.expect(">$", timeout=0.1)
        self.clean_pypy()

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
    def from_output(
        cls,
        output_dir: Path | str,
        executable: Path | str | None = None,
    ) -> Madgraph5:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            raise FileNotFoundError(f"Output directory {output_dir} does not exist")

        output_dir = output_dir.resolve()
        mg5 = cls(executable, verbose=0)
        mg5.verbose = 1
        mg5._output_dir = output_dir

        return mg5


class Madgraph5Run:
    def __init__(self, output_dir: str | Path, name: str):
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

    def _get_info(self, output_dir: str | Path, name: str):
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
