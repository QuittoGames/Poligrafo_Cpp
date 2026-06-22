@echo off
setlocal enabledelayedexpansion

title Poligrafos Graph Services - Setup & Run

echo ======================================
echo   POLIGRAFOS - SETUP + START
echo ======================================

set PYTHON_VERSION=3.14.3
set PYTHON_INSTALLER=python-3.14.3-amd64.exe
set REQUIREMENTS=requirements.txt

echo.
echo [1/5] Verificando Python...

python --version >nul 2>&1

if %errorlevel% == 0 (
    echo Python ja instalado.
) else (
    echo Python nao encontrado. Instalando...

    if not exist %PYTHON_INSTALLER% (
        echo Baixando Python %PYTHON_VERSION%...

        powershell -Command ^
        "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe -OutFile %PYTHON_INSTALLER%"
    )

    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
)

echo.
echo [2/5] Verificando ambiente virtual...

if exist venv\Scripts\python.exe (
    echo Venv valido encontrado. Usando ele.
) else (
    echo Criando ambiente virtual...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo.
echo [3/5] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r %REQUIREMENTS%

echo.
echo [4/5] Iniciando servidor...
start cmd /k "venv\Scripts\python.exe -m uvicorn src.main:app --reload --port 8001"

timeout /t 5 >nul

echo.
echo [5/5] Testando API...

curl http://127.0.0.1:8001/docs >nul 2>&1

if %errorlevel% == 0 (
    echo Server OK
    start http://127.0.0.1:8001/home
) else (
    echo ERRO: servidor nao subiu
)

echo.
echo ======================================
echo  PRONTO
echo ======================================

pause
endlocal