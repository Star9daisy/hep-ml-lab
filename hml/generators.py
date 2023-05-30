from __future__ import annotations
import tempfile
import os
from typing import Any
from pathlib import Path


class Madgraph5:
    def __init__(
        self,
        processes: str | list[str],
        output_dir: str | None = None,
        model: str = "sm",
        definitions: dict[str, str] | None = None,
        shower: str | None = None,
        detector: str | None = None,
        settings: dict[str, Any] | None = None,
        cards: list[str] | None = None,
    ) -> None:
        self.processes = processes
        self.output_dir = output_dir
        self.model = model
        self.definitions = definitions
        self.shower = shower
        self.detector = detector
        self.settings = settings
        self.cards = cards
        self.cmds = self._params_to_cmds()

    def launch(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write("\n".join(self.cmds))
            temp_file_path = temp_file.name

        os.system(f"mg5_aMC {temp_file_path}")
        os.system("rm py.py")

    def _params_to_cmds(self) -> list[str]:
        # Model
        cmds = [f"import model {self.model}"]

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
        if self.output_dir:
            cmds += [f"output {Path(self.output_dir).absolute()}"]
        else:
            cmds += ["output"]

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
            cmds += [f"    {Path(c).absolute()}" for c in self.cards]

        return cmds
