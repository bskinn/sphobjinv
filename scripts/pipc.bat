@echo off

setlocal

if "%~1"=="" (
  echo No pip-compile targets provided.
  exit /b 1
)

set CUSTOM_COMPILE_COMMAND=%0 %*

:loop
if "%~1"=="" goto :end
set arg=%1
shift

if "%arg%"=="dev" (
    pip-compile -o "requirements-dev.txt" "requirements-dev.in"
) else if "%arg%"=="ci" (
    pip-compile -o "requirements-ci.txt" "requirements-ci.in"
) else if "%arg%"=="flake8" (
    pip-compile -o "requirements-flake8.txt" "requirements-flake8.in"
) else if "%arg%"=="rtd" (
    pip-compile -o "requirements-rtd.txt" "requirements-rtd.in"
) else (
    echo Unknown argument '%arg%'
)

goto :loop

:end
endlocal
