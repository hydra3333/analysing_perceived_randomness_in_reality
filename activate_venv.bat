@echo off
call "%~dp0.venv\Scripts\activate.bat"
if defined VIRTUAL_ENV (
    echo Python VIRTUAL_ENV=%VIRTUAL_ENV%
) else (
    echo Python Virtual environment is not active.
)
exit /b
