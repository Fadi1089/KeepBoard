import gi

gi.require_version('Gdk', '4.0')
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import clipboard

# Create a new application
app = Gtk.Application(application_id='linux.Clipboard')
app.connect('activate', lambda app: clipboard.ClipboardWindow(app))

# Run the application
app.run(None)