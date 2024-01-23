# strace_generator

The `strace_generator` folder contains the `trace_app.sh` script, which is used to attach `strace` to all processes associated with a specified application. This script is useful for generating system call traces of an application, which can be further used for analysis or as input data for graph generation and classification models.

## Usage

The script takes the name of the application as an argument and attaches `strace` to each of its processes, outputting the system call traces to separate files.

### Prerequisites

- Ensure you have `strace` installed on your system. If not, you can install it using your distribution's package manager.
- The script is intended to be run on Unix-like operating systems.

### Running the Script

1. Make the script executable:
   ```bash
   chmod +x trace_app.sh

2. Run the script with the application name:
	```bash
	sudo ./trace_app.sh -name [application_name] 