#!/bin/bash

# 打包JetBrains AI Assistant配额分析器命令行版本
# 此脚本用于创建可执行文件

echo "===== 开始打包JetBrains AI Assistant配额分析器命令行版本 ====="

# 检查PyInstaller是否已安装
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller未安装，正在安装..."
    pip install pyinstaller
    
    # 检查安装是否成功
    if ! command -v pyinstaller &> /dev/null; then
        echo "PyInstaller安装失败，请手动安装后重试:"
        echo "pip install pyinstaller"
        exit 1
    fi
fi

# 检测操作系统
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_TYPE=Linux;;
    Darwin*)    OS_TYPE=macOS;;
    CYGWIN*)    OS_TYPE=Windows;;
    MINGW*)     OS_TYPE=Windows;;
    *)          OS_TYPE="未知"
esac

echo "检测到操作系统: $OS_TYPE"

# 清理之前的构建文件
echo "清理之前的构建文件..."
rm -rf build dist

# 使用spec文件构建可执行文件
echo "开始构建可执行文件..."
pyinstaller JetBrainsAIQuotaAnalyzer_CLI.spec --clean

# 检查构建是否成功
if [ "$OS_TYPE" = "macOS" ]; then
    # 检查macOS应用包
    if [ -d "dist/JetBrainsAIQuotaAnalyzer_CLI.app" ]; then
        echo "===== 构建成功! ====="
        echo "macOS应用包位于: dist/JetBrainsAIQuotaAnalyzer_CLI.app"
        
        # 显示可执行文件大小
        size=$(du -h -d 0 "dist/JetBrainsAIQuotaAnalyzer_CLI.app" | cut -f1)
        echo "应用包大小: $size"
        
        # 检查命令行可执行文件
        if [ -f "dist/JetBrainsAIQuotaAnalyzer_CLI" ]; then
            echo "命令行可执行文件位于: dist/JetBrainsAIQuotaAnalyzer_CLI"
            size=$(du -h "dist/JetBrainsAIQuotaAnalyzer_CLI" | cut -f1)
            echo "命令行可执行文件大小: $size"
        fi
        
        echo ""
        echo "使用方法:"
        echo "1. 双击 dist/JetBrainsAIQuotaAnalyzer_CLI.app 运行应用"
        echo "2. 或者使用命令行:"
        echo "   dist/JetBrainsAIQuotaAnalyzer_CLI -A --all  # 自动查找并分析所有配额文件"
        echo "   dist/JetBrainsAIQuotaAnalyzer_CLI -i        # 运行交互式界面"
        echo "   dist/JetBrainsAIQuotaAnalyzer_CLI --help    # 显示帮助信息"
    else
        # 检查命令行可执行文件
        if [ -f "dist/JetBrainsAIQuotaAnalyzer_CLI" ]; then
            echo "===== 构建成功! ====="
            echo "命令行可执行文件位于: dist/JetBrainsAIQuotaAnalyzer_CLI"
            size=$(du -h "dist/JetBrainsAIQuotaAnalyzer_CLI" | cut -f1)
            echo "命令行可执行文件大小: $size"
            
            echo ""
            echo "使用方法:"
            echo "dist/JetBrainsAIQuotaAnalyzer_CLI -A --all  # 自动查找并分析所有配额文件"
            echo "dist/JetBrainsAIQuotaAnalyzer_CLI -i        # 运行交互式界面"
            echo "dist/JetBrainsAIQuotaAnalyzer_CLI --help    # 显示帮助信息"
        else
            echo "===== 构建失败! ====="
            echo "请检查错误信息并修复问题"
            exit 1
        fi
    fi
else
    # 检查Windows/Linux可执行文件
    if [ -f "dist/JetBrainsAIQuotaAnalyzer_CLI" ] || [ -f "dist/JetBrainsAIQuotaAnalyzer_CLI.exe" ]; then
        echo "===== 构建成功! ====="
        
        if [ -f "dist/JetBrainsAIQuotaAnalyzer_CLI" ]; then
            echo "可执行文件位于: dist/JetBrainsAIQuotaAnalyzer_CLI"
            size=$(du -h "dist/JetBrainsAIQuotaAnalyzer_CLI" | cut -f1)
        else
            echo "可执行文件位于: dist/JetBrainsAIQuotaAnalyzer_CLI.exe"
            size=$(du -h "dist/JetBrainsAIQuotaAnalyzer_CLI.exe" | cut -f1)
        fi
        
        echo "可执行文件大小: $size"
        
        echo ""
        echo "使用方法:"
        if [ "$OS_TYPE" = "Windows" ]; then
            echo "dist\\JetBrainsAIQuotaAnalyzer_CLI.exe -A --all  # 自动查找并分析所有配额文件"
            echo "dist\\JetBrainsAIQuotaAnalyzer_CLI.exe -i        # 运行交互式界面"
            echo "dist\\JetBrainsAIQuotaAnalyzer_CLI.exe --help    # 显示帮助信息"
        else
            echo "dist/JetBrainsAIQuotaAnalyzer_CLI -A --all  # 自动查找并分析所有配额文件"
            echo "dist/JetBrainsAIQuotaAnalyzer_CLI -i        # 运行交互式界面"
            echo "dist/JetBrainsAIQuotaAnalyzer_CLI --help    # 显示帮助信息"
        fi
    else
        echo "===== 构建失败! ====="
        echo "请检查错误信息并修复问题"
        exit 1
    fi
fi

# 提示完成
echo ""
echo "打包过程完成!"
