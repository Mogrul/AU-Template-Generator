from pathlib import Path
from dataclasses import dataclass

@dataclass
class Author:
    name: str
    url: str

@dataclass
class Mod:
    name: str

@dataclass
class Side:
    name: str
    type: str
    description: str
    flag_file: Path