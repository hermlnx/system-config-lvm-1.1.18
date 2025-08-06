#!/usr/bin/python3

"""Entry point for system-config-lvm.

   This application wraps the LVM2 command line
   interface in a graphical user interface.

"""
 
import sys
import types
import select
import signal
import string
import os

PROGNAME = "system-config-lvm"
INSTALLDIR="/usr/local/share/system-config-lvm"
VERSION = "@VERSION@"

### gettext ("_") must come before import gtk ###
import gettext
gettext.bindtextdomain(PROGNAME, "/usr/share/locale")
gettext.textdomain(PROGNAME)
try:
    gettext.install(PROGNAME, "/usr/share/locale")
except IOError:
    import builtins
    builtins.__dict__['_'] = str
                                                                                

### gettext first, then import gtk (exception prints gettext "_") ###
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import GObject
except RuntimeError as e:
    print(_("""")
  Unable to initialize graphical environment. Most likely cause of failure
  is that the tool was not run using a graphical environment. Please either
  start your graphical user interface or set your DISPLAY variable.
                                                                                
  Caught exception: %s
""") % e)
    sys.exit(-1)

from lvm_model import lvm_model, lvm_conf_get_locking_type
from Volume_Tab_View import Volume_Tab_View
from lvmui_constants import *

#import gnome
#import gnome.ui

#gnome.program_init (PROGNAME, VERSION)
#gnome.app_version = VERSION
FORMALNAME=_("system-config-lvm")
ABOUT_VERSION=_("%s %s") % ('system-config-lvm',VERSION)


from execute import execWithCapture
from Cluster import Cluster



###############################################
class baselvm:
  def __init__(self, glade_xml, app):
    
    
    # check locking type
    locking_type = lvm_conf_get_locking_type()
    if locking_type != 1:
        should_exit = False
        if locking_type == 0:
            msg = _("LVM locks are disabled!!! \nMassive data corruption may occur.\nEnable locking (locking_type=1, 2 or 3 in /etc/lvm/lvm.conf).")
            should_exit = True
        elif locking_type == 2 or locking_type == 3:
            ps_out = execWithCapture('/bin/ps', ['/bin/ps', '-A'])
            if ps_out.find('clvmd') == -1:
                msg = _("LVM is configured to use Cluster Locking mechanism, but clvmd daemon is not running. Start daemon with command:\nservice clvmd start \nor, turn off cluster locking (locking_type=1 in /etc/lvm/lvm.conf).")
                should_exit = True
            else:
                if not Cluster().running():
                    msg = _("LVM is configured to use Cluster Locking mechanism, but cluster is not quorate.\nEither wait until cluster is quorate or turn off cluster locking (locking_type=1 in /etc/lvm/lvm.conf).")
                    should_exit = True
        else:
            msg = _("%s only supports file and cluster based lockings (locking_type=1, 2 or 3 in /etc/lvm/lvm.conf).")
            msg = msg % PROGNAME
            should_exit = True
        if should_exit:
            dlg = Gtk.MessageDialog(parent=None, flags=0,
                                    message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK,
                                    text=msg)
            dlg.run()
            sys.exit(10)

    
    #Need to suppress the spewing of file descriptor errors to terminal
    os.environ["LVM_SUPPRESS_FD_WARNINGS"] = "1"

    self.lvmm = lvm_model()
                                                                                
    self.main_win = app
    self.glade_xml = glade_xml

    self.volume_tab_view = Volume_Tab_View(glade_xml, self.lvmm, self.main_win)

    self.glade_xml.connect_signals(
      {
        "on_quit1_activate" : self.quit,
        "on_about1_activate" : self.on_about,
        "on_reload_lvm_activate" : self.on_reload
      }
    )
                                                                                
  def on_about(self, *args):
       dialog = Gtk.MessageDialog(parent=None, flags=0,
                                    message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK,
                                    text="This software is licensed under the terms of the GPL. Copyright (c) 2004 Red Hat, Inc. All rights reserved.")
       dialog.run()
       dialog.destroy()
        
  
  def on_reload(self, *args):
      self.volume_tab_view.reset_tree_model()
  
  def quit(self, *args):
      Gtk.main_quit()



#############################################################
def convert_glade_to_ui(glade_content):
    """Convert old Glade 2.0 format to GTK+ 3 UI format"""
    import re
    
    # Basic conversion from Glade 2.0 to UI format
    ui_content = glade_content
    
    # Replace the DOCTYPE and root element
    ui_content = re.sub(r'<!DOCTYPE.*?>', '', ui_content, flags=re.DOTALL)
    ui_content = re.sub(r'<glade-interface>', '<interface>', ui_content)
    ui_content = re.sub(r'</glade-interface>', '</interface>', ui_content)
    
    # Convert widget class names from GTK 2 to GTK 3
    gtk2_to_gtk3_classes = {
        'GtkWindow': 'GtkWindow',
        'GtkVBox': 'GtkBox',
        'GtkHBox': 'GtkBox', 
        'GtkVPaned': 'GtkPaned',
        'GtkHPaned': 'GtkPaned',
        'GtkScrolledWindow': 'GtkScrolledWindow',
        'GtkTreeView': 'GtkTreeView',
        'GtkButton': 'GtkButton',
        'GtkLabel': 'GtkLabel',
        'GtkEntry': 'GtkEntry',
        'GtkComboBox': 'GtkComboBoxText',
        'GtkMenuItem': 'GtkMenuItem',
        'GtkMenu': 'GtkMenu',
        'GtkMenuBar': 'GtkMenuBar',
        'GtkToolbar': 'GtkToolbar',
        'GtkSeparatorToolItem': 'GtkSeparatorToolItem',
        'GtkToolButton': 'GtkToolButton',
        'GtkNotebook': 'GtkNotebook',
        'GtkFrame': 'GtkFrame',
        'GtkCheckButton': 'GtkCheckButton',
        'GtkRadioButton': 'GtkRadioButton',
        'GtkSpinButton': 'GtkSpinButton',
        'GtkProgressBar': 'GtkProgressBar',
        'GtkDialog': 'GtkDialog',
        'GtkMessageDialog': 'GtkMessageDialog'
    }
    
    for gtk2_class, gtk3_class in gtk2_to_gtk3_classes.items():
        ui_content = re.sub(f'class="{gtk2_class}"', f'class="{gtk3_class}"', ui_content)
    
    # Add orientation property for Box widgets that were VBox/HBox
    ui_content = re.sub(
        r'<widget class="GtkBox" id="([^"]*)">\s*<property name="visible">True</property>',
        lambda m: f'<object class="GtkBox" id="{m.group(1)}"><property name="visible">True</property><property name="orientation">vertical</property>' 
        if 'vbox' in m.group(1).lower() else 
        f'<object class="GtkBox" id="{m.group(1)}"><property name="visible">True</property><property name="orientation">horizontal</property>',
        ui_content
    )
    
    # Convert widget tags to object tags
    ui_content = re.sub(r'<widget\s+class="([^"]*)"', r'<object class="\1"', ui_content)
    ui_content = re.sub(r'</widget>', '</object>', ui_content)
    
    # Convert property values from constants to values
    property_conversions = {
        'GTK_WINDOW_TOPLEVEL': 'toplevel',
        'GTK_WIN_POS_NONE': 'none',
        'GTK_WIN_POS_CENTER': 'center',
        'GTK_POLICY_AUTOMATIC': 'automatic',
        'GTK_POLICY_NEVER': 'never',
        'GTK_SHADOW_IN': 'in',
        'GTK_SHADOW_OUT': 'out',
        'GTK_SHADOW_NONE': 'none',
        'GTK_ORIENTATION_HORIZONTAL': 'horizontal',
        'GTK_ORIENTATION_VERTICAL': 'vertical',
        'True': 'True',
        'False': 'False'
    }
    
    for old_value, new_value in property_conversions.items():
        ui_content = re.sub(f'>{old_value}<', f'>{new_value}<', ui_content)
    
    return ui_content

def initGlade():
    # Try GTK+ 3 compatible UI files in order of preference
    fixed_ui_file = "lvui_fixed.ui"
    gtk3_ui_file = "lvui_gtk3.ui"
    ui_file = "lvui.ui" 
    
    # Try installed location first (for production use)
    fixed_installed = "%s/%s" % (INSTALLDIR, fixed_ui_file)
    gtk3_installed = "%s/%s" % (INSTALLDIR, gtk3_ui_file)
    ui_installed = "%s/%s" % (INSTALLDIR, ui_file)
    
    if os.path.exists(fixed_installed):
        gladepath = fixed_installed
    elif os.path.exists(gtk3_installed):
        gladepath = gtk3_installed
    elif os.path.exists(ui_installed):
        gladepath = ui_installed
    # Fall back to current directory (for development use)
    elif os.path.exists(fixed_ui_file):
        gladepath = fixed_ui_file
    elif os.path.exists(gtk3_ui_file):
        gladepath = gtk3_ui_file
    elif os.path.exists(ui_file):
        gladepath = ui_file
    else:
        raise FileNotFoundError(f"No UI file found: {fixed_ui_file}, {gtk3_ui_file}, or {ui_file}")

    glade_xml = Gtk.Builder()
    glade_xml.set_translation_domain(PROGNAME)
    
    try:
        # Try to load the file directly
        glade_xml.add_from_file(gladepath)
        if gladepath.endswith('_fixed.ui'):
            print(f"Loaded complete GTK+ 3 compatible UI file: {gladepath}")
        elif gladepath.endswith('_gtk3.ui'):
            print(f"Loaded GTK+ 3 compatible UI file: {gladepath}")
        elif gladepath.endswith('.ui'):
            print(f"Loaded GTK+ 3 UI file: {gladepath}")
        else:
            print(f"Loaded Glade file: {gladepath}")
            
    except Exception as e:
        print(f"Error loading UI file {gladepath}: {e}")
        raise
    
    return glade_xml
                                                                                
def runFullGUI():
    glade_xml = initGlade()
    Gtk.Window.set_default_icon_from_file(INSTALLDIR + '/pixmaps/lv_icon.png')
    app = glade_xml.get_object('window1')
    app.set_icon_from_file(INSTALLDIR + '/pixmaps/lv_icon.png')
    blvm = baselvm(glade_xml, app)
    app.show()
    app.connect("destroy", lambda w: Gtk.main_quit())
    Gtk.main()
                                                                                
                                                                                
if __name__ == "__main__":
    cmdline = sys.argv[1:]
    sys.argv = sys.argv[:1]
                                                                                

    if os.getuid() != 0:
        print(_("Please restart %s with root permissions!") % (sys.argv[0]))
        sys.exit(10)

    runFullGUI()

