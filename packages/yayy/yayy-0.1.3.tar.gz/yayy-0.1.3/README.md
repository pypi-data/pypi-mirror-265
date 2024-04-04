# yayy

## Scripts

These are batch files, save them in a .bat format.

1. `install.bat`
```bat
@echo off
echo Installing yayy Python package...

REM Check if pip is installed
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python pip is not installed or not in PATH.
    exit /b 1
)

REM Install yayy package
python -m pip install yayy

REM Check if installation was successful
if %errorlevel% equ 0 (
    echo yayy installed successfully.
) else (
    echo Error: Failed to install yayy.
    exit /b 1
)

exit /b 0
```

2. `run.bat`
```bat
@echo off
echo Running yayy...

REM
fkvit

echo yayy execution completed.

pause
```
You may run the tool manually post installation by typing `fkvit` in your terminal.

## Note:
- Get your gemini api key from [here](https://aistudio.google.com/app/apikey).
- Copy da MCQ and paste it in the terminal by simply pressing enter key.
- Wait for the answers to arrive.
- Supported OS: Windows 11
- To reset terminal opacity back to 100%, rerun the tool and kill the process by pressing `ctrl+c`.

# Lastly
![image](https://github.com/arpy8/queky/assets/74809468/671d24e4-77a6-474b-a083-730b2874f15f)