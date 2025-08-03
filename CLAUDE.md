# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

system-config-lvm is a Python 3 GUI application that provides a graphical interface to LVM2 (Logical Volume Manager) tools. It wraps command-line LVM utilities in a user-friendly interface for non-emergency storage administration.

**Migration Status**: This codebase has been migrated from Python 2 to Python 3 and from PyGTK (GTK+ 2) to PyGObject (GTK+ 3).

## Build System & Development Commands

### Build Commands
```bash
# Initial setup (requires automake-1.7 and aclocal-1.7)
./autogen.sh

# Build
make

# Create source RPM
make srpm

# Clean
make clean
```

### Ubuntu/Debian Package Building
```bash
# Build source package
debuild -S -d -us -uc

# Build with pbuilder for focal
pbuilder-dist focal build ../[filename].dsc

# Build for upload
debuild -S -sd

# Upload to PPA
dput [ppa name] [filename]_source.changes
```

### Development Tools
```bash
# Generate documentation
make docs

# Python code checking
make pycheck
```

## Architecture Overview

### Core Components

**Main Application (`system-config-lvm.py`):**
- Entry point requiring root privileges
- Initializes GTK interface and handles LVM locking validation
- Uses Glade XML files for UI definition

**LVM Model Layer (`lvm_model.py`):**
- Core data model interfacing with LVM2 commands
- Parses output from `pvs`, `lvs`, `vgs` commands
- Manages Physical Volumes, Volume Groups, and Logical Volumes

**Volume Management Classes:**
- `PhysicalVolume.py` - Physical volume operations
- `VolumeGroup.py` - Volume group management  
- `LogicalVolume.py` - Logical volume operations
- `Segment.py` - LVM segment handling
- `ExtentBlock.py` - Extent allocation tracking

**Device Layer:**
- `BlockDevice.py` / `BlockDeviceModel.py` - Block device abstraction
- `Partition.py` - Partition management
- `Multipath.py` - Multipath device support

**Filesystem Integration:**
- `Filesystem.py` - Filesystem operations (fsck, resize2fs)
- `Fstab.py` - /etc/fstab management

**UI Components:**
- `Volume_Tab_View.py` - Main tabbed interface
- `Properties_Renderer.py` - Property display rendering
- `renderer.py` - Custom GTK renderers
- Glade files: `lvui.glade`, `lv_edit_props.glade`, `migrate_extents.glade`

**Utilities:**
- `execute.py` - Command execution with progress dialogs
- `CommandHandler.py` / `CommandError.py` - Command processing
- `fdisk_wrapper.py` / `parted_wrapper.py` - Partitioning tool wrappers

### Dependencies

**Runtime Dependencies:**
- Python 3.6+ 
- GTK+ 3 with python3-gi (PyGObject)
- python3-gi-cairo for Cairo integration
- gir1.2-gtk-3.0 (GTK+ 3 GObject introspection bindings)
- LVM2 tools
- Filesystem utilities (fsck, resize2fs)

**Build Dependencies:**
- autotools (automake-1.7, aclocal-1.7)
- Python 3.6+
- gettext for internationalization
- intltool for translation integration

## Key Design Patterns

**MVC Architecture:**
- Model: `lvm_model.py` and LVM object classes
- View: Glade XML UI definitions and renderer classes  
- Controller: `Volume_Tab_View.py` and input controllers

**Command Pattern:**
- LVM operations wrapped in command objects
- Error handling through `CommandError` exceptions
- Progress tracking via `ProgressPopup`

**Observer Pattern:**
- UI automatically updates when LVM model changes
- Tree model reloading on volume modifications

## Migration Notes

**Python 2 to 3 Migration Completed:**
- Updated shebang from `#!/usr/bin/python2` to `#!/usr/bin/python3`
- Converted all `print` statements to `print()` functions
- Updated exception handling from `except Error, e:` to `except Error as e:`
- Fixed string/unicode handling (`__builtin__` → `builtins`, `.iteritems()` → `.items()`)

**PyGTK to PyGObject Migration Completed:**
- Updated imports from `import gtk` to `from gi.repository import Gtk`
- Converted `gtk.glade.XML()` to `Gtk.Builder().add_from_file()`
- Updated all GTK constants (e.g., `gtk.MESSAGE_ERROR` → `Gtk.MessageType.ERROR`)
- Migrated GDK usage patterns to modern equivalents

**Known Migration Issues:**
- Some drawing operations may need further Cairo integration
- Glade files (.glade) should eventually be converted to UI files (.ui)
- Some deprecated GTK+ 2 patterns may need additional refinement

## Important Notes

- **Python 3 Required**: This codebase now requires Python 3.6+
- **GTK+ 3 Required**: Uses PyGObject with GTK+ 3
- **Root Required**: Application must run with root privileges for LVM operations
- **LVM Locking**: Validates LVM configuration and cluster state before startup
- **RAID Warning**: Does not recognize RAID elements, may allow destructive operations on RAID-backed LVs
- **Internationalization**: Full i18n support with extensive translation files in `po/`