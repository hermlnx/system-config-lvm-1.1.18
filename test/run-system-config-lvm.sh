#!/bin/bash

# system-config-lvm launcher script
# This script provides a convenient way to run the system-config-lvm GUI application

set -e  # Exit on any error

# Script information
SCRIPT_NAME="run-system-config-lvm.sh"
SCRIPT_VERSION="1.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine project root directory (look for src directory)
if [[ -d "${SCRIPT_DIR}/src" ]]; then
    # Script is in project root
    PROJECT_ROOT="${SCRIPT_DIR}"
elif [[ -d "${SCRIPT_DIR}/../src" ]]; then
    # Script is in a subdirectory (like test/)
    PROJECT_ROOT="${SCRIPT_DIR}/.."
else
    # Try to find src directory in parent directories
    CURRENT_DIR="${SCRIPT_DIR}"
    while [[ "$CURRENT_DIR" != "/" ]]; do
        if [[ -d "$CURRENT_DIR/src" ]]; then
            PROJECT_ROOT="$CURRENT_DIR"
            break
        fi
        CURRENT_DIR="$(dirname "$CURRENT_DIR")"
    done
fi

# Set paths based on project root
SRC_DIR="${PROJECT_ROOT}/src"
MAIN_SCRIPT="${SRC_DIR}/system-config-lvm.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

System Config LVM - GUI for LVM2 management

OPTIONS:
    -h, --help          Show this help message
    -v, --version       Show version information
    -d, --debug         Run with debug output
    -c, --check         Check dependencies and requirements
    --no-root-check     Skip root privilege check (use with caution)

DESCRIPTION:
    This script launches the system-config-lvm GUI application, which provides
    a graphical interface for managing LVM2 (Logical Volume Manager) storage.
    
    The application requires root privileges to perform LVM operations.
    
EXAMPLES:
    $SCRIPT_NAME                    # Run normally (will prompt for sudo if needed)
    $SCRIPT_NAME --check            # Check if all requirements are met
    $SCRIPT_NAME --debug            # Run with debug information
    sudo $SCRIPT_NAME               # Run directly as root

REQUIREMENTS:
    - Python 3.6+
    - GTK+ 3 with PyGObject (python3-gi)
    - LVM2 tools (lvm2 package)
    - Root privileges for LVM operations

EOF
}

# Function to show version
show_version() {
    echo "system-config-lvm launcher script v${SCRIPT_VERSION}"
    echo "system-config-lvm GUI for LVM2 management"
    echo ""
    echo "Python version: $(python3 --version 2>/dev/null || echo 'Not found')"
    if [[ -f "$MAIN_SCRIPT" ]]; then
        echo "Main script: Found at $MAIN_SCRIPT"
    else
        echo "Main script: NOT FOUND at $MAIN_SCRIPT"
    fi
}

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        return 0  # Running as root
    else
        return 1  # Not running as root
    fi
}

# Function to check dependencies
check_dependencies() {
    local missing_deps=0
    
    print_info "Checking system dependencies..."
    
    # Check Python 3
    if command -v python3 >/dev/null 2>&1; then
        local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python 3 found: $python_version"
    else
        print_error "Python 3 not found. Please install python3."
        missing_deps=$((missing_deps + 1))
    fi
    
    # Check PyGObject (python3-gi)
    if python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null; then
        print_success "PyGObject (GTK+ 3 bindings) found"
    else
        print_error "PyGObject not found. Please install python3-gi and gir1.2-gtk-3.0."
        missing_deps=$((missing_deps + 1))
    fi
    
    # Check LVM2 tools
    if command -v lvm >/dev/null 2>&1; then
        local lvm_version=$(lvm version 2>/dev/null | head -n1 | cut -d' ' -f3 || echo "unknown")
        print_success "LVM2 tools found: $lvm_version"
    else
        print_warning "LVM2 tools not found. Install lvm2 package for full functionality."
    fi
    
    # Check if main script exists
    if [[ -f "$MAIN_SCRIPT" ]]; then
        print_success "Main application script found"
    else
        print_error "Main application script not found at: $MAIN_SCRIPT"
        missing_deps=$((missing_deps + 1))
    fi
    
    # Check if source directory is accessible
    if [[ -d "$SRC_DIR" ]]; then
        print_success "Source directory found: $SRC_DIR"
    else
        print_error "Source directory not found: $SRC_DIR"
        missing_deps=$((missing_deps + 1))
    fi
    
    # Test basic imports
    print_info "Testing Python imports..."
    if python3 -c "
import sys
sys.path.insert(0, '$SRC_DIR')
try:
    import lvm_model
    import Volume_Tab_View
    print('✓ Core modules import successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
" 2>/dev/null; then
        print_success "Python imports test passed"
    else
        print_error "Python imports test failed"
        missing_deps=$((missing_deps + 1))
    fi
    
    echo ""
    if [[ $missing_deps -eq 0 ]]; then
        print_success "All dependencies satisfied!"
        return 0
    else
        print_error "$missing_deps missing dependencies found."
        echo ""
        echo "To install missing dependencies on Ubuntu/Debian:"
        echo "  sudo apt-get install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 lvm2"
        echo ""
        echo "To install missing dependencies on RHEL/CentOS/Fedora:"
        echo "  sudo yum install python3 python3-gobject gtk3 lvm2"
        echo "  # or"
        echo "  sudo dnf install python3 python3-gobject gtk3 lvm2"
        return 1
    fi
}

# Function to run the application
run_application() {
    local debug_mode="$1"
    local skip_root_check="$2"
    
    # Check if main script exists
    if [[ ! -f "$MAIN_SCRIPT" ]]; then
        print_error "Main application script not found: $MAIN_SCRIPT"
        print_error "Please ensure you're running this script from the correct directory."
        exit 1
    fi
    
    # Check root privileges (unless skipped)
    if [[ "$skip_root_check" != "true" ]]; then
        if ! check_root; then
            print_warning "This application requires root privileges for LVM operations."
            print_info "Attempting to run with sudo..."
            
            # Check if sudo is available
            if command -v sudo >/dev/null 2>&1; then
                # Re-run this script with sudo, preserving arguments
                exec sudo "$0" "$@"
            else
                print_error "sudo not available. Please run as root:"
                print_error "  su -c '$0 $*'"
                exit 1
            fi
        else
            print_info "Running as root - LVM operations will be available."
        fi
    else
        print_warning "Root privilege check skipped - some LVM operations may fail."
    fi
    
    # Set up environment
    export PYTHONPATH="$SRC_DIR:${PYTHONPATH:-}"
    
    # Display startup information
    print_info "Starting system-config-lvm..."
    print_info "Source directory: $SRC_DIR"
    print_info "Main script: $MAIN_SCRIPT"
    
    if [[ "$debug_mode" == "true" ]]; then
        print_info "Debug mode enabled"
        export PYTHONPATH="$SRC_DIR"
        print_info "PYTHONPATH: $PYTHONPATH"
        print_info "Current user: $(whoami)"
        print_info "Current directory: $(pwd)"
    fi
    
    # Change to source directory
    cd "$SRC_DIR"
    
    # Run the application
    if [[ "$debug_mode" == "true" ]]; then
        print_info "Executing: python3 $MAIN_SCRIPT"
        python3 "$MAIN_SCRIPT" "$@"
    else
        # Run quietly, but still show any errors
        python3 "$MAIN_SCRIPT" "$@" 2>&1 | grep -v "^$"
    fi
}

# Main script logic
main() {
    local debug_mode="false"
    local skip_root_check="false"
    local check_only="false"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--version)
                show_version
                exit 0
                ;;
            -d|--debug)
                debug_mode="true"
                shift
                ;;
            -c|--check)
                check_only="true"
                shift
                ;;
            --no-root-check)
                skip_root_check="true"
                shift
                ;;
            *)
                # Unknown option, pass it through to the main application
                break
                ;;
        esac
    done
    
    # If check-only mode, run dependency check and exit
    if [[ "$check_only" == "true" ]]; then
        check_dependencies
        exit $?
    fi
    
    # Run dependency check (but don't exit on failure, just warn)
    if ! check_dependencies; then
        print_warning "Some dependencies are missing. The application may not work correctly."
        echo ""
        read -p "Do you want to continue anyway? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Aborted by user."
            exit 1
        fi
    fi
    
    echo ""
    
    # Run the application
    run_application "$debug_mode" "$skip_root_check" "$@"
}

# Run main function with all arguments
main "$@"