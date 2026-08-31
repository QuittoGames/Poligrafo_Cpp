import re
from typing import Optional

import serial
from serial.tools import list_ports

from src.api.utils.logger import Logger
from src.api.model.Sensor_State import Sensor_State


# VID/PID pairs commonly associated with Arduino Uno boards and their clones.
# Used as a fallback when the port description does not contain "Arduino"/"Uno".
_ARDUINO_VID_PIDS: frozenset = frozenset(
    {
        (0x2341, 0x0043),  # Arduino Uno R3 (ATmega16U2)
        (0x2341, 0x0001),  # Arduino Uno (older firmware)
        (0x1A86, 0x7523),  # CH340/CH341 (very common clones)
        (0x0403, 0x6001),  # FTDI FT232R
        (0x10C4, 0xEA60),  # Silicon Labs CP210x
    }
)

# Tag emitted by src/main.cpp loop() to mark a real data frame (vs setup() preamble).
_DATA_TAG = "[DATA]"

# State strings written by State::stateToString() in src/enum/State.hpp.
_VALID_STATES: frozenset = frozenset(
    {
        "NONE",
        "ESTAVEL",
        "VARIACAO_LEVE",
        "PICO_DETECTADO",
        "NOT_CONNECTED",
    }
)


class ReaderService:
    """Reads serial frames emitted by the Arduino firmware (see src/main.cpp).

    Wire format (one line, newline-terminated):
        ---------------------------------------[DATA] GSR=<float> | BASELINE=<float> | DIFF=<float> | STATE=<STATE>
    """

    def __init__(self, port: Optional[str] = None, baud: int = 9600) -> None:
        self._port = port or self._detect_arduino_port()
        Logger.logger.info(f"[SERIAL] Opening {self._port} @ {baud} baud")
        try:
            self.ser = serial.Serial(self._port, baud, timeout=1)
        except serial.SerialException as exc:
            raise RuntimeError(
                f"Failed to open serial port '{self._port}': {exc}"
            ) from exc

    @staticmethod
    def _detect_arduino_port() -> str:
        """Find the Arduino Uno's serial port across Windows, Linux and macOS.

        Strategy:
            1. Description/manufacturer/product contains 'arduino' or 'uno'.
            2. Known VID/PID of common Arduino/clone USB-serial chips.
            3. Only one port present -> use it.
            4. Otherwise raise with a list of available ports.
        """
        candidates = list_ports.comports()
        if not candidates:
            raise RuntimeError("Nenhuma porta serial encontrada no sistema.")

        for port_info in candidates:
            blob = " ".join(
                filter(
                    None,
                    (
                        port_info.description,
                        port_info.manufacturer,
                        port_info.product,
                    ),
                )
            ).lower()
            if "arduino" in blob or "uno" in blob:
                return port_info.device

        for port_info in candidates:
            if (
                port_info.vid is not None
                and (port_info.vid, port_info.pid) in _ARDUINO_VID_PIDS
            ):
                return port_info.device

        if len(candidates) == 1:
            return candidates[0].device

        available = ", ".join(
            f"{p.device} ({p.description or 'sem descricao'})" for p in candidates
        )
        raise RuntimeError(
            f"Arduino Uno nao detectado. Portas disponiveis: {available}"
        )

    def read(self) -> Optional[Sensor_State]:
        """Block-read the next frame from the serial port.

        Returns a populated Sensor_State on a [DATA] line, or None on
        timeout/empty/preamble lines. Raises RuntimeError on serial errors.
        """
        try:
            raw = self.ser.readline().decode(errors="ignore").strip()
        except serial.SerialException as exc:
            Logger.logger.error(f"[SERIAL] readline failed: {exc}")
            raise RuntimeError(f"Serial read failure on {self._port}: {exc}") from exc

        if not raw or _DATA_TAG not in raw:
            return None

        try:
            fields = self._parse_data_line(raw)
        except ValueError as exc:
            Logger.logger.warning(f"[SERIAL] malformed data line: {raw!r} ({exc})")
            return None

        return Sensor_State(
            gsr=fields["GSR"],
            baseline=fields["BASELINE"],
            diff=fields["DIFF"],
            state=fields["STATE"],
        )

    @staticmethod
    def _parse_data_line(line: str) -> dict:
        """Parse '[DATA] GSR=x | BASELINE=y | DIFF=z | STATE=s' into a dict.

        Raises ValueError if any required field is missing or malformed.
        """
        body = line.split(_DATA_TAG, 1)[1].strip()
        fields: dict = {}
        for chunk in body.split("|"):
            chunk = chunk.strip()
            if not chunk:
                continue
            key, sep, value = chunk.partition("=")
            if not sep:
                continue
            key = key.strip()
            value = value.strip()
            if key in ("GSR", "BASELINE", "DIFF"):
                try:
                    fields[key] = float(value)
                except ValueError:
                    raise ValueError(f"{key!r} is not a number: {value!r}")
            elif key == "STATE":
                fields[key] = value

        missing = {"GSR", "BASELINE", "DIFF", "STATE"} - fields.keys()
        if missing:
            raise ValueError(f"missing fields: {sorted(missing)}")

        if fields["STATE"] not in _VALID_STATES:
            Logger.logger.warning(
                f"[SERIAL] unknown STATE {fields['STATE']!r} (expected one of {sorted(_VALID_STATES)})"
            )

        return fields
