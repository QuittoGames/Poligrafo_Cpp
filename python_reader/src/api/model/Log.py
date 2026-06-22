from dataclasses import dataclass,field
from datetime import date
from src.api.model.Sensor_State import Sensor_State

@dataclass
class Log:
    data_state: list[Sensor_State] = field(default_factory=list)
    date: date = field(default_factory=date.today)

    def _avg_gsr(self) -> float:
        values = [i.gsr for i in self.data_state if i.gsr is not None]
        return sum(values) / len(values) if values else 0
    
    def serialize_toJSON(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "avg": self._avg_gsr(),
            "states": [
                {
                    "gsr": s.gsr,
                    "baseline": s.baseline,
                    "diff": s.diff,
                    "state": s.state
                }
                for s in self.data_state
            ]
        }
    
    def serialize_toLog(self) -> str:
        return {
            "date": self.date.isoformat(),
            "avg": self._avg_gsr(),
            "states": [
                {
                    "gsr": s.gsr,
                    "baseline": s.baseline,
                    "diff": s.diff,
                    "state": s.state
                }
                for s in self.data_state
            ]
        }