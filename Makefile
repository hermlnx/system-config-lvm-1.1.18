#!/usr/bin/make -f
# Simple Makefile for system-config-lvm development
# This replaces the complex autotools Makefile with something that works

PYTHON := python3
VERSION := 1.1.18
PREFIX := /usr/local
BINDIR := $(PREFIX)/bin
SBINDIR := $(PREFIX)/sbin
DATADIR := $(PREFIX)/share
PKGDATADIR := $(DATADIR)/system-config-lvm
APPLICATIONSDIR := $(DATADIR)/applications

# Source files
PYTHON_FILES := \
	src/InputController.py \
	src/CommandHandler.py \
	src/CommandError.py \
	src/lvm_model.py \
	src/lvmui_constants.py \
	src/Properties_Renderer.py \
	src/renderer.py \
	src/Volume_Tab_View.py \
	src/fdisk_wrapper.py \
	src/parted_wrapper.py \
	src/Partition.py \
	src/BlockDevice.py \
	src/BlockDeviceModel.py \
	src/Filesystem.py \
	src/Fstab.py \
	src/execute.py \
	src/cylinder_items.py \
	src/PhysicalVolume.py \
	src/LogicalVolume.py \
	src/VolumeGroup.py \
	src/Volume.py \
	src/Segment.py \
	src/ExtentBlock.py \
	src/WaitMsg.py \
	src/Multipath.py \
	src/utilities.py \
	src/Cluster.py \
	src/system-config-lvm.py

UI_FILES := \
	src/lvui.ui \
	src/lvui_fixed.ui \
	src/lvui_gtk3.ui \
	src/migrate_extents.ui \
	src/lv_edit_props.ui \
	src/Filesystem.ui

PIXMAP_FILES := \
	src/pixmaps/UV.xpm \
	src/pixmaps/VG.xpm \
	src/pixmaps/LV.xpm \
	src/pixmaps/PV.xpm \
	src/pixmaps/grad3.xpm \
	src/pixmaps/lv_icon.png

.PHONY: all build clean install uninstall test run help pycheck

# Default target
all: build

# Build target - create symlink for development
build:
	@echo "Building system-config-lvm..."
	cd src && rm -f system-config-lvm && ln -s system-config-lvm.py system-config-lvm
	@echo "Build complete. Use 'make run' to test or 'make install' to install."

# Clean compiled Python files and symlinks
clean:
	@echo "Cleaning..."
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	rm -f src/system-config-lvm
	rm -f system-config-lvm.desktop
	@echo "Clean complete."

# Install to system
install: build
	@echo "Installing system-config-lvm to $(PREFIX)..."
	
	# Create directories
	install -d $(DESTDIR)$(SBINDIR)
	install -d $(DESTDIR)$(PKGDATADIR)
	install -d $(DESTDIR)$(PKGDATADIR)/pixmaps
	install -d $(DESTDIR)$(APPLICATIONSDIR)
	
	# Install main Python files
	install -m 644 $(PYTHON_FILES) $(DESTDIR)$(PKGDATADIR)/
	install -m 755 src/system-config-lvm.py $(DESTDIR)$(PKGDATADIR)/
	
	# Install UI files
	install -m 644 $(UI_FILES) $(DESTDIR)$(PKGDATADIR)/
	
	# Install pixmaps
	install -m 644 $(PIXMAP_FILES) $(DESTDIR)$(PKGDATADIR)/pixmaps/
	
	# Create symlink in sbin
	ln -sf ../share/system-config-lvm/system-config-lvm.py $(DESTDIR)$(SBINDIR)/system-config-lvm
	
	# Install desktop file if it exists
	if [ -f system-config-lvm.desktop ]; then \
		install -m 644 system-config-lvm.desktop $(DESTDIR)$(APPLICATIONSDIR)/; \
	fi
	
	@echo "Installation complete."

# Uninstall from system
uninstall:
	@echo "Uninstalling system-config-lvm..."
	rm -rf $(DESTDIR)$(PKGDATADIR)
	rm -f $(DESTDIR)$(SBINDIR)/system-config-lvm
	rm -f $(DESTDIR)$(APPLICATIONSDIR)/system-config-lvm.desktop
	@echo "Uninstall complete."

# Run the application (requires root)
run: build
	@echo "Running system-config-lvm (requires root permissions)..."
	@if [ "$(shell id -u)" != "0" ]; then \
		echo "Error: system-config-lvm requires root privileges."; \
		echo "Run with: sudo make run"; \
		exit 1; \
	fi
	cd src && $(PYTHON) system-config-lvm.py

# Test syntax of Python files
test:
	@echo "Testing Python syntax..."
	@for file in $(PYTHON_FILES); do \
		echo "Checking $$file..."; \
		$(PYTHON) -m py_compile $$file || exit 1; \
	done
	@echo "All Python files passed syntax check."

# Python code quality check (if pychecker is available)
pycheck:
	@echo "Running Python code quality checks..."
	@if command -v pychecker >/dev/null 2>&1; then \
		pychecker $(PYTHON_FILES); \
	else \
		echo "pychecker not found, skipping code quality checks."; \
		echo "Install with: pip install pychecker"; \
	fi

# Create desktop file
desktop:
	@echo "Creating desktop file..."
	@if [ -f system-config-lvm.desktop.in ]; then \
		sed 's/@VERSION@/$(VERSION)/g' system-config-lvm.desktop.in > system-config-lvm.desktop; \
		echo "Desktop file created: system-config-lvm.desktop"; \
	else \
		echo "Warning: system-config-lvm.desktop.in not found"; \
	fi

# Show help
help:
	@echo "Available targets:"
	@echo "  all      - Build the application (default)"
	@echo "  build    - Build the application"
	@echo "  clean    - Remove compiled files and build artifacts"
	@echo "  install  - Install to system (PREFIX=$(PREFIX))"
	@echo "  uninstall- Remove from system"
	@echo "  run      - Run the application (requires root)"
	@echo "  test     - Test Python syntax"
	@echo "  pycheck  - Run code quality checks"
	@echo "  desktop  - Create desktop file"
	@echo "  help     - Show this help"
	@echo ""
	@echo "Variables:"
	@echo "  PREFIX   - Installation prefix (default: $(PREFIX))"
	@echo "  DESTDIR  - Destination directory for packaging"
	@echo "  PYTHON   - Python interpreter (default: $(PYTHON))"