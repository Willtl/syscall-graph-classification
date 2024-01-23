#!/bin/bash

# Check if an application name was provided
if [ $# -eq 0 ]; then
    echo "No application name provided. Usage: $0 -name [application_name]"
    exit 1
fi

# Extract the application name from the arguments
for i in "$@"; do
    case $i in
        -name)
        APP_NAME="${2}"
        shift # past argument
        shift # past value
        ;;
        *)
        # unknown option
        ;;
    esac
done

# Check if the application name is empty
if [ -z "$APP_NAME" ]; then
    echo "No application name provided. Usage: $0 -name [application_name]"
    exit 1
fi

# Find PIDs associated with the application name
PIDS=$(pgrep -x "$APP_NAME")

# Check if any PIDs were found
if [ -z "$PIDS" ]; then
    echo "No processes found for the application name: $APP_NAME"
    exit 1
fi

# Loop through each PID and attach strace
for pid in $PIDS; do
    strace -o "strace_output_${APP_NAME}_$pid" -p $pid &
done

echo "Tracing PIDs for $APP_NAME. Output files will be named strace_output_${APP_NAME}_PID."
