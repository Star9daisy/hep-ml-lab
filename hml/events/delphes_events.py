from ROOT import TFile
from ROOT import TTree
from ROOT import gSystem

from hml.types import Path
from hml.types import PathLike

gSystem.Load("libDelphes")


class DelphesEvents:
    def __init__(self, filepath: PathLike):
        self.filepath = Path(filepath)
        if self.filepath.suffix != ".root":
            raise ValueError(f"Expected .root file, got '{self.filepath.suffix}'")
        if not self.filepath.exists():
            raise FileNotFoundError(f"File {self.filepath} does not exist")

        self.file = TFile(self.filepath.as_posix())
        self.tree = self.file.Get("Delphes")

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __getitem__(self, index: int) -> TTree:
        self.tree.GetEntry(index)
        return self.tree

    def __len__(self) -> int:
        return self.tree.GetEntries()
