from dataclasses import dataclass

@dataclass
class SideParams:
    side: str
    name: str
    description: str
    flag_texture: str
    base_path: str
    file_no_ext: str

@dataclass
class Params:
    mod_name: str
    author_name: str
    author_url: str = None