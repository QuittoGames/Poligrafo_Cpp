import asyncio
from src.services.ReaderService import ReaderService
from src.core.container import data_local
import random
from src.utils.logger import Logger

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

                data_local.latest_state.append(fake_value)

                if len(data_local.latest_state) > 100:
                    data_local.latest_state.pop(0)

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
                    data_local.latest_state.append(value)

                if len(data_local.latest_state) > 100:
                    data_local.latest_state.pop(0)

                await asyncio.sleep(1)
        except RuntimeError as RE:
            Logger.logger.error(f"Runtime Error In Worker: {RE}")
        except Exception as e:
            Logger.logger.error(f"Worker error: {e}")
            await asyncio.sleep(1)