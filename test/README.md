# Test Directory

This directory contains testing utilities and launcher scripts for the system-config-lvm application.

## Contents

### `run-system-config-lvm.sh`
A comprehensive bash launcher script that:
- Automatically checks system dependencies
- Handles root privilege requirements
- Provides debug and testing modes
- Works from any directory location
- Includes comprehensive help and usage information

### `test-launcher.sh`
A test script that demonstrates the launcher functionality without actually starting the GUI.

### `LAUNCHER_README.md`
Detailed documentation for the launcher script including:
- Usage examples
- System requirements
- Installation instructions
- Troubleshooting guide

## Quick Usage

```bash
# Check if all dependencies are installed
./run-system-config-lvm.sh --check

# Test the launcher functionality
./test-launcher.sh

# Run the application (will prompt for sudo if needed)
./run-system-config-lvm.sh

# Get help
./run-system-config-lvm.sh --help
```

## Features Tested

✅ **Python 3 Compatibility**
- All Python files compile successfully
- Core modules import without errors
- Fixed tuple unpacking syntax issues
- Fixed regex escape sequences
- Added missing gettext imports

✅ **Dependency Management**
- Automatic detection of required packages
- Clear error messages for missing dependencies
- Installation guidance for different Linux distributions

✅ **Root Privilege Handling**
- Automatic sudo invocation when needed
- Safe privilege checking
- Option to skip for testing

## System Requirements

The launcher automatically checks for:
- Python 3.6+
- GTK+ 3 with PyGObject bindings
- LVM2 tools
- All required Python modules

## Notes

- The launcher script automatically locates the project source directory
- Works whether placed in project root or subdirectories
- Provides colored output for better user experience
- Includes comprehensive error handling and user guidance