import asyncio
from src.api.Services.ReaderService import ReaderService
from src.api.data.core.deps.deps import get_data
import random
from src.api.utils.logger import Logger

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
                    "state": "TEST"
                }

                get_data().latest_state.append(fake_value)

                if len(get_data().latest_state) > 100:
                    get_data().latest_state.pop(0)

                Logger.logger.debug(f"GSR={gsr:.3f}")

                await asyncio.sleep(1)

            except Exception as e:
                Logger.logger.error(f"Worker error: {e}")

    async def sensor_worker():
        try:
            reader = ReaderService()
            while True:
                value = reader.read()
                if value:
                    get_data().latest_state.append(value)

                if len(get_data().latest_state) > 100:
                    get_data().latest_state.pop(0)

                await asyncio.sleep(1)
        except RuntimeError as RE:
            Logger.logger.error(f"Runtime Error In Worker: {RE}")
        except Exception as e:
            Logger.logger.error(f"Worker error: {e}")
            await asyncio.sleep(1)