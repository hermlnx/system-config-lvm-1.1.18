
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class WaitMsg:
    
    def __init__(self, message):
        self.displayed = False
        self.msg = message
    
    def show(self):
        self.dlg = Gtk.MessageDialog(None, 0,
                                     Gtk.MessageType.INFO, Gtk.ButtonsType.NONE, 
                                     self.msg)
        self.dlg.set_modal(True)
        self.dlg.show_now()
        self.displayed = True
        
        # change cursor
        cursor = Gdk.Cursor.new(Gdk.CursorType.WATCH)
        self.dlg.get_root_window().set_cursor(cursor)
        
        self.refresh()
        self.refresh()
        self.refresh()
    
    def hide(self):
        if self.displayed:
            self.dlg.destroy()
            self.displayed = False
            
            # revert cursor
            cursor = Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR)
            self.dlg.get_root_window().set_cursor(cursor)
            
        self.refresh()
    
    def refresh(self):
        while Gtk.events_pending():
            Gtk.main_iteration()
