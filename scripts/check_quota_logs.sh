#!/bin/bash

# Script to check JetBrains AI Assistant quota refresh logs
# Usage: ./check_quota_logs.sh <IDE_BASE_PATH>

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Error: IDE base path not provided."
    echo "Usage: $0 <IDE_BASE_PATH>"
    echo "Example: $0 /path/to/your/JetBrains/IDE/installation"
    echo "Note: Please provide the base path to your JetBrains IDE installation."
    echo "      For example, if your log file is at '/path/to/IDE/system/log/idea.log',"
    echo "      then provide '/path/to/IDE' as the argument."
    exit 1
fi

IDE_PATH="$1"
LOG_FILE="${IDE_PATH}/system/log/idea.log"

# Check if the log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file not found at $LOG_FILE"
    echo "Please check if the path is correct and the file exists."
    exit 1
fi

echo "Analyzing AI Assistant quota logs from: $LOG_FILE"
echo "------------------------------------------------------"

# Extract quota-related log entries
echo "Recent quota updates (last 20 entries):"
echo ""

grep "QuotaManager2" "$LOG_FILE" | grep -E "New quota state|quota refill|Quota update requested" | tail -20 | while read -r line; do
    # Extract timestamp
    TIMESTAMP=$(echo "$line" | cut -d' ' -f1-2)
    
    # Extract message
    MESSAGE=$(echo "$line" | sed 's/.*QuotaManager2 - //')
    
    # Format the output
    echo "[$TIMESTAMP] $MESSAGE"
done

echo ""
echo "------------------------------------------------------"

# Extract the latest quota information
echo "Latest quota information:"
echo ""

LATEST_QUOTA=$(grep "QuotaManager2" "$LOG_FILE" | grep "New quota state is: Available" | tail -1)

if [ -n "$LATEST_QUOTA" ]; then
    # Extract timestamp
    TIMESTAMP=$(echo "$LATEST_QUOTA" | cut -d' ' -f1-2)
    
    # Extract quota details
    QUOTA_DETAILS=$(echo "$LATEST_QUOTA" | sed 's/.*Available(//' | sed 's/)//')
    
    # Parse the details
    CURRENT=$(echo "$QUOTA_DETAILS" | sed 's/current=//' | sed 's/,.*//')
    MAXIMUM=$(echo "$QUOTA_DETAILS" | sed 's/.*maximum=//' | sed 's/,.*//')
    UNTIL=$(echo "$QUOTA_DETAILS" | sed 's/.*until=//' | sed 's/Z.*//')Z
    
    # Format the output
    echo "Last Updated: [$TIMESTAMP]"
    echo "Current Usage: $CURRENT tokens"
    echo "Maximum Quota: $MAXIMUM tokens"
    echo "Valid Until: $UNTIL"
    
    # Calculate percentage used
    if [[ "$CURRENT" =~ ^[0-9]+(\.[0-9]+)?$ ]] && [[ "$MAXIMUM" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        PERCENTAGE=$(awk "BEGIN {printf \"%.2f\", ($CURRENT/$MAXIMUM)*100}")
        echo "Percentage Used: $PERCENTAGE%"
    fi
else
    echo "No quota information found in the logs."
fi

echo "------------------------------------------------------"
echo "Note: This information is based on the log file and may not reflect real-time usage."
