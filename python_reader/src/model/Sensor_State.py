from dataclasses import dataclass

@dataclass
class Sensor_State:
    baseline:float = 0.0
    grs:float = 0.0
    dif:float = 0.0
    state:str = "IDLE"