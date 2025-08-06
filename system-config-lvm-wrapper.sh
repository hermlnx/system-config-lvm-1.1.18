#!/bin/bash
# Production wrapper script for system-config-lvm
# This script ensures the application runs from the correct directory
# to find its UI and resource files

INSTALLDIR="/usr/local/share/system-config-lvm"
PYTHON_SCRIPT="system-config-lvm.py"

# Check if we're running as root
if [ "$(id -u)" != "0" ]; then
    echo "Error: system-config-lvm requires root privileges."
    echo "Run with: sudo system-config-lvm"
    exit 1
fi

# Check if the installation directory exists
if [ ! -d "$INSTALLDIR" ]; then
    echo "Error: Installation directory not found: $INSTALLDIR"
    echo "Please reinstall system-config-lvm."
    exit 1
fi

# Check if the Python script exists
if [ ! -f "$INSTALLDIR/$PYTHON_SCRIPT" ]; then
    echo "Error: Python script not found: $INSTALLDIR/$PYTHON_SCRIPT"
    echo "Please reinstall system-config-lvm."
    exit 1
fi

# Change to the installation directory and run the application
cd "$INSTALLDIR" || {
    echo "Error: Cannot change to installation directory: $INSTALLDIR"
    exit 1
}

# Execute the Python application with all arguments passed through
exec python3 "$PYTHON_SCRIPT" "$@"