# Build Instructions for system-config-lvm

This project uses a simple, functional Makefile that replaces the complex autotools build system.

## Development Build and Usage

```bash
# Build for development
make build

# Run for development (requires root privileges)
sudo make run

# Clean build artifacts and Python cache files
make clean

# Test Python syntax
make test

# Show all available targets
make help
```

## Production Installation

```bash
# Install to system (default: /usr/local)
sudo make install

# Run the application from anywhere
sudo system-config-lvm

# Uninstall from system
sudo make uninstall
```

## Build System Details

### Current Makefile Targets:
- `build` - Create symlink for development
- `run` - Run application in development mode (requires root)
- `install` - Install to system with wrapper script
- `uninstall` - Remove from system
- `clean` - Remove build artifacts and Python cache files  
- `test` - Test Python syntax of all source files
- `help` - Show available targets

### Installation Structure:
- **Executable**: `/usr/local/sbin/system-config-lvm` (wrapper script)
- **Application**: `/usr/local/share/system-config-lvm/system-config-lvm.py`
- **UI Files**: `/usr/local/share/system-config-lvm/*.ui`
- **Resources**: `/usr/local/share/system-config-lvm/pixmaps/`

The wrapper script ensures the application runs from the correct directory to find its UI and resource files.
