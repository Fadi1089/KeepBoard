import sys, time, subprocess, threading
import gi

gi.require_version('Gdk', '4.0')
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib

class ClipboardWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title='Clipboard') # title of the window
        self.set_default_size(300, 400)
        
        self.clipboard_items = []  # List to self.store clipboard history
        self.last_item = None  # Track last clipboard item

        # Create a ScrolledWindow to hold the ListBox
        scrolled_window = Gtk.ScrolledWindow()
        self.set_child(scrolled_window)

        # Create a ListBox to show the clipboard history and add it to the window
        self.list_box = Gtk.ListBox()
        scrolled_window.set_child(self.list_box)

        self.display = Gdk.Display.get_default() # Create the display 
        self.clipboard = self.display.get_clipboard() # the clipboard object
        self.clipboard.connect("changed", self.on_clipboard_changed) # connecting the clipboard object to trigger a function upon receiving the "changed" signal

        # Initial formats (for demonstration)
        self.formats = self.clipboard.get_formats()

        # (debugging) adding text options to the ListStore for display
        # for name in ["Benjamin", "Charles", "Alfred", "David", "charles", "david", "benjamin"]:
        #     self.list_box.append(name)
            
        # initial clipbpoard check
        self.on_clipboard_changed(self.clipboard)

        self.present()
        

    def on_clipboard_changed(self, clipboard):
        self.clipboard.read_text_async(None, self.on_text_read)

    def on_text_read(self, clipboard, result):

        text = clipboard.read_text_finish(result)

        if text and text != self.last_item and text not in self.clipboard_items:
            print(f"Clipboard changed to: {text}")
            self.last_item = text
            self.clipboard_items.append(text)

            # Creating and adding the widget to the list_box
            box = Gtk.Box(spacing=6, homogeneous=True)
            self.list_box.append(box)
            entry = Gtk.Entry()
            entry.set_text(text)
            box.append(entry)
            button_copy_text = Gtk.Button(label='Copy Text')
            button_copy_text.connect('clicked', lambda copy: self.clipboard.set(entry.get_text()))
            box.append(button_copy_text)
            
def on_activate(app):
    win = ClipboardWindow(app)

# Create a new application
app = Gtk.Application(application_id='linux.Clipboard')
app.connect('activate', on_activate)

# Run the application
app.run(None)