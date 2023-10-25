@echo off

rem run function
:run
python main.py
goto :eof

rem Install function
:install
pip install -r requirements.txt
pre-commit install
goto :eof

rem Test function
:test
python -m pytest test_main.py
goto :eof

rem Commit function
:commit
git add .
git commit
goto :eof

rem Format function
:fmt
python -m black .
goto :eof

rem create virtual environment using venv
:v
echo Creating virtual environment with variable name
python -m venv %1
goto :EOF


:activate
echo Activating virtual environment
source %1/bin/activate
goto :EOF

rem create virtual environment using pipenv
:V
echo Creating virtual environment with variable name
pipenv shell
goto :EOF

rem Execute function based on the first argument
%1

:eof
