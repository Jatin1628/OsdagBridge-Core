@echo off
echo Running pre-unlink script for osdagbridge-core...

%PREFIX%\python.exe -m pip uninstall -y openseespy opsvis

echo Pre-unlink completed.
exit /b 0