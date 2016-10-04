# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# Design patern singelton ??

class BasicMessage(Gtk.Dialog):
    """Show all the dialogs"""

    def __init__(self, parent, typeDialog, title, text):
        """Create a dialog

        typeDialog include :
        -Gtk.MessageType.INFO
        -Gtk.MessageType.ERROR
        -Gtk.MessageType.WARNING
        -Gtk.MessageType.QUESTION"""

        dialog = Gtk.MessageDialog(parent, 0, typeDialog, Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(text)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("WARN dialog closed by clicking OK button")
        elif response == Gtk.ResponseType.CANCEL:
            print("WARN dialog closed by clicking CANCEL button")

        dialog.destroy()


class ConnectionServer(Gtk.Dialog):
    """Window for connecting to the server"""

    def __init__(self, parent, ip, port, username):
        Gtk.Dialog.__init__(self, "Connect to Server", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        # The label
        lblInstruction = Gtk.Label("Enter the adress of the server")
        lblIp = Gtk.Label("Adress Ip : ")
        lblPort = Gtk.Label("Port (Default : 6379) : ")
        lblUser = Gtk.Label("Your Name on the Server : ")

        # The entry
        self.entryIp = Gtk.Entry()
        self.entryIp.set_text(ip)
        self.entryIp.set_placeholder_text("123.255.123.123")
        self.entryIp.set_max_length(15)
        self.entryPort = Gtk.Entry()
        self.entryPort.set_text(port)
        self.entryPort.set_placeholder_text("6379")
        self.entryPort.set_max_length(5)
        self.entryUser = Gtk.Entry()
        self.entryUser.set_text(username)
        self.entryUser.set_placeholder_text("Peter")
        self.entryUser.set_max_length(20)

        # Layout
        layoutGrid = Gtk.Grid()
        box = self.get_content_area()
        box.add(layoutGrid)

        # Add to the base layout
        layoutGrid.attach(lblInstruction, 0, 0, 1, 1)
        layoutGrid.attach(lblIp, 0, 1, 1, 1)
        layoutGrid.attach(self.entryIp, 1, 1, 1, 1)
        layoutGrid.attach(lblPort, 0, 2, 1, 1)
        layoutGrid.attach(self.entryPort, 1, 2, 1, 1)
        layoutGrid.attach(lblUser, 0, 3, 1, 1)
        layoutGrid.attach(self.entryUser, 1, 3, 1, 1)

        self.show_all()


class ConnectionChannel(Gtk.Dialog):
    """Window for connecting to a channel"""

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Connect to a Channel", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        # The label
        lblChannel = Gtk.Label("Channel Name :")

        # The entry
        self.entryChannel = Gtk.Entry()
        self.entryChannel.set_placeholder_text("chat")
        self.entryChannel.set_max_length(15)

        # Layout
        layoutGrid = Gtk.Grid()
        box = self.get_content_area()
        box.add(layoutGrid)

        # Add to the base layout
        layoutGrid.attach(lblChannel, 0, 0, 1, 1)
        layoutGrid.attach(self.entryChannel, 1, 0, 1, 1)

        self.show_all()
