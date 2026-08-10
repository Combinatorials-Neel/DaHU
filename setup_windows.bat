@echo off

mkdir uploads

REM Set up virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip and install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install --upgrade wheel
pip install --upgrade setuptools
pip install --upgrade pillow
pip install --no-cache-dir -r requirements.txt

echo Setup complete!
pause
