# JetBrains AI Assistant Quota Usage Checker

This project helps you check your JetBrains AI Assistant quota usage information. It provides both manual methods and scripts to easily view your current quota status.

[中文文档](README_CN.md)

## Disclaimer

**This project is for educational and informational purposes only.**

- This tool is not officially affiliated with or endorsed by JetBrains.
- Users must comply with JetBrains' terms of service and usage policies when using this tool.
- Do not use this project for any commercial purposes or in ways that violate applicable laws or regulations.
- The authors are not responsible for any misuse of this tool or any consequences resulting from its use.
- Use this project at your own risk. The authors make no warranties about the accuracy or reliability of the information provided.
- This tool is designed to help users understand their quota usage, not to circumvent any limitations or restrictions.

## Command-Line Analyzer Tool

This project now includes a command-line version of the JetBrains AI Assistant Quota Analyzer. This tool provides an easy way to analyze your quota usage, track historical data, and filter records by path.

### Features

- **Auto-find quota files** across your system
- **Analyze quota information** from XML files
- **Track historical usage** in a SQLite database
- **Filter history** by file path
- **Interactive mode** with a user-friendly menu
- **Command-line arguments** for batch operations
- **Standalone executable** for easy deployment

### Installation

#### Option 1: Download the Standalone Executable

1. Download the latest release from the [Releases](https://github.com/hwwwww/JetBrainsAIAssistantQuotaUsage/releases) page
2. Extract the archive
3. Run the executable directly - no installation required!

#### Option 2: Run from Source

1. Clone this repository
2. Install the required dependencies (Python 3.6+ required)
3. Run the script using Python

### Usage

#### Using the Standalone Executable

##### Windows
```bash
JetBrainsAIQuotaAnalyzer_CLI.exe -A --all  # Auto-find and analyze all quota files
JetBrainsAIQuotaAnalyzer_CLI.exe -i        # Run in interactive mode
JetBrainsAIQuotaAnalyzer_CLI.exe --help    # Show help information
```

##### macOS/Linux
```bash
./JetBrainsAIQuotaAnalyzer_CLI -A --all    # Auto-find and analyze all quota files
./JetBrainsAIQuotaAnalyzer_CLI -i          # Run in interactive mode
./JetBrainsAIQuotaAnalyzer_CLI --help      # Show help information
```

On macOS, you can also double-click the `.app` bundle to run the application.

#### Running from Source

##### Interactive Mode

```bash
python JetBrainsAIQuotaAnalyzer_CLI.py -i
```

##### Auto-find and Analyze All Quota Files

```bash
python JetBrainsAIQuotaAnalyzer_CLI.py -A --all
```

##### Analyze a Specific File

```bash
python JetBrainsAIQuotaAnalyzer_CLI.py -a /path/to/AIAssistantQuotaManager2.xml
```

##### View History Records

```bash
python JetBrainsAIQuotaAnalyzer_CLI.py -H -l 20  # Show last 20 records
```

##### Filter History by Path

```bash
python JetBrainsAIQuotaAnalyzer_CLI.py -f /path/to/AIAssistantQuotaManager2.xml -l 5  # Show last 5 records for specific file
```

### Building the Executable

If you want to build the executable yourself:

1. Install PyInstaller: `pip install pyinstaller`
2. Run the build script:
   ```bash
   # On macOS/Linux
   chmod +x build_executable.sh
   ./build_executable.sh
   
   # On Windows
   build_executable.bat
   ```
3. The executable will be created in the `dist` directory

### Common Quota File Locations

#### Windows
```
%APPDATA%\JetBrains\<IDE>\options\AIAssistantQuotaManager2.xml
```

#### macOS
```
~/Library/Application Support/JetBrains/<IDE>/options/AIAssistantQuotaManager2.xml
```

#### Linux
```
~/.config/JetBrains/<IDE>/options/AIAssistantQuotaManager2.xml
```

Where `<IDE>` can be:
- PyCharm2024.1
- IntelliJIdea2024.1
- WebStorm2024.1
- CLion2024.1
- Etc.

## Understanding the Output

The tool will display information about your JetBrains AI Assistant quota, including:

- **Type**: The type of quota (usually "Available")
- **Current Value**: Your current quota amount
- **Maximum Value**: The maximum quota amount
- **Usage Percentage**: How much of your quota you've used
- **Valid Until**: The expiration date of your quota
- **Refill Information**: Details about when and how your quota will be refilled

### Example Output

```
配额信息:
类型: Available
当前值: 797931.70
最大值: 2000000.00
使用百分比: 39.90%
有效期至: 2026-05-21T21:00:00Z

补充信息:
补充类型: Known
下次补充: 2025-05-21T16:03:48.944Z
补充数量: 0.00
补充周期: 

时间戳: 2025-05-15T21:04:08.841381
文件路径: /Users/hwwwww/Library/Application Support/JetBrains/GoLand2025.1/options/AIAssistantQuotaManager2.xml
```

## Manual Methods

### Method 1: Check Account Usage

You can directly check your AI Assistant quota usage by examining the `AIAssistantQuotaManager2.xml` file.

#### File Location by OS:

- **Windows**: `%APPDATA%\JetBrains\<IDE>\options\AIAssistantQuotaManager2.xml`
- **macOS**: `~/Library/Application Support/JetBrains/<IDE>/options/AIAssistantQuotaManager2.xml`
- **Linux**: `~/.config/JetBrains/<IDE>/options/AIAssistantQuotaManager2.xml`

Where `<IDE>` is your specific JetBrains IDE (e.g., IntelliJ IDEA 2025.1, WebStorm 2025.1, etc.)

You can override the locations by creating `.check_quota_cached_quota_file_path` and `.check_quota_logs_cached_log_path` with the full paths to the related files.

### Method 2: Check Refresh Logs

You can also check the quota refresh logs in the IDE log file by searching for the keyword "QuotaManager2".

#### Log File Location by OS:

- **Windows**: `%APPDATA%\JetBrains\<IDE>\system\log\idea.log`
- **macOS**: `~/Library/Logs/JetBrains/<IDE>/idea.log`
- **Linux**: `~/.cache/JetBrains/<IDE>/log/idea.log`

## Using the Scripts

This project provides scripts to help you check your quota information for both Unix/Linux/macOS (bash) and Windows (cmd):

On MacOS and Linux the paths are stored in .check_quota_cached_quota_file_path and .check_quota_logs_cached_log_path after the first time use.

### 1. Check Current Quota Usage

#### For Unix/Linux/macOS:
```bash
./scripts/check_quota.sh <IDE_BASE_PATH>
```

#### For Windows:
```cmd
scripts\check_quota.cmd <IDE_BASE_PATH>
```

Example:
```bash
./scripts/check_quota.sh /path/to/your/JetBrains/IDE
```

**Note**: Please provide the base path to your JetBrains IDE installation. For example, if your quota file is at `/path/to/IDE/config/options/AIAssistantQuotaManager2.xml`, then provide `/path/to/IDE` as the argument.

### 2. Check Quota Refresh Logs

#### For Unix/Linux/macOS:
```bash
./scripts/check_quota_logs.sh [-n 200] <IDE_BASE_PATH>
```

-n flag is optional and overrides the default 200 limit.

#### For Windows:
```cmd
scripts\check_quota_logs.cmd <IDE_BASE_PATH>
```

Example:
```bash
./scripts/check_quota_logs.sh /path/to/your/JetBrains/IDE
```

**Note**: The scripts expect the following structure:
- Quota file at: `<IDE_BASE_PATH>/config/options/AIAssistantQuotaManager2.xml`
- Log file at: `<IDE_BASE_PATH>/system/log/idea.log`

## Sample Output

When you run the quota check script, you'll see output similar to this:

```
Analyzing AI Assistant quota usage from: /path/to/JetBrains/IDE/config/options/AIAssistantQuotaManager2.xml
------------------------------------------------------
Current Quota Status:
---------------------
Quota Status: Available
Current Usage: 1000000.0000 tokens
Maximum Quota: 2000000 tokens
Valid Until: 2026-06-01T00:00:00Z
Percentage Used: 50.00%

Next Quota Refill:
-----------------
Refill Type: Known
Next Refill Date: 2025-06-01T00:00:00.000Z
Refill Amount: 2000000 tokens
Refill Duration: PT720H
------------------------------------------------------
Note: This information is based on the local cache and may not reflect real-time usage.
```

## Understanding the Output

The quota information includes:
- **Quota Status**: Current status of your quota (Available, Exhausted, etc.)
- **Current Usage**: Your current usage quota in tokens
- **Maximum Quota**: Your maximum quota limit in tokens
- **Valid Until**: The expiration date of your current quota
- **Percentage Used**: How much of your quota has been used
- **Next Refill Date**: When your quota will be refreshed
- **Refill Amount**: How many tokens will be added on refresh
- **Refill Duration**: How long the refreshed quota will last

The log information shows:
- When quota updates were requested
- New quota states
- Refresh schedules

## Requirements

- Bash shell (for Unix/Linux/macOS) or Command Prompt (for Windows)
- xmllint (for XML parsing in bash script)
- grep (for log searching in bash script)
- PowerShell (for Windows scripts, used for HTML entity decoding)

## Notes

- **Windows Scripts**: The Windows command scripts (.cmd) have not been extensively tested. Please report any issues you encounter when using them.

## Acknowledgements

This project was developed with assistance from [Windsurf](http://windsurf.com).
