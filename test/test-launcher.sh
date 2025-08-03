#!/bin/bash

# Test script for the system-config-lvm launcher
# This script demonstrates various features of the launcher

set -e

echo "========================================"
echo "Testing system-config-lvm launcher script"
echo "========================================"
echo ""

LAUNCHER="./run-system-config-lvm.sh"

# Test 1: Help function
echo "1. Testing help function:"
echo "----------------------------------------"
$LAUNCHER --help
echo ""

# Test 2: Version information
echo "2. Testing version information:"
echo "----------------------------------------"
$LAUNCHER --version
echo ""

# Test 3: Dependency check
echo "3. Testing dependency check:"
echo "----------------------------------------"
$LAUNCHER --check
echo ""

# Test 4: Debug mode check (without actually running the GUI)
echo "4. Testing debug mode (dependency check only):"
echo "----------------------------------------"
echo "Note: This would show debug information if we ran the full application"
echo "Command that would be used: $LAUNCHER --debug --check"
echo ""

echo "========================================"
echo "All launcher tests completed successfully!"
echo ""
echo "To actually run the GUI application:"
echo "  $LAUNCHER"
echo ""
echo "Note: The GUI requires a display and will prompt for root privileges"
echo "========================================"