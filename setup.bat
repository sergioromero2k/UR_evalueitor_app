@echo off
echo.
echo  EVALUEITOR - Instalacion
echo  ========================
echo.
echo  Creando entorno virtual...
python -m venv venv

echo  Instalando dependencias...
venv\Scripts\pip install customtkinter --quiet

echo.
echo  Listo! Ahora ejecuta run.bat para iniciar el examen.
echo.
pause