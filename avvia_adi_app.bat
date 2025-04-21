@echo off
echo 📊 Avvio Calcolo Scala ADI 2025...

REM === 1. Crea .streamlit e config.toml se mancano ===
set "streamlit_cfg=%USERPROFILE%\.streamlit"
if not exist "%streamlit_cfg%" (
    mkdir "%streamlit_cfg%"
)

set "config_file=%streamlit_cfg%\config.toml"
if not exist "%config_file%" (
    echo [browser] > "%config_file%"
    echo gatherUsageStats = false >> "%config_file%"
    echo ✅ File config.toml creato in %config_file%
) else (
    echo ℹ️  config.toml già presente
)

REM === 2. Vai nella cartella dell'app ===
cd /d C:\calcolo_scala_adi.py\adi-app

REM === 3. (Facoltativo) Attiva ambiente virtuale ===
REM call ..\adi_env\Scripts\activate.bat

REM === 4. Avvia streamlit e apri il browser ===
start "" http://localhost:8501
streamlit run calcolo_scala_adi.py
