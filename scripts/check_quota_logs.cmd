@echo off
setlocal enabledelayedexpansion

REM Script to check JetBrains AI Assistant quota refresh logs
REM Usage: check_quota_logs.cmd <IDE_BASE_PATH>

REM Check if argument is provided
if "%~1"=="" (
    echo Error: IDE base path not provided.
    echo Usage: %0 ^<IDE_BASE_PATH^>
    echo Example: %0 C:\Path\to\your\JetBrains\IDE\installation
    echo Note: Please provide the base path to your JetBrains IDE installation.
    echo       For example, if your log file is at 'C:\Path\to\IDE\system\log\idea.log',
    echo       then provide 'C:\Path\to\IDE' as the argument.
    exit /b 1
)

set "IDE_PATH=%~1"
set "LOG_FILE=%IDE_PATH%\system\log\idea.log"

REM Check if the log file exists
if not exist "%LOG_FILE%" (
    echo Error: Log file not found at %LOG_FILE%
    echo Please check if the path is correct and the file exists.
    exit /b 1
)

echo Analyzing AI Assistant quota logs from: %LOG_FILE%
echo ------------------------------------------------------

REM Create temporary files for processing
set "TEMP_FILE=%TEMP%\quota_logs.txt"
set "LATEST_QUOTA_FILE=%TEMP%\latest_quota.txt"

REM Extract quota-related log entries
echo Recent quota updates (last 20 entries):
echo.

REM Use findstr to find quota-related entries and save to temp file
findstr /C:"QuotaManager2" "%LOG_FILE%" > "%TEMP_FILE%"

REM Filter for specific quota-related messages
findstr /C:"New quota state" /C:"quota refill" /C:"Quota update requested" "%TEMP_FILE%" > "%TEMP_FILE%.filtered"

REM Display the last 20 entries (using a simple loop as Windows batch doesn't have tail)
set "count=0"
set "lines="
for /f "tokens=*" %%a in ('type "%TEMP_FILE%.filtered"') do (
    set /a count+=1
    set "lines[!count!]=%%a"
)

REM Display last 20 entries
if !count! gtr 0 (
    set /a start=count-19
    if !start! lss 1 set start=1
    
    for /l %%i in (!start!,1,!count!) do (
        set "line=!lines[%%i]!"
        for /f "tokens=1,2 delims=]" %%b in ("!line!") do (
            set "timestamp=%%b"
            set "timestamp=!timestamp:~1!"
            for /f "tokens=*" %%d in ("%%c") do (
                set "message=%%d"
                set "message=!message:*QuotaManager2 - =!"
                echo [!timestamp!] !message!
            )
        )
    )
) else (
    echo No quota-related log entries found.
)

echo.
echo ------------------------------------------------------

REM Extract the latest quota information
echo Latest quota information:
echo.

REM Find the latest quota state
findstr /C:"New quota state is: Available" "%TEMP_FILE%" > "%LATEST_QUOTA_FILE%"

REM Check if any quota information was found
for %%A in ("%LATEST_QUOTA_FILE%") do if %%~zA==0 (
    echo No quota information found in the logs.
) else (
    REM Get the last line (latest quota information)
    set "latest_line="
    for /f "tokens=*" %%a in ('type "%LATEST_QUOTA_FILE%"') do (
        set "latest_line=%%a"
    )
    
    if defined latest_line (
        REM Extract timestamp
        for /f "tokens=1,2 delims=]" %%b in ("!latest_line!") do (
            set "timestamp=%%b"
            set "timestamp=!timestamp:~1!"
            
            REM Extract quota details
            for /f "tokens=*" %%d in ("%%c") do (
                set "details=%%d"
                set "details=!details:*Available(=!"
                set "details=!details:)=!"
                
                REM Parse details
                for /f "tokens=1,2,3 delims=," %%e in ("!details!") do (
                    set "current=%%e"
                    set "maximum=%%f"
                    set "until=%%g"
                    
                    set "current=!current:current=!"
                    set "current=!current:~1!"
                    
                    set "maximum=!maximum:maximum=!"
                    set "maximum=!maximum:~1!"
                    
                    set "until=!until:until=!"
                    set "until=!until:~1!"
                    
                    echo Last Updated: [!timestamp!]
                    echo Current Usage: !current! tokens
                    echo Maximum Quota: !maximum! tokens
                    echo Valid Until: !until!
                )
            )
        )
    ) else (
        echo No quota information found in the logs.
    )
)

REM Clean up temporary files
del "%TEMP_FILE%" 2>nul
del "%TEMP_FILE%.filtered" 2>nul
del "%LATEST_QUOTA_FILE%" 2>nul

echo ------------------------------------------------------
echo Note: This information is based on the log file and may not reflect real-time usage.

endlocal
