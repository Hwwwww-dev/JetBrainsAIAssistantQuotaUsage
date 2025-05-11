#!/bin/bash

# Script to check JetBrains AI Assistant quota usage
# Usage: ./check_quota.sh <IDE_BASE_PATH>

# Check if xmllint is installed
if ! command -v xmllint &> /dev/null; then
    echo "Error: xmllint is not installed. Please install it first."
    exit 1
fi

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Error: IDE base path not provided."
    echo "Usage: $0 <IDE_BASE_PATH>"
    echo "Example: $0 /path/to/your/JetBrains/IDE/installation"
    echo "Note: Please provide the base path to your JetBrains IDE installation."
    echo "      For example, if your quota file is at '/path/to/IDE/config/options/AIAssistantQuotaManager2.xml',"
    echo "      then provide '/path/to/IDE' as the argument."
    exit 1
fi

IDE_PATH="$1"
QUOTA_FILE="${IDE_PATH}/config/options/AIAssistantQuotaManager2.xml"

# Check if the quota file exists
if [ ! -f "$QUOTA_FILE" ]; then
    echo "Error: Quota file not found at $QUOTA_FILE"
    echo "Please check if the path is correct and the file exists."
    exit 1
fi

echo "Analyzing AI Assistant quota usage from: $QUOTA_FILE"
echo "------------------------------------------------------"

# Extract quota information using xmllint
QUOTA_INFO=$(xmllint --xpath "//component[@name='AIAssistantQuotaManager2']/option[@name='quotaInfo']/@value" "$QUOTA_FILE" 2>/dev/null | sed 's/value="//' | sed 's/"//')
NEXT_REFILL=$(xmllint --xpath "//component[@name='AIAssistantQuotaManager2']/option[@name='nextRefill']/@value" "$QUOTA_FILE" 2>/dev/null | sed 's/value="//' | sed 's/"//')

if [ -z "$QUOTA_INFO" ]; then
    echo "No quota information found in the file."
    exit 1
fi

# Decode HTML entities and format JSON
QUOTA_INFO=$(echo "$QUOTA_INFO" | sed 's/&#10;/\n/g' | sed 's/&quot;/"/g')
if [ -n "$NEXT_REFILL" ]; then
    NEXT_REFILL=$(echo "$NEXT_REFILL" | sed 's/&#10;/\n/g' | sed 's/&quot;/"/g')
fi

# Extract quota details using grep with multiline support
TYPE=$(echo "$QUOTA_INFO" | grep -o '"type"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"type"[[:space:]]*:[[:space:]]*"//' | sed 's/"[[:space:]]*$//')
CURRENT=$(echo "$QUOTA_INFO" | grep -o '"current"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"current"[[:space:]]*:[[:space:]]*"//' | sed 's/"[[:space:]]*$//')
MAXIMUM=$(echo "$QUOTA_INFO" | grep -o '"maximum"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"maximum"[[:space:]]*:[[:space:]]*"//' | sed 's/"[[:space:]]*$//')
UNTIL=$(echo "$QUOTA_INFO" | grep -o '"until"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"until"[[:space:]]*:[[:space:]]*"//' | sed 's/"[[:space:]]*$//')

# Extract next refill details if available
if [ -n "$NEXT_REFILL" ]; then
    REFILL_TYPE=$(echo "$NEXT_REFILL" | grep -o '"type"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"type"[[:space:]]*:[[:space:]]*"//' | sed 's/"[[:space:]]*$//')
    NEXT_DATE=$(echo "$NEXT_REFILL" | grep -o '"next"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"next"[[:space:]]*:[[:space:]]*"//' | sed 's/"[[:space:]]*$//')
    
    # Extract tariff information if available
    TARIFF_AMOUNT=$(echo "$NEXT_REFILL" | grep -o '"amount"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"amount"[[:space:]]*:[[:space:]]*"//' | sed 's/"[[:space:]]*$//')
    TARIFF_DURATION=$(echo "$NEXT_REFILL" | grep -o '"duration"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"duration"[[:space:]]*:[[:space:]]*"//' | sed 's/"[[:space:]]*$//')
fi

# Format the output
echo "Current Quota Status:"
echo "---------------------"
echo "Quota Status: $TYPE"
echo "Current Usage: $CURRENT tokens"
echo "Maximum Quota: $MAXIMUM tokens"
echo "Valid Until: $UNTIL"

# Calculate percentage used
if [[ "$CURRENT" =~ ^[0-9]+(\.[0-9]+)?$ ]] && [[ "$MAXIMUM" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    PERCENTAGE=$(awk "BEGIN {printf \"%.2f\", ($CURRENT/$MAXIMUM)*100}")
    echo "Percentage Used: $PERCENTAGE%"
fi

# Display next refill information if available
if [ -n "$NEXT_REFILL" ] && [ -n "$REFILL_TYPE" ] && [ "$REFILL_TYPE" != "Unknown" ]; then
    echo ""
    echo "Next Quota Refill:"
    echo "-----------------"
    echo "Refill Type: $REFILL_TYPE"
    if [ -n "$NEXT_DATE" ]; then
        echo "Next Refill Date: $NEXT_DATE"
    fi
    if [ -n "$TARIFF_AMOUNT" ]; then
        echo "Refill Amount: $TARIFF_AMOUNT tokens"
    fi
    if [ -n "$TARIFF_DURATION" ]; then
        echo "Refill Duration: $TARIFF_DURATION"
    fi
fi

echo "------------------------------------------------------"
echo "Note: This information is based on the local cache and may not reflect real-time usage."
