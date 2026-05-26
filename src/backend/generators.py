from pathlib import Path

from .models.templates import CONFIG_TEMPLATE, SIDE_TEMPLATE
from .models.params import Mod, Author, Side
from .models.rebel import (
    Vehicle, Breacher, Rebel, StartingEquipment,
    UnitEquipment, Vehicles
)

def _create_file(output: Path, content: str) -> None:
    output.parent.mkdir(parents = True, exist_ok = True)
    output.write_text(content)

def generate_config(
        output: Path,
        mod: Mod,
        author: Author,
        sides: list[Side]
):
    sides_str = ""
    for side in sides:
        sides_str += SIDE_TEMPLATE.substitute(
            mod_name = mod.name,
            side = side.type,
            side_name = side.name,
            side_description = side.description,
            side_flag = side.flag_file,
            side_path = "placeholder",
            side_file_name = "placeholder"
        )
    
    _create_file(output, CONFIG_TEMPLATE.substitute(
        mod_name = mod.name,
        author_name = author.name,
        author_url = author.url,
        side_templates = sides_str
    ))

def generate_rebel_template(
        output: Path,
        rebel: Rebel
        #starting_equipment: StartingEquipment,
        #unit_equipment: UnitEquipment,
        #vehicles: Vehicles
):
    to_template = "call _fnc_saveToTemplate;"
    content_str = ""
    
    content_str += "// SIDE INFORMATION\n"
    content_str += f'["name", "{rebel.name}"] {to_template}\n'
    content_str += f'["flag", "{rebel.flag_name}"] {to_template}\n'
    content_str += f'["flagTexture", "{rebel.flag_texture}"] {to_template}\n'
    content_str += f'["flagMarkerType", "{rebel.marker_type}"] {to_template}\n\n'
    
    content_str += "// IDENTITY\n"
    content_str += f'["faces", {str(rebel.faces)}] {to_template}\n'
    content_str += f'["voices", {str(rebel.voices)}] {to_template}\n'
    
    _create_file(output, content_str)
    