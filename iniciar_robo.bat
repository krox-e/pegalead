@echo off
title Robô de Disparo 100% Automático WhatsApp - Leonardo
cd /d "%~dp0"
echo ===================================================================
echo  ROBO DE DISPARO 100%% AUTOMATICO WHATSAPP WEB
echo ===================================================================
echo.
echo Iniciando servidor e automacao Playwright na porta 5000...
echo.
.\uv.exe run --with fastapi --with uvicorn --with playwright python app_automacao.py
pause
