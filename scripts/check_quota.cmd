@echo off
setlocal enabledelayedexpansion

REM Script to check JetBrains AI Assistant quota usage
REM Usage: check_quota.cmd <IDE_BASE_PATH>

REM Check if argument is provided
if "%~1"=="" (
    echo Error: IDE base path not provided.
    echo Usage: %0 ^<IDE_BASE_PATH^>
    echo Example: %0 C:\Path\to\your\JetBrains\IDE\installation
    echo Note: Please provide the base path to your JetBrains IDE installation.
    echo       For example, if your quota file is at 'C:\Path\to\IDE\config\options\AIAssistantQuotaManager2.xml',
    echo       then provide 'C:\Path\to\IDE' as the argument.
    exit /b 1
)

set "IDE_PATH=%~1"
set "QUOTA_FILE=%IDE_PATH%\config\options\AIAssistantQuotaManager2.xml"

REM Check if the quota file exists
if not exist "%QUOTA_FILE%" (
    echo Error: Quota file not found at %QUOTA_FILE%
    echo Please check if the path is correct and the file exists.
    exit /b 1
)

echo Analyzing AI Assistant quota usage from: %QUOTA_FILE%
echo ------------------------------------------------------

REM Create temporary files for processing
set "TEMP_XML=%TEMP%\ai_quota_xml.txt"
set "QUOTA_INFO_FILE=%TEMP%\quota_info.txt"
set "NEXT_REFILL_FILE=%TEMP%\next_refill.txt"

REM Copy XML file to temp and decode HTML entities
type "%QUOTA_FILE%" > "%TEMP_XML%"

REM Replace HTML entities with actual characters
powershell -Command "(Get-Content '%TEMP_XML%') -replace '&#10;', [char]10 -replace '&quot;', '\"' | Set-Content '%TEMP_XML%'"

REM Extract quota information and next refill information
type "%TEMP_XML%" | findstr "quotaInfo" > "%QUOTA_INFO_FILE%"
type "%TEMP_XML%" | findstr "nextRefill" > "%NEXT_REFILL_FILE%"

REM Check if quota information was found
for %%A in ("%QUOTA_INFO_FILE%") do if %%~zA==0 (
    echo No quota information found in the file.
    del "%TEMP_XML%" 2>nul
    del "%QUOTA_INFO_FILE%" 2>nul
    del "%NEXT_REFILL_FILE%" 2>nul
    exit /b 1
)

REM Initialize variables
set "TYPE="
set "CURRENT="
set "MAXIMUM="
set "UNTIL="
set "REFILL_TYPE="
set "NEXT_DATE="
set "TARIFF_AMOUNT="
set "TARIFF_DURATION="

REM Parse the quota info
for /f "tokens=*" %%a in ('type "%QUOTA_INFO_FILE%"') do (
    set "line=%%a"
    
    REM Extract type
    echo !line! | findstr /C:"\"type\"" > nul
    if !errorlevel! equ 0 (
        for /f "tokens=1,2 delims=:" %%b in ('echo !line! ^| findstr /C:"\"type\""') do (
            for /f "tokens=1,2 delims=," %%d in ('echo %%c') do (
                set "TYPE=%%d"
                set "TYPE=!TYPE:"=!"
                set "TYPE=!TYPE: =!"
            )
        )
    )
    
    REM Extract current
    echo !line! | findstr /C:"\"current\"" > nul
    if !errorlevel! equ 0 (
        for /f "tokens=1,2 delims=:" %%b in ('echo !line! ^| findstr /C:"\"current\""') do (
            for /f "tokens=1,2 delims=," %%d in ('echo %%c') do (
                set "CURRENT=%%d"
                set "CURRENT=!CURRENT:"=!"
                set "CURRENT=!CURRENT: =!"
            )
        )
    )
    
    REM Extract maximum
    echo !line! | findstr /C:"\"maximum\"" > nul
    if !errorlevel! equ 0 (
        for /f "tokens=1,2 delims=:" %%b in ('echo !line! ^| findstr /C:"\"maximum\""') do (
            for /f "tokens=1,2 delims=," %%d in ('echo %%c') do (
                set "MAXIMUM=%%d"
                set "MAXIMUM=!MAXIMUM:"=!"
                set "MAXIMUM=!MAXIMUM: =!"
            )
        )
    )
    
    REM Extract until
    echo !line! | findstr /C:"\"until\"" > nul
    if !errorlevel! equ 0 (
        for /f "tokens=1,2 delims=:" %%b in ('echo !line! ^| findstr /C:"\"until\""') do (
            for /f "tokens=1,2 delims=}" %%d in ('echo %%c') do (
                set "UNTIL=%%d"
                set "UNTIL=!UNTIL:"=!"
                set "UNTIL=!UNTIL: =!"
            )
        )
    )
)

REM Parse the next refill info
for /f "tokens=*" %%a in ('type "%NEXT_REFILL_FILE%"') do (
    set "line=%%a"
    
    REM Extract refill type
    echo !line! | findstr /C:"\"type\"" > nul
    if !errorlevel! equ 0 (
        for /f "tokens=1,2 delims=:" %%b in ('echo !line! ^| findstr /C:"\"type\""') do (
            for /f "tokens=1,2 delims=," %%d in ('echo %%c') do (
                set "REFILL_TYPE=%%d"
                set "REFILL_TYPE=!REFILL_TYPE:"=!"
                set "REFILL_TYPE=!REFILL_TYPE: =!"
            )
        )
    )
    
    REM Extract next date
    echo !line! | findstr /C:"\"next\"" > nul
    if !errorlevel! equ 0 (
        for /f "tokens=1,2 delims=:" %%b in ('echo !line! ^| findstr /C:"\"next\""') do (
            for /f "tokens=1,2 delims=," %%d in ('echo %%c') do (
                set "NEXT_DATE=%%d"
                set "NEXT_DATE=!NEXT_DATE:"=!"
                set "NEXT_DATE=!NEXT_DATE: =!"
            )
        )
    )
    
    REM Extract tariff amount
    echo !line! | findstr /C:"\"amount\"" > nul
    if !errorlevel! equ 0 (
        for /f "tokens=1,2 delims=:" %%b in ('echo !line! ^| findstr /C:"\"amount\""') do (
            for /f "tokens=1,2 delims=," %%d in ('echo %%c') do (
                set "TARIFF_AMOUNT=%%d"
                set "TARIFF_AMOUNT=!TARIFF_AMOUNT:"=!"
                set "TARIFF_AMOUNT=!TARIFF_AMOUNT: =!"
            )
        )
    )
    
    REM Extract tariff duration
    echo !line! | findstr /C:"\"duration\"" > nul
    if !errorlevel! equ 0 (
        for /f "tokens=1,2 delims=:" %%b in ('echo !line! ^| findstr /C:"\"duration\""') do (
            for /f "tokens=1,2 delims=}" %%d in ('echo %%c') do (
                set "TARIFF_DURATION=%%d"
                set "TARIFF_DURATION=!TARIFF_DURATION:"=!"
                set "TARIFF_DURATION=!TARIFF_DURATION: =!"
            )
        )
    )
)

REM Clean up temporary files
del "%TEMP_XML%" 2>nul
del "%QUOTA_INFO_FILE%" 2>nul
del "%NEXT_REFILL_FILE%" 2>nul

REM Format the output
echo Current Quota Status:
echo ---------------------
echo Quota Status: %TYPE%
echo Current Usage: %CURRENT% tokens
echo Maximum Quota: %MAXIMUM% tokens
echo Valid Until: %UNTIL%

REM Calculate percentage if possible
if defined CURRENT if defined MAXIMUM (
    if "%CURRENT%"=="" set "CURRENT=0"
    if "%MAXIMUM%"=="" set "MAXIMUM=0"
    
    REM Check if both values are numeric
    echo %CURRENT%| findstr /r "^[0-9]*\.* *[0-9][0-9]*$" >nul
    if !errorlevel! equ 0 (
        echo %MAXIMUM%| findstr /r "^[0-9]*\.* *[0-9][0-9]*$" >nul
        if !errorlevel! equ 0 (
            REM Use PowerShell to calculate percentage
            for /f "delims=" %%p in ('powershell -Command "$current = [double]'%CURRENT%'; $max = [double]'%MAXIMUM%'; if ($max -gt 0) { $percent = ($current / $max) * 100; '{0:F2}' -f $percent } else { '0.00' }"') do (
                set "PERCENTAGE=%%p"
                echo Percentage Used: !PERCENTAGE!%%
            )
        )
    )
)

REM Display next refill information if available
if defined REFILL_TYPE if not "%REFILL_TYPE%"=="Unknown" (
    echo.
    echo Next Quota Refill:
    echo -----------------
    echo Refill Type: %REFILL_TYPE%
    if defined NEXT_DATE (
        echo Next Refill Date: %NEXT_DATE%
    )
    if defined TARIFF_AMOUNT (
        echo Refill Amount: %TARIFF_AMOUNT% tokens
    )
    if defined TARIFF_DURATION (
        echo Refill Duration: %TARIFF_DURATION%
    )
)

echo ------------------------------------------------------
echo Note: This information is based on the local cache and may not reflect real-time usage.

endlocal
