# system-config-lvm

*system-config-lvm* is a Python 3 GUI application that provides a graphical interface to LVM2 (Logical Volume Manager) tools. It wraps command-line LVM utilities in a user-friendly interface for non-emergency storage administration.

## Features

- **Graphical LVM Management**: Visual interface for Physical Volumes, Volume Groups, and Logical Volumes
- **2D Visualization**: Clean bar-based visualization of volume allocation and usage
- **GTK+ 3 Interface**: Modern PyGObject-based interface
- **Python 3**: Fully migrated from Python 2 to Python 3.6+
- **Root Integration**: Proper privilege handling for LVM operations

## Quick Start

### Development
```bash
# Clone and run for development
git clone <repository>
cd system-config-lvm
sudo make run
```

### Production Installation  
```bash
# Install system-wide
sudo make install
sudo system-config-lvm
```

## Requirements

- **Python 3.6+**
- **GTK+ 3** with PyGObject (`python3-gi`)
- **Cairo integration** (`python3-gi-cairo`)  
- **LVM2 tools**
- **Root privileges** (required for LVM operations)

## Build Documentation

See [Build.md](Build.md) for complete build and installation instructions.

## Migration Status

✅ **Complete Migration**: This codebase has been fully migrated:
- **Python 2 → Python 3** (syntax, libraries, string handling)
- **PyGTK → PyGObject** (GTK+ 2 → GTK+ 3)
- **Glade XML → GTK+ 3 UI files** (modern interface definitions)
- **3D visualization → 2D Cairo rendering** (simplified and reliable)
- **Autotools → Simple Makefile** (functional build system)

## License

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

