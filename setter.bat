@echo off
setlocal

:: Step 1: Download and Install Python
set PYTHON_VERSION=3.11.5
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

echo Downloading Python %PYTHON_VERSION%...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile python-installer.exe"

echo Installing Python...
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

:: Verify Python installation
python --version
if %errorlevel% neq 0 (
    echo Python installation failed.
    exit /b 1
)

:: Step 2: Upgrade pip and install virtualenv
echo Upgrading pip and installing virtualenv...
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install --upgrade virtualenv

:: Step 3: Install Node.js
echo Installing Node.js...
powershell -Command "Invoke-WebRequest -Uri https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi -OutFile nodejs.msi"
msiexec /i nodejs.msi /quiet

:: Verify Node.js installation
node --version
if %errorlevel% neq 0 (
    echo Node.js installation failed.
    exit /b 1
)

:: Step 4: Install AWS CDK globally
echo Installing AWS CDK...
npm install -g aws-cdk

:: Verify AWS CDK installation
cdk --version
if %errorlevel% neq 0 (
    echo AWS CDK installation failed.
    exit /b 1
)

:: Step 5: Set up a new AWS CDK project
echo Creating AWS CDK project...
mkdir my-project
cd my-project
cdk init app --language python

:: Step 6: Set up Python virtual environment for the CDK project
echo Setting up Python virtual environment...
python -m virtualenv .venv

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

:: Step 7: Install project dependencies
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt
) else (
    echo No requirements.txt found, skipping dependency installation.
)

:: Clean up installers
cd ..
del python-installer.exe
del nodejs.msi

echo Setup complete! AWS CDK project is ready for development.
pause
