from fastapi import FastAPI
import asyncio
from src.services.WorkerService import Worker
from src.utils.tool import tool
from src.controller.SensorController import router as sensor_router
from src.data.data import Data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from src.utils.logger import Logger
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="src/frontend/web"), name="static")
app.include_router(sensor_router)

# =========================
# HOME (WEB)
# =========================

@app.get("/home")
def home():
    file_path = Path("src/frontend/web/index.html")
    return FileResponse(file_path)

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

        task.add_done_callback(lambda t: print(f"[TASK CRASH] {t.exception()}"))

    except Exception as e:
        Logger.logger.error(f"\033[91m[ERROR] {e}\033[0m")