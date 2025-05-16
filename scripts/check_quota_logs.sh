#!/bin/bash

# Script to check JetBrains AI Assistant quota refresh logs
# Usage: ./check_quota_logs.sh [-n <number_of_entries>] [<IDE_BASE_PATH>]
# If <IDE_BASE_PATH> is provided, it's used and its corresponding log path is cached.
# If not provided, the cached log path is used.

SCRIPT_DIR=$(dirname "$0")
# Configuration file to store the last used log file path in the script's directory
CONFIG_FILE="${SCRIPT_DIR}/.check_quota_logs_cached_log_path"

# Default number of entries
NUM_ENTRIES=20
IDE_PATH_ARG=""

# Parse options for -n
while getopts ":n:" opt; do
  case ${opt} in
    n )
      if [[ "$OPTARG" =~ ^[0-9]+$ ]]; then
        NUM_ENTRIES=$OPTARG
      else
        echo "Error: Invalid number of entries specified for -n. Must be a positive integer."
        echo "Usage: $0 [-n <number_of_entries>] [<IDE_BASE_PATH>]"
        exit 1
      fi
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      echo "Usage: $0 [-n <number_of_entries>] [<IDE_BASE_PATH>]"
      exit 1
      ;;
    : )
      echo "Invalid option: -$OPTARG requires an argument" 1>&2
      echo "Usage: $0 [-n <number_of_entries>] [<IDE_BASE_PATH>]"
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# Check if IDE base path argument is provided (remaining argument after options)
if [ $# -gt 0 ]; then
    IDE_PATH_ARG="$1"
fi

LOG_FILE=""

if [ -n "$IDE_PATH_ARG" ]; then
    # IDE_BASE_PATH is provided, determine LOG_FILE and cache it
    # Remove trailing slash from IDE_PATH_ARG if it exists
    IDE_PATH_CLEANED="${IDE_PATH_ARG%/}"

    if [[ "$(uname -s)" == "Darwin" ]]; then
        # macOS
        LOG_FILE="${IDE_PATH_CLEANED}/idea.log"
    else
        # Other OS (Linux, etc.)
        LOG_FILE="${IDE_PATH_CLEANED}/system/log/idea.log"
    fi
    # Ensure SCRIPT_DIR is an absolute path or CONFIG_FILE path is correctly resolved if script is called from elsewhere
    if [[ "$SCRIPT_DIR" != /* && "$SCRIPT_DIR" != "." && "$SCRIPT_DIR" != ".." ]]; then
        CONFIG_FILE_PATH_TO_SAVE="$(pwd)/${SCRIPT_DIR#./}/.check_quota_logs_cached_log_path"
    elif [[ "$SCRIPT_DIR" == "." ]]; then
        CONFIG_FILE_PATH_TO_SAVE="$(pwd)/.check_quota_logs_cached_log_path"
    else # Covers absolute paths and ".."
        CONFIG_FILE_PATH_TO_SAVE="${CONFIG_FILE}"
    fi
    # Create directory for config file if it doesn't exist, to avoid error if SCRIPT_DIR is like ./scripts
    mkdir -p "$(dirname "$CONFIG_FILE_PATH_TO_SAVE")"
    echo "$LOG_FILE" > "$CONFIG_FILE_PATH_TO_SAVE"
    echo "IDE base path provided. Log file path set to '$LOG_FILE' and cached in '$CONFIG_FILE_PATH_TO_SAVE'."
elif [ -f "$CONFIG_FILE" ]; then
    # No IDE_BASE_PATH provided, try to use cached path
    LOG_FILE=$(cat "$CONFIG_FILE")
    if [ -z "$LOG_FILE" ]; then
        echo "Error: Cached log file path in '$CONFIG_FILE' is empty."
        echo "Please provide the <IDE_BASE_PATH> argument once to set it."
        echo "Usage: $0 [-n <number_of_entries>] [<IDE_BASE_PATH>]"
        exit 1
    fi
    echo "Using cached log file path: $LOG_FILE (from $CONFIG_FILE)"
else
    # No IDE_BASE_PATH provided and no cached path found
    echo "Error: IDE base path not provided and no cached path found in '$CONFIG_FILE'."
    echo "Please provide the <IDE_BASE_PATH> argument on the first run to cache the log path."
    echo "Usage: $0 [-n <number_of_entries>] [<IDE_BASE_PATH>]"
    echo "Example (first run): $0 /path/to/your/JetBrains/IDE/installation" # Note: Adjust example if it's for log dir
    echo "Example (subsequent runs): $0"
    exit 1
fi

# Check if the log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file not found at $LOG_FILE"
    echo "Please check if the path is correct and the file exists."
    echo "If the cached path is incorrect, please run the script again with the correct <IDE_BASE_PATH>."
    exit 1
fi

echo "Analyzing AI Assistant quota logs from: $LOG_FILE"
echo "------------------------------------------------------"

# Extract quota-related log entries
echo "Recent quota updates (last $NUM_ENTRIES entries):"
echo ""

PREV_AVAIL_CURRENT_VAL="" # Stores the 'current' value from the previous "Available" state line

# Use a while read loop for broader compatibility
grep "QuotaManager2" "$LOG_FILE" | grep -E "New quota state|quota refill|Quota update requested" | tail -n "$NUM_ENTRIES" | while IFS= read -r line; do
    TIMESTAMP=$(echo "$line" | cut -d' ' -f1-2)
    # Get the part of the message after "QuotaManager2 - "
    MESSAGE_CONTENT=$(echo "$line" | sed 's/.*QuotaManager2 - //')

    OUTPUT_DISPLAY_LINE="[$TIMESTAMP] $MESSAGE_CONTENT"
    DIFFERENCE_INFO_TEXT=""

    # Check if this line is a "New quota state is: Available" line
    if echo "$MESSAGE_CONTENT" | grep -q "New quota state is: Available"; then
        # Extract the 'current' value from this line
        CURRENT_VALUE_EXTRACTED=$(echo "$MESSAGE_CONTENT" | sed -n 's/.*current=\([0-9.]*\).*/\1/p')

        # Check if extracted value is a valid number
        if [[ -n "$CURRENT_VALUE_EXTRACTED" && "$CURRENT_VALUE_EXTRACTED" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
            # If there was a 'current' value from a previous "Available" line, calculate the difference
            if [[ -n "$PREV_AVAIL_CURRENT_VAL" && "$PREV_AVAIL_CURRENT_VAL" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
                DIFFERENCE=$(awk "BEGIN {printf \"%.4f\", $CURRENT_VALUE_EXTRACTED - $PREV_AVAIL_CURRENT_VAL}")
                DIFFERENCE_INFO_TEXT=" (Diff: $DIFFERENCE)"
            fi
            # Update the previous 'current' value with the one from this line
            PREV_AVAIL_CURRENT_VAL="$CURRENT_VALUE_EXTRACTED"
        else
            # If current value couldn't be extracted or is not numeric, reset previous
            PREV_AVAIL_CURRENT_VAL=""
        fi
    fi
    # Removed the else branch that was resetting PREV_AVAIL_CURRENT_VAL
    # This allows differences to be calculated between "Available" entries even when they're not consecutive

    echo "${OUTPUT_DISPLAY_LINE}${DIFFERENCE_INFO_TEXT}"
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
    if [[ "$CURRENT" =~ ^[0-9]+(\.[0-9]+)?$ ]] && [[ "$MAXIMUM" =~ ^[0-9]+(\.[0-9]+)?$ ]] && [ $(echo "$MAXIMUM > 0" | bc -l 2>/dev/null) -eq 1 ]; then
        PERCENTAGE=$(awk "BEGIN {printf \"%.2f\", ($CURRENT/$MAXIMUM)*100}")
        echo "Percentage Used: $PERCENTAGE%"
    fi
else
    echo "No quota information found in the logs."
fi

echo "------------------------------------------------------"
echo "Note: This information is based on the log file and may not reflect real-time usage."
