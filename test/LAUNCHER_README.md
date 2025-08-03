# System Config LVM Launcher Script

This directory contains a convenient bash script to run the system-config-lvm GUI application.

## Quick Start

```bash
# Make sure you're in the project directory
cd /path/to/system-config-lvm-1.1.18

# Check if all dependencies are installed
./run-system-config-lvm.sh --check

# Run the application (will prompt for sudo if needed)
./run-system-config-lvm.sh
```

## Script Features

### 🔍 **Dependency Checking**
- Automatically checks for Python 3.6+
- Verifies GTK+ 3 and PyGObject bindings
- Tests LVM2 tools availability
- Validates core Python module imports

### 🛡️ **Root Privilege Management**
- Automatically detects if root privileges are needed
- Prompts for sudo when required
- Provides option to skip root checks for testing

### 🐛 **Debug Support**
- Debug mode for troubleshooting
- Detailed environment information
- Verbose output options

### 🎨 **User-Friendly Interface**
- Colored output for better readability
- Clear error messages and suggestions
- Comprehensive help documentation

## Usage Examples

```bash
# Basic usage - run the application
./run-system-config-lvm.sh

# Check system requirements
./run-system-config-lvm.sh --check

# Run with debug information
./run-system-config-lvm.sh --debug

# Show version information
./run-system-config-lvm.sh --version

# Get help
./run-system-config-lvm.sh --help

# Skip root privilege check (for testing)
./run-system-config-lvm.sh --no-root-check
```

## System Requirements

### Required Dependencies
- **Python 3.6+** - Core runtime
- **PyGObject (python3-gi)** - GTK+ 3 bindings for GUI
- **GTK+ 3** - GUI toolkit
- **LVM2 tools** - For LVM operations

### Installation Commands

**Ubuntu/Debian:**
```bash
sudo apt-get install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 lvm2
```

**RHEL/CentOS/Fedora:**
```bash
# RHEL/CentOS
sudo yum install python3 python3-gobject gtk3 lvm2

# Fedora
sudo dnf install python3 python3-gobject gtk3 lvm2
```

## Important Notes

### Root Privileges Required
System-config-lvm requires root privileges to perform LVM operations. The script will:
1. Check if already running as root
2. Automatically use `sudo` if available
3. Provide instructions for manual elevation if needed

### Security Considerations
- Always review code before running with root privileges
- The `--no-root-check` option is for development/testing only
- LVM operations can be destructive - use with caution

## Troubleshooting

### Common Issues

**"PyGObject not found" Error:**
```bash
# Install GTK+ 3 bindings
sudo apt-get install python3-gi gir1.2-gtk-3.0
```

**"Python imports test failed" Error:**
```bash
# Check Python path and try debug mode
./run-system-config-lvm.sh --debug --check
```

**"Main application script not found" Error:**
- Ensure you're running the script from the correct directory
- Check that `src/system-config-lvm.py` exists

### Debug Mode
Use debug mode to get detailed information:
```bash
./run-system-config-lvm.sh --debug --check
```

This will show:
- Python path configuration
- Environment variables
- Detailed import information
- File system checks

## Script Structure

The launcher script includes:
- **Dependency validation** - Ensures all required components are available
- **Environment setup** - Configures Python path and environment variables
- **Privilege management** - Handles root access requirements
- **Error handling** - Provides clear error messages and solutions
- **Cross-distribution support** - Works on various Linux distributions

## Development

To modify the launcher script:
1. Edit `run-system-config-lvm.sh`
2. Test with `--check` and `--debug` options
3. Verify both root and non-root execution paths
4. Test on different distributions if possible

## License

This launcher script is provided under the same license as the system-config-lvm project.