import asyncio
from src.api.Services.ReaderService import ReaderService
from src.api.data.core.deps.deps import get_data
import random
from src.api.utils.logger import Logger

# Backoff bounds (seconds) for the reader reconnection loop.
_INITIAL_BACKOFF_S: float = 1.0
_MAX_BACKOFF_S: float = 30.0
_BUFFER_LIMIT: int = 100
_READ_INTERVAL_S: float = 1.0


class Worker:
    @staticmethod
    async def sensor_worker_test():
        Logger.logger.info("Worker SIMULADO ativo")

        gsr = 0.5

        while True:
            try:
                gsr += random.uniform(-0.03, 0.03)
                gsr = max(0, min(1, gsr))

                if random.random() < 0.1:
                    gsr += random.uniform(0.2, 0.5)

                gsr = max(0, min(1, gsr))

                fake_value = {
                    "gsr": gsr,
                    "baseline": 0.5,
                    "diff": abs(gsr - 0.5),
                    "state": "TEST",
                }

                get_data().latest_state.append(fake_value)

                if len(get_data().latest_state) > _BUFFER_LIMIT:
                    get_data().latest_state.pop(0)

                Logger.logger.debug(f"GSR={gsr:.3f}")

                await asyncio.sleep(_READ_INTERVAL_S)

            except Exception as e:
                Logger.logger.error(f"Worker error: {e}")

    @staticmethod
    async def sensor_worker():
        """Read frames from the Arduino forever, reconnecting on failure.

        The reader (port handle + pyserial object) is recreated on every
        RuntimeError so that a transient disconnection, unplug/replug, or
        port-busy error recovers automatically. Backoff is exponential with
        a cap; it resets after a successful read.
        """
        reader: ReaderService | None = None
        backoff = _INITIAL_BACKOFF_S

        while True:
            try:
                if reader is None:
                    reader = ReaderService()

                value = reader.read()

                if value is not None:
                    get_data().latest_state.append(value)
                    if len(get_data().latest_state) > _BUFFER_LIMIT:
                        get_data().latest_state.pop(0)
                    backoff = _INITIAL_BACKOFF_S  # success — reset backoff

                await asyncio.sleep(_READ_INTERVAL_S)

            except RuntimeError as exc:
                Logger.logger.warning(
                    f"[SERIAL] worker RuntimeError: {exc}. "
                    f"Reconnecting in {backoff:.1f}s..."
                )
                reader = None  # force a fresh ReaderService next iteration
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, _MAX_BACKOFF_S)

            except Exception as exc:
                Logger.logger.error(f"[WORKER] unexpected error: {exc}")
                await asyncio.sleep(_READ_INTERVAL_S)
