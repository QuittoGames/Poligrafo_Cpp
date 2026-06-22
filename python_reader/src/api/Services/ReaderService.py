import serial
import re
from src.api.utils.logger import Logger
from src.api.model.Sensor_State import Sensor_State

class ReaderService:
    def __init__(self, port="COM3", baud=9600):
        self.ser = serial.Serial(port, baud, timeout=1)

    def read(self) -> Sensor_State:
        try:
            raw = self.ser.readline().decode(errors="ignore").strip()

            if not raw:
                return None

            state = Sensor_State()

            # GSR
            gsr = re.search(r"GSR:\s*([0-9.]+)", raw)
            if gsr:
                state.gsr = float(gsr.group(1))

            # BASELINE
            baseline = re.search(r"BASELINE:\s*([0-9.]+)", raw)
            if baseline:
                state.baseline = float(baseline.group(1))

            # DIFF
            diff = re.search(r"DIFF:\s*([0-9.]+)", raw)
            if diff:
                state.diff = float(diff.group(1))

            # STATE (texto)
            if "ESTAVEL" in raw:
                state.state = "ESTAVEL"
            elif "ALERT" in raw or "PICO" in raw:
                state.state = "ALERT"
            elif "SEM CONTATO" in raw:
                state.state = "NO_CONTACT"

            return state
        except RuntimeError as RE:
            Logger.logger.warn("Error in Reader.py")
            raise RE