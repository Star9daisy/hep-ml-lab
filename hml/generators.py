from __future__ import annotations
import tempfile
import os
from typing import Any
from pathlib import Path
import ROOT

ROOT.gSystem.Load("libDelphes")


class Madgraph5:
    """Simple API for Madgraph5

    Parameters
    ----------
    processes : str | list[str]
        Processes to generate. Equal to the `generate` and `add process` commands in Madgraph5.
    output_dir : str | None, optional
        Output directory for the generated files. Equal to the `output` command in Madgraph5.
    model : str, optional
        Model to use. Equal to the `import model` command in Madgraph5.
    definitions : dict[str, str] | None, optional
        Definitions to use. Equal to the `define` command in Madgraph5.
    shower : str | None, optional
        Parton shower tool. Equal to the `shower` option in Madgraph5.
    detector : str | None, optional
        Detector simulation tool. Equal to the `detector` option in Madgraph5.
    settings : dict[str, Any] | None, optional
        Phase space and parameter settings. Equal to the `set` command in Madgraph5.
    cards : list[str] | None, optional
        Shower and detector cards to use. Equal to enter the card paths in Madgraph5.

    Properties
    ----------
    All parameters are stored as properties.
    cmds : list[str]
        Commands to be executed by Madgraph5.
    runs: list[MG5Run]
        List of MG5Run objects containing necessary information of each run.

    Methods
    -------
    launch(): None
        Launch Madgraph5 with the stored commands.
    """

    def __init__(
        self,
        processes: str | list[str],
        output_dir: str | Path | None = None,
        model: str = "sm",
        definitions: dict[str, str] | None = None,
        shower: str | None = None,
        detector: str | None = None,
        settings: dict[str, Any] | None = None,
        cards: list[str | Path] | None = None,
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
        # Save cmds to a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write("\n".join(self.cmds))
            temp_file_path = temp_file.name

        # Launch Madgraph5
        os.system(f"mg5_aMC {temp_file_path}")
        os.system("rm py.py")

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


class MG5Run:
    """A class to store information of a MG5 run."""

    def __init__(self, run_dir: str | Path) -> None:
        self.run_dir = Path(run_dir)
        self._load()

    def _load(self) -> None:
        # Find banner file
        banner_file = list(self.run_dir.glob("*banner.txt"))[0]
        with open(banner_file, "r") as f:
            contents = f.readlines()

        # Seach for run tag
        self.run_tag = "tag_1"
        for line in contents:
            if "name of the run" in line:
                self.run_tag = line.split("!")[0].split("=")[0].strip()
                break

        # Search for cross section
        self.cross_section = 0
        for line in contents[::-1]:
            if line.startswith("#  Integrated weight (pb)"):
                self.cross_section = float(line.split()[-1])
                break

        # Find event file and get events
        self.event_file = list(self.run_dir.glob("*.root"))[0]
        self.event_file = ROOT.TFile(str(self.event_file))
        self.events = self.event_file.Get("Delphes")
