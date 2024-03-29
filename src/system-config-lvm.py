#!/usr/bin/python2

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
INSTALLDIR="/usr/share/system-config-lvm"
VERSION = "@VERSION@"

### gettext ("_") must come before import gtk ###
import gettext
gettext.bindtextdomain(PROGNAME, "/usr/share/locale")
gettext.textdomain(PROGNAME)
try:
    gettext.install(PROGNAME, "/usr/share/locale", 1)
except IOError:
    import __builtin__
    __builtin__.__dict__['_'] = unicode
                                                                                

### gettext first, then import gtk (exception prints gettext "_") ###
try:
    import gtk
    import gtk.glade
except RuntimeError, e:
    print _("""
  Unable to initialize graphical environment. Most likely cause of failure
  is that the tool was not run using a graphical environment. Please either
  start your graphical user interface or set your DISPLAY variable.
                                                                                
  Caught exception: %s
""") % e
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
            dlg = gtk.MessageDialog(None, 0,
                                    gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                    msg)
            dlg.run()
            sys.exit(10)

    
    #Need to suppress the spewing of file descriptor errors to terminal
    os.environ["LVM_SUPPRESS_FD_WARNINGS"] = "1"

    self.lvmm = lvm_model()
                                                                                
    self.main_win = app
    self.glade_xml = glade_xml

    self.volume_tab_view = Volume_Tab_View(glade_xml, self.lvmm, self.main_win)

    self.glade_xml.signal_autoconnect(
      {
        "on_quit1_activate" : self.quit,
        "on_about1_activate" : self.on_about,
        "on_reload_lvm_activate" : self.on_reload
      }
    )
                                                                                
  def on_about(self, *args):
       dialog = gtk.MessageDialog(None, 0,
                                    gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                                    "This software is licensed under the terms of the GPL. Copyright (c) 2004 Red Hat, Inc. All rights reserved.")
       dialog.run()
       dialog.destroy()
        
  
  def on_reload(self, *args):
      self.volume_tab_view.reset_tree_model()
  
  def quit(self, *args):
      gtk.main_quit()



#############################################################
def initGlade():
    gladepath = "lvui.glade"
    if not os.path.exists(gladepath):
      gladepath = "%s/%s" % (INSTALLDIR,gladepath)

    gtk.glade.bindtextdomain(PROGNAME)
    glade_xml = gtk.glade.XML (gladepath, domain=PROGNAME)
    return glade_xml
                                                                                
def runFullGUI():
    glade_xml = initGlade()
    gtk.window_set_default_icon_from_file(INSTALLDIR + '/pixmaps/lv_icon.png')
    app = glade_xml.get_widget('window1')
    app.set_icon_from_file(INSTALLDIR + '/pixmaps/lv_icon.png')
    blvm = baselvm(glade_xml, app)
    app.show()
    app.connect("destroy", lambda w: gtk.main_quit())
    gtk.main()
                                                                                
                                                                                
if __name__ == "__main__":
    cmdline = sys.argv[1:]
    sys.argv = sys.argv[:1]
                                                                                

    if os.getuid() != 0:
        print _("Please restart %s with root permissions!") % (sys.argv[0])
        sys.exit(10)

    runFullGUI()

