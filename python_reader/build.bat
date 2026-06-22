@echo off
title Poligrafos Graph Services


echo ========================================
echo   Poligrafos Graph Services - START
echo ========================================

color 0A
cd /d %~dp0

echo Iniciando servidor...

start cmd /k "python -m uvicorn src.main:app --reload --port 8001"

timeout /t 4 >nul

curl http://127.0.0.1:8001/docs >nul 2>&1

if %errorlevel% == 0 (
    echo Server OK
    start http://127.0.0.1:8001/home
) else (
    echo ERRO: servidor nao subiu
)
color 07
pause