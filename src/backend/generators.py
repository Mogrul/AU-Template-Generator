from pathlib import Path
from dataclasses import fields, is_dataclass

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
        rebel: Rebel,
        starting_equipment: StartingEquipment,
        unit_equipment: UnitEquipment,
        vehicles: Vehicles
):
    def sqf_array(values: list[str]) -> str:
        return "[" + ", ".join(f'"{v}"' for v in values) + "]"
    
    def build_side_information(rebel: Rebel):
        return (
            "// SIDE INFORMATION\n"
            f'["name", "{rebel.name}"] call _fnc_saveToTemplate;\n'
            f'["flag", "{rebel.flag_name}"] call _fnc_saveToTemplate;\n'
            f'["flagTexture", "{rebel.flag_texture}"] call _fnc_saveToTemplate;\n'
            f'["flagMarkerType", "{rebel.marker_type}"] call _fnc_saveToTemplate;\n'
            "\n"
        )
    
    def build_identity(rebel: Rebel):
        return (
            "// IDENTITY\n"
            f'["faces", {sqf_array(rebel.faces)}] call _fnc_saveToTemplate;\n'
            f'["voices", {sqf_array(rebel.voices)}] call _fnc_saveToTemplate;\n'
            "\n"
        )
    
    def build_vehicles(vehicles: Vehicles):
        mapping = {
            "vehiclesBasic": vehicles.basic,
            "vehiclesLightUnarmed": vehicles.unarmed,
            "vehiclesLightArmed": vehicles.armed,
            "vehiclesTruck": vehicles.truck,
            "vehiclesAT": vehicles.anti_tank,
            "vehiclesAA": vehicles.anti_air,
            "vehiclesBoat": vehicles.boat,
            "vehiclesPlane": vehicles.plane,
            "vehiclesMedical": vehicles.medical,
            "vehiclesCivCar": vehicles.civ.basic,
            "vehiclesCivTruck": vehicles.civ.truck,
            "vehiclesCivHeli": vehicles.civ.heli,
            "vehiclesCivBoat": vehicles.civ.boat,
            "vehiclesCivPlane": vehicles.civ.plane,
            "vehiclesCivSupply": vehicles.civ.supply,
            "staticMGs": vehicles.static.machine_gun,
            "staticAT": vehicles.static.anti_tank,
            "staticAA": vehicles.static.anti_air,
            "staticMortars": vehicles.static.mortar,
            "minesAT": vehicles.placeables.anti_tank,
            "minesAPERS": vehicles.placeables.anti_personnel
        }
        
        def names(vehicles_list: list[Vehicle]) -> str:
            return sqf_array(v.name for v in vehicles_list)
    
        content_str = "".join(
            f'["{key}", {names(value)}] call _fnc_saveToTemplate;\n'
            for key, value in mapping.items()
        )
        
        content_str += f'["staticMortarMagHE", "{vehicles.static.mortar_mag_he}"] call _fnc_saveToTemplate;\n'
        content_str += f'["staticMortarMagSmoke", "{vehicles.static.mortar_mag_smoke}"] call _fnc_saveToTemplate;\n'
        
        def breacher_array(breachers: list[Breacher]) -> str:
            return ", ".join(f'[{b.to_pair()}]' for b in breachers)
        
        content_str += (
            f'["breachingExplosivesAPC", [{breacher_array(vehicles.breachers.apc)}]] call _fnc_saveToTemplate;\n'
        )
        content_str += (
            f'["breachingExplosivesTank", [{breacher_array(vehicles.breachers.tank)}]] call _fnc_saveToTemplate;\n'
        )
        
        return (
            "// VEHICLES\n"
            + content_str
            + "\n"
        )

    def build_vehicle_attributes(vehicles: Vehicles):
        def to_attribute(obj) -> str:
            if isinstance(obj, Vehicle):
                return obj.to_attribute()

            if isinstance(obj, Breacher):
                return None

            raise TypeError(f"Unsupported type: {type(obj)}")
        
        def extract_vehicle_attributes(obj) -> list[str]:
            result = []
            
            for f in fields(obj):
                value = getattr(obj, f.name)
                
                if isinstance(value, list):
                    for item in value:
                        result.append(to_attribute(item))

                elif is_dataclass(value):
                    for sub_f in fields(value):
                        sub_value = getattr(value, sub_f.name)

                        if isinstance(sub_value, list):
                            for item in sub_value:
                                attr = to_attribute(item)
                                if attr:
                                    result.append(attr)

            return result
        
        attrs = extract_vehicle_attributes(vehicles)

        return (
            "// VEHICLE ATTRIBUTES\n"
            f'["attributesVehicles", [{', '.join(attrs)}]] call _fnc_saveToTemplate;\n'
            "\n"
        )
            
    def build_starting_equipment(starting_equipment: StartingEquipment):
        return (
            "// STARTING EQUIPMENT\n"
            f"_equipmentGun = {sqf_array(starting_equipment.guns)};\n"
            f"_equipmentAmmo = {sqf_array(starting_equipment.ammo)};\n"
            f"_equipmentUniform = {sqf_array(starting_equipment.uniforms)};\n"
            f"_equipmentHeadgear = {sqf_array(starting_equipment.headgear)};\n"
            f"_equipmentVest = {sqf_array(starting_equipment.vests)};\n"
            f"_equipmentFacewear = {sqf_array(starting_equipment.facewear)};\n"
            f"_equipmentBackpack = {sqf_array(starting_equipment.backpacks)};\n"
            "\n"
            '["initialRebelEquipment", \n'
            "   _equipmentGun\n"
            "   + _equipmentAmmo\n"
            "   + _equipmentUniform\n"
            "   + _equipmentHeadgear\n"
            "   + _equipmentVest\n"
            "   + _equipmentFacewear\n"
            "   + _equipmentBackpack\n"
            "] _fnc_saveToTemplate;\n"
            "\n"
        )
    
    def build_unit_equipment(unit_equipment: UnitEquipment):
        return (
            "// UNIT EQUIPMENT\n"
            f"_equipmentUnitUniform = {sqf_array(unit_equipment.uniforms)};\n"
            f"_equipmentUnitHeadgear = {sqf_array(unit_equipment.headgear)};\n"
            f"_equipmentUnitFacewear = {sqf_array(unit_equipment.facewear)};\n"
            "\n"
            '["uniforms", _equipmentUnitUniform] call _fnc_saveToTemplate;\n'
            '["headgear", _equipmentUnitHeadgear] call _fnc_saveToTemplate;\n'
            "\n"
        )
    
    def build_loadout():
        return (
            "// LOADOUT\n"
            "private _loadout = call _fnc_createLoadoutData;\n"
            "\n"
            '_loadout set ["maps", ["ItemMap"]];\n'
            '_loadout set ["watches", ["ItemWatch"]];\n'
            '_loadout set ["compasses", ["ItemCompass"]];\n'
            '_loadout set ["item_medical_basic", ["BASIC"]];\n'
            '_loadout set ["item_medical_standard", ["STANDARD"]];\n'
            '_loadout set ["item_medical_medic", ["MEDIC"]];\n'
            '_loadout set ["items_miscEssentials", [] call A3A_fnc_itemset_miscEssentials];\n'
            '_loadout set ["uniforms", _equipmentUnitUniforms];\n'
            '_loadout set ["facewear", _equipmentUnitFacewear];\n'
            "\n"
        )
    
    def build_unit_types():
        return (
            "// UNIT TYPES\n"
            "private _squadLeader = {\n"
            '   ["uniforms"] call _fnc_setUniform;\n'
            '   ["facewear"] call _fnc_setFacewear;\n'
            '   ["maps"] call _fnc_addMap;\n'
            '   ["watches"] call _fnc_addWatch;\n'
            '   ["compasses"] call _fnc_addCompass;\n'
            '   ["binoculars"] call _fnc_addBinoculars;\n'
            "};\n"
            "\n"
            "private _rifleman = {\n"
            '   ["uniforms"] call _fnc_setUniform;\n'
            '   ["facewear"] call _fnc_setFacewear;\n'
            '   ["maps"] call _fnc_addMap;\n'
            '   ["watches"] call _fnc_addWatch;\n'
            '   ["compasses"] call _fnc_addCompass;\n'
            "};\n"
            "\n"
        )
    
    
    def build_unit():
        mapping = {
            "_squadLeader": ["Petros", "SquadLeader"],
            "_rifleman": [
                "Rifleman",
                "staticCrew",
                "Medic",
                "Engineer",
                "ExplosivesExpert",
                "Grenadier",
                "LAT",
                "AT",
                "AA",
                "MachineGunner",
                "Marksman",
                "Sniper",
                "Unarmed"
            ]
        }
        
        lines = []
        for group_var, names in mapping.items():
            for name in names:
                match name:
                    case "Medic":
                        lines.append(f'    ["{name}", {group_var}, [["medic", true]]]')
                    case "Engineer":
                        lines.append(f'    ["{name}", {group_var}, [["engineer", true]]]')
                    case "ExplosivesExpert":
                        lines.append(f'    ["{name}", {group_var}, [["explosivesExpert", true]]]')
                    case _:
                        lines.append(f'    ["{name}", {group_var}]')

        return (
            "// UNIT\n"
            "private _unit = [\n"
            + ",\n".join(lines)
            + "\n"
            + "];\n"
            + "\n"
            + (
                '["militia", _unit, _loadout] call _fnc_generateAndSaveUnitsToTemplate;'
            )
        )

    content_str = ""
    content_str += build_side_information(rebel)
    content_str += build_identity(rebel)
    content_str += build_vehicles(vehicles)
    content_str += build_vehicle_attributes(vehicles)
    content_str += build_starting_equipment(starting_equipment)
    content_str += build_unit_equipment(unit_equipment)
    content_str += build_loadout()
    content_str += build_unit_types()
    content_str += build_unit()
    
    _create_file(output, content_str)
    