from __future__ import annotations

import os
import pty
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Union

import ROOT

_ = ROOT.gSystem.Load("libDelphes")  # type: ignore


PathLike = Union[str, Path]


class Madgraph5:
    def __init__(
        self,
        executable: PathLike,
        processes: list[str],
        model: PathLike = "sm",
        definitions: dict[str, Any] | None = None,
        output: PathLike = "madevent",
    ) -> None:
        # Check if the executable exists
        if (_executable := shutil.which(executable)) is not None:
            self.executable = Path(_executable).resolve()
            self.mg5_dir = self.executable.parent.parent
        else:
            raise EnvironmentError(f"{executable} does not exist.")

        self.model = model
        self.definitions = definitions
        self.processes = processes

        self.output = Path(output).resolve()
        if self.output.exists():
            raise FileExistsError(
                f"{self.output.relative_to(Path.cwd())} already exists."
            )

        # Create commands and save them in a temporary file
        self.commands = {
            "pre": [
                *[f"import {model}"],
                *[f"generate {self.processes[0]}"],
                *[f"add process {p}" for p in self.processes[1:]],
                *[f"output {self.output}"],
            ],
        }
        command_file = self._cmds_to_file(self.commands["pre"])

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
        _, stderr = process.communicate()
        if stderr:
            raise RuntimeError(stderr.decode())

    def launch(
        self,
        shower: str = "off",
        detector: str = "off",
        settings: dict[str, Any] | None = None,
        cards: list[Path] | None = None,
        multi_run: int = 1,
    ):
        if shower not in ["off", "pythia8"]:
            raise ValueError(f"Unknown shower tool {shower}")
        if detector not in ["off", "delphes"]:
            raise ValueError(f"Unknown detector tool {detector}")

        self.shower = shower
        self.detector = detector
        self.settings = settings if settings is not None else {}

        if cards is None:
            self.cards = []
        else:
            self.cards = [card.resolve() for card in cards]

        # -------------------------------------------------------------------- #
        commands = [
            *[f"launch -i {self.output}"],
            *[f"multi_run {multi_run}"],
            *[f"shower={shower}"],
            *[f"detector={detector}"],
            *[f"set {k} {v}" for k, v in self.settings.items()],
            *[f"{card}" for card in self.cards],
        ]
        command_file = self._cmds_to_file(commands)

        # -------------------------------------------------------------------- #
        (self.output / "Logs").mkdir()
        n_runs = len(list((self.output / "Events").glob("*banner.txt"))) + 1
        log_file = self.output / "Logs" / f"run_{n_runs:02d}.log"

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
                        print(status)
                        if idx == storing_files_idx:
                            current_run += 1
                            if current_run > multi_run:
                                last_known_status = idx
                            else:
                                last_known_status = -1
                        else:
                            last_known_status = idx

            # Check if process is still running
            if process.poll() is not None:  # Process has finished
                print("Done")
                os.close(child)
                break

        # -------------------------------------------------------------------- #
        _, stderr = process.communicate()
        if stderr:
            raise RuntimeError(stderr.decode())

    def _cmds_to_file(self, cmds: list[str]) -> str:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write("\n".join(cmds))
            temp_file_path = temp_file.name
        return temp_file_path
