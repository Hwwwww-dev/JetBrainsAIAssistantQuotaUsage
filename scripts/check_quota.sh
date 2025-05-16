#!/bin/bash

# Script to check JetBrains AI Assistant quota usage
# Usage: ./check_quota.sh [<IDE_BASE_PATH>]
# If <IDE_BASE_PATH> is provided, the full QUOTA_FILE path is derived and cached.
# If not provided, the cached QUOTA_FILE path is used.

SCRIPT_DIR=$(dirname "$0")
# Configuration file to store the last used full QUOTA_FILE path
CONFIG_FILE="${SCRIPT_DIR}/.check_quota_cached_quota_file_path"

# Check if xmllint is installed
if ! command -v xmllint &> /dev/null; then
    echo "Error: xmllint is not installed. Please install it first."
    exit 1
fi

IDE_PATH_ARG=""
# Check if IDE base path argument is provided
if [ $# -gt 0 ]; then
    IDE_PATH_ARG="$1"
fi

QUOTA_FILE=""

if [ -n "$IDE_PATH_ARG" ]; then
    # IDE_BASE_PATH is provided, determine QUOTA_FILE and cache its full path
    # Remove trailing slash from IDE_PATH_ARG if it exists
    IDE_PATH_CLEANED="${IDE_PATH_ARG%/}"

    if [[ "$(uname -s)" == "Darwin" ]]; then
        # macOS
        QUOTA_FILE="${IDE_PATH_CLEANED}/options/AIAssistantQuotaManager2.xml"
    else
        # Other OS (Linux, etc.)
        QUOTA_FILE="${IDE_PATH_CLEANED}/config/options/AIAssistantQuotaManager2.xml"
    fi

    # Ensure SCRIPT_DIR is an absolute path or CONFIG_FILE path is correctly resolved
    if [[ "$SCRIPT_DIR" != /* && "$SCRIPT_DIR" != "." && "$SCRIPT_DIR" != ".." ]]; then
        CONFIG_FILE_PATH_TO_SAVE="$(pwd)/${SCRIPT_DIR#./}/.check_quota_cached_quota_file_path"
    elif [[ "$SCRIPT_DIR" == "." ]]; then
        CONFIG_FILE_PATH_TO_SAVE="$(pwd)/.check_quota_cached_quota_file_path"
    else # Covers absolute paths and ".."
        CONFIG_FILE_PATH_TO_SAVE="${CONFIG_FILE}"
    fi
    # Create directory for config file if it doesn't exist
    mkdir -p "$(dirname "$CONFIG_FILE_PATH_TO_SAVE")"
    echo "$QUOTA_FILE" > "$CONFIG_FILE_PATH_TO_SAVE"
    echo "IDE base path provided. Full quota file path set to '$QUOTA_FILE' and cached in '$CONFIG_FILE_PATH_TO_SAVE'."
elif [ -f "$CONFIG_FILE" ]; then
    # No IDE_BASE_PATH provided, try to use cached QUOTA_FILE path
    QUOTA_FILE=$(cat "$CONFIG_FILE")
    if [ -z "$QUOTA_FILE" ]; then
        echo "Error: Cached quota file path in '$CONFIG_FILE' is empty."
        echo "Please provide the <IDE_BASE_PATH> argument once to set it."
        echo "Usage: $0 [<IDE_BASE_PATH>]"
        exit 1
    fi
    echo "Using cached quota file path: $QUOTA_FILE (from $CONFIG_FILE)"
else
    # No IDE_BASE_PATH provided and no cached path found
    echo "Error: IDE base path not provided and no cached quota file path found in '$CONFIG_FILE'."
    echo "Please provide the <IDE_BASE_PATH> argument on the first run to cache the path."
    echo "Usage: $0 [<IDE_BASE_PATH>]"
    echo "Example (first run): $0 /path/to/your/JetBrains/IDE/installation"
    echo "Example (subsequent runs): $0"
    exit 1
fi

# Check if the quota file exists
if [ ! -f "$QUOTA_FILE" ]; then
    echo "Error: Quota file not found at $QUOTA_FILE"
    echo "Please check if the path is correct and the file exists."
    echo "If the cached path is incorrect, please run the script again with the correct <IDE_BASE_PATH>."
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
if [[ "$CURRENT" =~ ^[0-9]+(\.[0-9]+)?$ ]] && [[ "$MAXIMUM" =~ ^[0-9]+(\.[0-9]+)?$ ]] && [ $(echo "$MAXIMUM > 0" | bc -l 2>/dev/null) -eq 1 ]; then
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
