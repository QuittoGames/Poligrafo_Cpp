from fastapi import FastAPI
import asyncio
from src.api.Services.WorkerService import Worker
from src.api.utils.tool import tool
from src.api.Controller.SensorController import router as sensor_router
from src.api.Controller.HomeController import route_home
from src.api.data.data import Data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from src.api.utils.logger import Logger
from fastapi.staticfiles import StaticFiles


# Configure root logging (colors, format, level) before anything logs.
Logger.setup()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/frontend/web"), name="static")
app.include_router(sensor_router)
app.include_router(route_home)


# =========================
# STARTUP
# =========================
@app.on_event("startup")
async def startup():
    try:
        # tool.clear_screen()
        print("=" * 40)
        print("   Polígrafos Graph Services")
        print("=" * 40)

        task = asyncio.create_task(Worker.sensor_worker())

        task.add_done_callback(
            lambda t: (
                print("\033[93m[TASK STOPPED]\033[0m")
                if t.cancelled()
                else print(f"\033[91m[TASK CRASH]\033[0m {t.exception()}")
            )
        )
    except Exception as e:
        Logger.logger.error(f"\033[91m[ERROR] {e}\033[0m")
