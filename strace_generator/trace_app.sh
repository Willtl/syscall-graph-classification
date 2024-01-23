#!/bin/bash

# Function to handle the interrupt signal (Ctrl+C)
trap "echo 'Exiting...'; exit 0" SIGINT

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

# Create a directory for the application if it doesn't exist
APP_DIR="${APP_NAME}_strace_logs"
mkdir -p "$APP_DIR"

# Set of PIDs already traced
declare -A traced_pids

# Loop indefinitely
while true; do
    # Find PIDs associated with the application name
    PIDS=$(pgrep -x "$APP_NAME")

    # Check if any PIDs were found
    if [ -z "$PIDS" ]; then
        echo "No processes found for the application name: $APP_NAME"
    else
        for pid in $PIDS; do
            # Check if PID is already being traced
            if [ -z "${traced_pids[$pid]}" ]; then
                # Trace new PID and save output to the application's directory
                strace -o "${APP_DIR}/strace_output_${APP_NAME}_${pid}" -p $pid &
                traced_pids[$pid]=1
                echo "Tracing PID $pid for $APP_NAME. Output file: ${APP_DIR}/strace_output_${APP_NAME}_${pid}"
            fi
        done
    fi

    # Sleep for a short period before checking again
    sleep 2
done
