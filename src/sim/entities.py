import random
from dataclasses import dataclass

@dataclass
class Vehicle:
    id: int
    lane: str
    position: float = 0.0
    speed: float = 10.0
    waiting_time: float = 0.0
    broken: bool = False
    is_emergency: bool = False

@dataclass
class Pedestrian:
    id: int
    cross_pos: float = 0.0
    speed: float = 1.2
    waiting_time: float = 0.0
