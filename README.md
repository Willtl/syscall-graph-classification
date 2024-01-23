# syscall-graph-classification

# System Call Sequence Graph Generator

## Overview
This script analyzes sequences of system calls from a file and constructs a directed graph to represent these sequences. Utilizing PyTorch Geometric and NetworkX libraries, it visualizes the flow of system calls. This visualization is instrumental in understanding application behavior and can be particularly useful for detecting patterns in malware.

## Features
- **Graph Generation**: Converts sequences of system calls into a directed graph.
- **System Call Filtering**: Option to filter the graph based on a predefined list of relevant system calls.
- **Visualization**: Uses NetworkX for graph visualization, providing a clear view of the system call sequence flow.

## System Call Filtering
The script can optionally filter system calls based on a predefined list of relevant system calls. This feature is useful for focusing on specific types of system calls that are more indicative of certain behaviors in applications.

## Visualization Details
The graph visualization plots each system call as a node, with directed edges representing the sequence in which system calls occur. The nodes are color-coded and labeled for easy identification.

## Relevant System Calls
The script focuses on a set of relevant system calls for detailed analysis. Below is the table of these system calls along with their descriptions:

| Notation | System Call  | Description                                    | Notation | System Call | Description                                   |
|----------|--------------|------------------------------------------------|----------|-------------|-----------------------------------------------|
| A        | recvfrom     | to receive a message from a socket             | B        | write       | write to a file descriptor                    |
| C        | ioctl        | manipulates the underlying device parameters   | D        | read        | for read operation                            |
| E        | send to      | send a message on a socket                     | F        | dup         | used to create a copy of the file descriptor  |
| G        | writev       | to write data to manipulate buffer             | H        | pread       | write to or read from a file descriptor to a given offset |
| I        | close        | to close a file descriptor                     | J        | socket      | is used to create an endpoint for communication |
| K        | bind         | to bind a name to a socket                     | L        | connect     | to start a connection on a socket directory   |
| M        | mkdir        | is used to create a directory                  | N        | access      | used to check the users permission for accessing the file |
| O        | chmod        | is used to change the permission of a file     | P        | open        | to open a file specified by the path name     |
| Q        | fchown       | used to change the ownership of a file         | R        | rename      | change the location or name of a file         |
| S        | unlink       | to remove a file                               | T        | pwrit       | write or read from a file descriptor          |
| U        | umask        | used to get file mode creation mask            | V        | fcntl64     | used to change the file descriptor            |
| W        | recvmsg      | used to receive a message from a socket        | X        | sendmsg     | used to send a message on a socket            |
| Y        | getdents64   | used to obtain the directory entries           | Z        | epoll wait  | used to wait for an I/O event                 |


## Usage
To use this script, ensure you have Python installed along with the required libraries: `matplotlib`, `networkx`, `torch`, and `torch_geometric`.

Run the script using the following command:

```bash
python script.py /path/to/syscall_file -f
```
* `/path/to/syscall_file` should be replaced with the path to your file containing system call sequences.
* Append `-f` if you wish to filter the system calls based on a predefined set of relevant system calls.

