# src/controller/sensor.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.api.data.core.deps.deps import get_data
from src.api.Services.LogService import LogService
from src.api.model.Sensor_State import Sensor_State
import random
import time
import math

router = APIRouter(prefix="/api")

class SensorController:
    @router.get("/state")
    def get_state(data=Depends(get_data)):
        if get_data().Debug:
            if not hasattr(get_data(), "latest_state"):
                pass

            baseline = random.uniform(212, 216)

            r = random.random()

            # 80% normal
            if r < 0.8:
                diff = random.uniform(0.5, 3)
                state = "ESTAVEL"

            # 15% leve alteração
            elif r < 0.95:
                diff = random.uniform(4, 7)
                state = "LEVE_ALTERACAO"

            # 5% pico
            else:
                diff = random.uniform(8, 12)
                state = "PICO"

            gsr = baseline + diff
            sensor_state = Sensor_State(baseline, gsr, diff, state)

            get_data().latest_state.append(sensor_state)
            return [
                {
                    "gsr": round(sensor_state.gsr, 2),
                    "baseline": round(sensor_state.baseline, 2),
                    "diff": round(sensor_state.diff, 2),
                    "state": sensor_state.state,
                }
            ]

        latest = getattr(get_data(), "latest_state", None)

        if not isinstance(latest, list) or len(latest) == 0:
            return {"response": "buffer vazio - aguardando dados do sensor"}

        return [
            {"gsr": i.gsr, "baseline": i.baseline, "diff": i.diff, "state": i.state}
            for i in get_data().latest_state
        ]

    @router.get("/log")
    def generete_log(data=Depends(get_data)):
        log = LogService.create_log()
        if log:
            return JSONResponse(content="ok", status_code=200)
        return HTTPException(
            status_code=404, detail="Error In Generate File , please verify the log"
        )
