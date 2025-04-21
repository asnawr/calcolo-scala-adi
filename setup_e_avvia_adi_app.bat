@echo off
title 📊 Setup + Avvio Calcolo Scala ADI 2025

echo ======================================
echo 📦 Inizializzazione dell'ambiente...
echo ======================================

REM 1. Vai nella cartella dell'app
cd /d C:\calcolo_scala_adi.py\adi-app

REM 2. Crea ambiente virtuale se non esiste
if not exist "..\adi_env" (
    echo ➕ Creo ambiente virtuale...
    python -m venv ..\adi_env
)

REM 3. Attiva ambiente virtuale
echo ✅ Attivo ambiente virtuale...
call ..\adi_env\Scripts\activate.bat

REM 4. Installa pacchetti se necessari
echo 📥 Installazione pacchetti (streamlit, pandas)...
pip install --upgrade pip
pip install -r requirements.txt

REM 5. Crea file config.toml per disattivare telemetry
set "streamlit_cfg=%USERPROFILE%\.streamlit"
if not exist "%streamlit_cfg%" mkdir "%streamlit_cfg%"

set "config_file=%streamlit_cfg%\config.toml"
if not exist "%config_file%" (
    echo [browser] > "%config_file%"
    echo gatherUsageStats = false >> "%config_file%"
    echo ✅ config.toml creato in %config_file%
) else (
    echo ℹ️  config.toml già esistente
)

REM 6. Avvia app Streamlit
echo 🚀 Avvio dell'app in corso...
start "" http://localhost:8501
streamlit run calcolo_scala_adi.py
