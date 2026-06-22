# src/controller/sensor.py

from fastapi import APIRouter, Depends , HTTPException 
from fastapi.responses import JSONResponse
from src.core.deps.deps import get_data
from src.services.LogService import LogService

router = APIRouter(prefix="/api")

@router.get("/state")
def get_state(data = Depends(get_data)):
    if not data.latest_state or data.latest_state is None:
        # return HTTPException(status_code=404,detail="data is null")
        return [{
            "gsr": i.get("gsr", 0) if isinstance(i, dict) else getattr(i, "gsr", 0),
            "baseline": i.get("baseline", 0) if isinstance(i, dict) else getattr(i, "baseline", 0),
            "diff": i.get("diff", 0) if isinstance(i, dict) else getattr(i, "diff", 0),
            "state": i.get("state", "ESTAVEL") if isinstance(i, dict) else getattr(i, "state", "ESTAVEL")
        } for i in data.latest_state]
        
    return [{
            "gsr": i.gsr,
            "baseline": i.baseline,
            "diff": i.diff,
            "state": i.state
    } for i in data.latest_state]

@router.post("/log")
def generete_log(data = Depends(get_data)):
    log = LogService.create_log()
    if log:
        return JSONResponse(content="ok",status_code=200)
    return HTTPException(status_code=404,detail="Error In Generate File , please verify the log")