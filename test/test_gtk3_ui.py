#!/usr/bin/env python3
"""
Simple test script to verify GTK+ 3 UI file loading and basic menu functionality.
This tests the converted UI files without running the full LVM application.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def test_ui_loading():
    """Test that UI files can be loaded successfully"""
    ui_files = [
        'lvui_gtk3.ui',
        'lv_edit_props.ui', 
        'migrate_extents.ui',
        'Filesystem.ui'
    ]
    
    results = {}
    
    for ui_file in ui_files:
        ui_path = os.path.join('..', 'src', ui_file)
        try:
            builder = Gtk.Builder()
            builder.add_from_file(ui_path)
            results[ui_file] = "SUCCESS"
            print(f"✓ {ui_file} loaded successfully")
        except Exception as e:
            results[ui_file] = f"ERROR: {e}"
            print(f"✗ {ui_file} failed: {e}")
    
    return results

def test_menu_structure():
    """Test that the main UI has the expected menu structure"""
    ui_path = os.path.join('..', 'src', 'lvui_gtk3.ui')
    
    try:
        builder = Gtk.Builder()
        builder.add_from_file(ui_path)
        
        # Test that key objects exist
        expected_objects = [
            'window1',
            'menubar1', 
            'file1',
            'quit1',
            'tools1',
            'view1',
            'help1',
            'about1',
            'reload_lvm'
        ]
        
        missing_objects = []
        for obj_id in expected_objects:
            obj = builder.get_object(obj_id)
            if obj is None:
                missing_objects.append(obj_id)
        
        if missing_objects:
            print(f"✗ Missing objects in lvui_gtk3.ui: {missing_objects}")
            return False
        else:
            print("✓ All expected menu objects found in lvui_gtk3.ui")
            return True
            
    except Exception as e:
        print(f"✗ Error testing menu structure: {e}")
        return False

def main():
    print("Testing GTK+ 3 UI file conversion...")
    print("=" * 50)
    
    # Change to test directory so relative paths work
    os.chdir(os.path.dirname(__file__))
    
    # Test UI file loading
    print("\n1. Testing UI file loading...")
    ui_results = test_ui_loading()
    
    # Test menu structure 
    print("\n2. Testing menu structure...")
    menu_ok = test_menu_structure()
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    
    success_count = sum(1 for result in ui_results.values() if result == "SUCCESS")
    total_count = len(ui_results)
    
    print(f"UI Files: {success_count}/{total_count} loaded successfully")
    print(f"Menu Structure: {'✓' if menu_ok else '✗'}")
    
    if success_count == total_count and menu_ok:
        print("\n🎉 All tests passed! GTK+ 3 conversion successful.")
        return 0
    else:
        print("\n❌ Some tests failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())