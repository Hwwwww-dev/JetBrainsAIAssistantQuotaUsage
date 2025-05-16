@echo off
echo ===== 开始打包JetBrains AI Assistant配额分析器命令行版本 =====

REM 检查PyInstaller是否已安装
python -c "import PyInstaller" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller未安装，正在安装...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo 安装PyInstaller失败，请手动安装后重试。
        echo 可以使用命令: pip install pyinstaller
        exit /b 1
    )
)

REM 清理之前的构建文件
echo 清理之前的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM 开始构建可执行文件
echo 开始构建可执行文件...
pyinstaller JetBrainsAIQuotaAnalyzer_CLI.spec

if %ERRORLEVEL% NEQ 0 (
    echo 构建失败！请检查错误信息。
    exit /b 1
)

REM 检查是否成功创建可执行文件
if not exist dist\JetBrainsAIQuotaAnalyzer_CLI.exe (
    echo 构建过程完成，但未找到可执行文件。请检查构建日志。
    exit /b 1
)

REM 获取文件大小
for %%F in (dist\JetBrainsAIQuotaAnalyzer_CLI.exe) do set size=%%~zF
set /a size_mb=%size% / 1048576

echo ===== 构建成功! =====
echo 命令行可执行文件位于: dist\JetBrainsAIQuotaAnalyzer_CLI.exe
echo 命令行可执行文件大小: %size_mb%MB

echo.
echo 使用方法:
echo dist\JetBrainsAIQuotaAnalyzer_CLI.exe -A --all  # 自动查找并分析所有配额文件
echo dist\JetBrainsAIQuotaAnalyzer_CLI.exe -i        # 运行交互式界面
echo dist\JetBrainsAIQuotaAnalyzer_CLI.exe --help    # 显示帮助信息
echo.
echo 打包过程完成!
