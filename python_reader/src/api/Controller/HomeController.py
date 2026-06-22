from fastapi import APIRouter, Depends , HTTPException 
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from pathlib import Path

route_home = APIRouter()

class HomeController:
    @route_home.get("/home")
    def home():
        file_path = Path("src/frontend/web/index.html")
        return FileResponse(file_path)
