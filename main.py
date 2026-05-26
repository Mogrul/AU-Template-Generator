from pathlib import Path

from src.backend.generators import generate_config, generate_rebel_template
from src.backend.models.params import Author, Mod, Side
from src.backend.models.rebel import *

if __name__ == "__main__":
    generate_config(
        output = Path("out/addons/config.cpp"),
        mod = Mod(
            name = "ModName"
        ),
        author = Author(
            name = "Mogrul",
            url = "https://mogrul.com"
        ),
        sides = [
            Side(
                name = "Rhodesia",
                type = "Reb",
                description = "Description",
                flag_file = "flag.paa"
            ),
            Side(
                name = "Rhodesia",
                type = "Reb",
                description = "Description",
                flag_file = "flag.paa"
            ),
            Side(
                name = "Rhodesia",
                type = "Reb",
                description = "Description",
                flag_file = "flag.paa"
            )
        ]
    )
    
    generate_rebel_template(
        output = Path("out/addons/Templates/reb_template.sqf"),
        rebel = Rebel(
            name = "Rhodesia",
            flag_name = "Rhodesia_Flag_R",
            flag_texture = "rhodesia_flag.paa",
            marker_type = "Rhodesia_Marker_R",
            faces = ["Karl", "Mike"],
            voices = ["KarlVoice", "MikeVoice"]
        ),
        starting_equipment = StartingEquipment(),
        unit_equipment = UnitEquipment(),
        vehicles = Vehicles(
            civ = CivVehicles(),
            static = StaticVehicles(
                mortar_mag_he = "mag",
                mortar_mag_smoke = "smoke"
            ),
            placeables = PlaceableVehicles(),
            breachers = BreachingVehicles(
                apc = [Breacher("test", 0), Breacher("test2", 20)],
                tank = [Breacher("breacher", 40), Breacher("tttt", 20)]
            )
        )
    )