import gi

gi.require_version('Gdk', '4.0')
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from clipboard import ClipboardWindow

# Create a new application
app = Gtk.Application(application_id='linux.Clipboard')
app.connect('activate', lambda app: ClipboardWindow(app))

# Run the application
if __name__ == '__main__':
    app.run(None)