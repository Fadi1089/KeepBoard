import gi

gi.require_version('Gdk', '4.0')
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib


class ClipboardWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title='KeepBoard') # title of the window
        self.set_default_size(800, 400)
        self.clipboard_items = []  # List to self.store clipboard history

        # Create a ScrolledWindow to hold the ListBox
        # the set_child method is called to append a widget to the window or to another widget
        scrolled_window = Gtk.ScrolledWindow()
        self.set_child(scrolled_window)

        # Create a ListBox to show the clipboard history and add it to the window
        self.list_box = Gtk.ListBox()
        scrolled_window.set_child(self.list_box)

        self.display = Gdk.Display.get_default() # Create the display 
        self.clipboard = self.display.get_clipboard() # the clipboard object
        self.clipboard.connect("changed", self._on_clipboard_changed) # connecting the clipboard object to trigger a function upon receiving the "changed" signal

        # Initial formats (for demonstration)
        self.formats = self.clipboard.get_formats()

        self.present()

    def _on_clipboard_changed(self, _clipboard):
        self.clipboard.read_text_async(None, self.__on_text_read)

    def __on_text_read(self, clipboard, result):
        try:
            text = clipboard.read_text_finish(result)
        except Exception as e:
            print(f"Error reading clipboard: {e}")
            return

        if text and text not in self.clipboard_items:
            # Truncate long text for display
            display_text = text[:100] + "..." if len(text) > 100 else text
            
            #debugging and appending to the list
            print(f"Clipboard changed to: {display_text}")
            self.clipboard_items.append(text)

            # Schedule UI update on main thread
            GLib.idle_add(self._add_clipboard_item, text, display_text)

    def _add_clipboard_item(self, full_text, display_text):
        """Add a clipboard item to the UI (runs on main thread)"""
        # Creating and adding the widget to the list_box
        box = Gtk.Box(spacing=6, homogeneous=True)
        self.list_box.append(box)
        
        button_copy_text = Gtk.Button(label=display_text)
        # Fix lambda closure by capturing full_text in closure
        button_copy_text.connect('clicked', lambda btn, text=full_text: self._copy_to_clipboard(text))
        box.append(button_copy_text)
        
        return False  # Don't repeat this idle function

    def _copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.clipboard.set(text)