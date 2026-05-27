from dataclasses import dataclass

@dataclass
class Border:
    colour: str
    size: int

@dataclass
class Background:
    colour: str

class AppParams:
    border = Border("#2a2b2c", 1)
    
    bar_background = Background("#191a1b")
    body_background = Background("#121314")