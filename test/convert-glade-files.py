#!/usr/bin/env python3

"""
Manual Glade 2.0 to GTK+ 3 UI format converter
This script converts old .glade files to the new .ui format for GTK+ 3 compatibility
"""

import os
import re
import sys
import argparse

def convert_glade_to_ui(glade_content):
    """Convert Glade 2.0 XML format to GTK+ 3 UI format"""
    ui_content = glade_content
    
    # Remove DOCTYPE declaration
    ui_content = re.sub(r'<!DOCTYPE[^>]*>', '', ui_content, flags=re.DOTALL)
    
    # Replace root element
    ui_content = ui_content.replace('<glade-interface>', '<interface>')
    ui_content = ui_content.replace('</glade-interface>', '</interface>')
    
    # Convert widget elements to object elements  
    ui_content = re.sub(r'<widget\s+class="([^"]*)"(\s+id="[^"]*")?([^>]*)>', 
                       r'<object class="\1"\2\3>', ui_content)
    ui_content = ui_content.replace('</widget>', '</object>')
    
    # Convert child elements
    ui_content = re.sub(r'<child(\s[^>]*)?>([^<]*)<placeholder/></child>', 
                       r'<child\1>\2</child>', ui_content)
    
    # Convert property values from GTK+ 2 constants to GTK+ 3 values
    property_mappings = {
        'GTK_WINDOW_TOPLEVEL': 'toplevel',
        'GTK_WIN_POS_NONE': 'none',
        'GTK_WIN_POS_CENTER': 'center',
        'GTK_WIN_POS_CENTER_ON_PARENT': 'center-on-parent',
        'GTK_POLICY_AUTOMATIC': 'automatic',
        'GTK_POLICY_NEVER': 'never',
        'GTK_POLICY_ALWAYS': 'always',
        'GTK_SHADOW_IN': 'in',
        'GTK_SHADOW_OUT': 'out',
        'GTK_SHADOW_NONE': 'none',
        'GTK_SHADOW_ETCHED_IN': 'etched-in',
        'GTK_SHADOW_ETCHED_OUT': 'etched-out',
        'GTK_ORIENTATION_HORIZONTAL': 'horizontal',
        'GTK_ORIENTATION_VERTICAL': 'vertical',
        'GTK_SELECTION_SINGLE': 'single',
        'GTK_SELECTION_MULTIPLE': 'multiple',
        'GTK_SELECTION_BROWSE': 'browse',
        'GTK_SELECTION_NONE': 'none',
        'GTK_UPDATE_CONTINUOUS': 'continuous',
        'GTK_UPDATE_DISCONTINUOUS': 'discontinuous',
        'GTK_UPDATE_DELAYED': 'delayed',
        'GTK_POS_LEFT': 'left',
        'GTK_POS_RIGHT': 'right',
        'GTK_POS_TOP': 'top',
        'GTK_POS_BOTTOM': 'bottom',
        'GTK_JUSTIFY_LEFT': 'left',
        'GTK_JUSTIFY_RIGHT': 'right',
        'GTK_JUSTIFY_CENTER': 'center',
        'GTK_JUSTIFY_FILL': 'fill'
    }
    
    for old_constant, new_value in property_mappings.items():
        ui_content = re.sub(f'>{old_constant}<', f'>{new_value}<', ui_content)
    
    # Handle VBox/HBox conversion to Box with orientation
    # This is a complex conversion that might need manual review
    ui_content = re.sub(r'<object class="GtkVBox"', 
                       r'<object class="GtkBox"', ui_content)
    ui_content = re.sub(r'<object class="GtkHBox"', 
                       r'<object class="GtkBox"', ui_content)
    
    # Add orientation property after visible property for converted boxes
    # This is a simplified approach - in reality, this needs more sophisticated handling
    ui_content = re.sub(r'(<object class="GtkBox"[^>]*>[\s]*<property name="visible">True</property>)',
                       r'\1\n    <property name="orientation">vertical</property>', ui_content)
    
    # Clean up any extra whitespace
    ui_content = re.sub(r'\n\s*\n', '\n', ui_content)
    
    return ui_content

def convert_file(input_file, output_file=None):
    """Convert a single Glade file to UI format"""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return False
    
    if output_file is None:
        output_file = input_file.replace('.glade', '.ui')
    
    try:
        print(f"Converting {input_file} -> {output_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            glade_content = f.read()
        
        ui_content = convert_glade_to_ui(glade_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ui_content)
        
        print(f"✓ Successfully converted: {output_file}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {input_file}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert Glade 2.0 files to GTK+ 3 UI format')
    parser.add_argument('files', nargs='*', help='Glade files to convert')
    parser.add_argument('--all', action='store_true', help='Convert all .glade files in current directory')
    parser.add_argument('--src-dir', default='../src', help='Source directory containing .glade files')
    
    args = parser.parse_args()
    
    files_to_convert = []
    
    if args.all or not args.files:
        # Find all .glade files in the source directory
        src_dir = args.src_dir
        if os.path.exists(src_dir):
            for file in os.listdir(src_dir):
                if file.endswith('.glade'):
                    files_to_convert.append(os.path.join(src_dir, file))
        else:
            print(f"Source directory '{src_dir}' not found")
            return 1
    else:
        files_to_convert = args.files
    
    if not files_to_convert:
        print("No .glade files found to convert")
        return 1
    
    print(f"Found {len(files_to_convert)} .glade files to convert:")
    for file in files_to_convert:
        print(f"  - {file}")
    print()
    
    success_count = 0
    for file in files_to_convert:
        if convert_file(file):
            success_count += 1
    
    print(f"\nConversion completed: {success_count}/{len(files_to_convert)} files converted successfully")
    
    if success_count > 0:
        print("\nNote: The converted files may need manual review and adjustment.")
        print("Complex UI elements might not convert perfectly and may require manual fixes.")
        print("Test the converted UI files with your application.")
    
    return 0 if success_count == len(files_to_convert) else 1

if __name__ == '__main__':
    sys.exit(main())