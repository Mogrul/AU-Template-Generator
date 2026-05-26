from dataclasses import dataclass, field

from .params import Side

@dataclass
class Vehicle:
    name: str
    cost: int = 100
    
    def to_attribute(self) -> str:
        return f'["{self.name}", ["rebCost", {self.cost}]]'

@dataclass
class Breacher:
    name: str
    amount: int = 1
    
    def to_pair(self) -> str:
        return f'"{self.name}", {self.amount}'

@dataclass
class Rebel:
    name: str
    flag_name: str
    flag_texture: str
    marker_type: str
    faces: list[str] = field(default_factory = list)
    voices: list[str] = field(default_factory = list)

@dataclass
class StartingEquipment:
    guns: list[str] = field(default_factory = list)
    ammo: list[str] = field(default_factory = list)
    uniforms: list[str] = field(default_factory = list)
    headgear: list[str] = field(default_factory = list)
    vests: list[str] = field(default_factory = list)
    facewear: list[str] = field(default_factory = list)
    backpacks: list[str] = field(default_factory = list)

@dataclass
class UnitEquipment:
    uniforms: list[str] = field(default_factory = list)
    headgear: list[str] = field(default_factory = list)
    facewear: list[str] = field(default_factory = list)

@dataclass
class Vehicles:
    civ: CivVehicles
    static: StaticVehicles
    placeables: PlaceableVehicles
    breachers: BreachingVehicles
    
    basic: list[Vehicle] = field(default_factory = list)
    unarmed: list[Vehicle] = field(default_factory = list)
    armed: list[Vehicle] = field(default_factory = list)
    truck: list[Vehicle] = field(default_factory = list)
    anti_tank: list[Vehicle] = field(default_factory = list)
    anti_air: list[Vehicle] = field(default_factory = list)
    boat: list[Vehicle] = field(default_factory = list)
    plane: list[Vehicle] = field(default_factory = list)
    medical: list[Vehicle] = field(default_factory = list)

@dataclass
class CivVehicles:
    basic: list[Vehicle] = field(default_factory = list)
    truck: list[Vehicle] = field(default_factory = list)
    heli: list[Vehicle] = field(default_factory = list)
    boat: list[Vehicle] = field(default_factory = list)
    plane: list[Vehicle] = field(default_factory = list)
    supply: list[Vehicle] = field(default_factory = list)

@dataclass
class StaticVehicles:
    mortar_mag_he: str
    mortar_mag_smoke: str
    
    machine_gun: list[Vehicle] = field(default_factory = list)
    anti_tank: list[Vehicle] = field(default_factory = list)
    anti_air: list[Vehicle] = field(default_factory = list)
    mortar: list[Vehicle] = field(default_factory = list)

@dataclass
class PlaceableVehicles:
    anti_tank: list[Vehicle] = field(default_factory = list)
    anti_personnel: list[Vehicle] = field(default_factory = list)

@dataclass
class BreachingVehicles:
    apc: list[Breacher] = field(default_factory = list)
    tank: list[Breacher] = field(default_factory = list)