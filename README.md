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

## Manual Methods

### Method 1: Check Account Usage

You can directly check your AI Assistant quota usage by examining the `AIAssistantQuotaManager2.xml` file.

#### File Location by OS:

- **Windows**: `%APPDATA%\JetBrains\<IDE>\options\AIAssistantQuotaManager2.xml`
- **macOS**: `~/Library/Application Support/JetBrains/<IDE>/options/AIAssistantQuotaManager2.xml`
- **Linux**: `~/.config/JetBrains/<IDE>/options/AIAssistantQuotaManager2.xml`

Where `<IDE>` is your specific JetBrains IDE (e.g., IntelliJ IDEA 2025.1, WebStorm 2025.1, etc.)

### Method 2: Check Refresh Logs

You can also check the quota refresh logs in the IDE log file by searching for the keyword "QuotaManager2".

#### Log File Location by OS:

- **Windows**: `%APPDATA%\JetBrains\<IDE>\system\log\idea.log`
- **macOS**: `~/Library/Logs/JetBrains/<IDE>/idea.log`
- **Linux**: `~/.cache/JetBrains/<IDE>/log/idea.log`

## Using the Scripts

This project provides scripts to help you check your quota information for both Unix/Linux/macOS (bash) and Windows (cmd):

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
./scripts/check_quota_logs.sh <IDE_BASE_PATH>
```

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
