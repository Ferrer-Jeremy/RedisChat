#!/usr/bin/python
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from DialogMessage import BasicMessage, ConnectionServer, ConnectionChannel
from RedisServer import RedisServer
import _thread
import redis


class MyWindow(Gtk.Window):
    """The main window"""

    def __init__(self):
        Gtk.Window.__init__(self, title="Chat")
        self.set_default_size(500, 450)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.ipServer = ""
        self.port = ""
        self.username = ""

        # Create an instance of redisServer
        self.redisServer = RedisServer()

        # Layout
        self.layoutGrid = Gtk.Grid()

        self.header()  # Add header
        self.tabs()  # Add the channels tab
        self.Submit()  # Add the submit box

        self.add(self.layoutGrid)  # Add the base layout

    def header(self):  # Check if my use of Gtk.HeaderBar() id legit
        """The header, toolbar"""
        self.layoutHeaderBar = Gtk.HeaderBar()

        # The buttons with icons
        btnConnectionServer = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_CONNECT))
        btnAddChannel = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ADD))
        btnDeconnection = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_STOP))

        # The labels & tooltips
        self.layoutHeaderBar.props.title = "Deconnect"
        btnConnectionServer.set_tooltip_text("Connect to a server")
        btnAddChannel.set_tooltip_text("Add a channel in a tab")
        btnDeconnection.set_tooltip_text("Deconnect from the server")

        # The events
        btnConnectionServer.connect("clicked", self.connectToServer)
        btnAddChannel.connect("clicked", self.addAChannel)

        # Add
        self.layoutHeaderBar.add(btnConnectionServer)
        self.layoutHeaderBar.add(btnAddChannel)
        self.layoutHeaderBar.pack_end(btnDeconnection)
        self.layoutGrid.attach(self.layoutHeaderBar, 0, 0, 4, 1)

    def tabs(self):
        """The tabs with inside the text area"""

        # Container of tabs
        self.notebook = Gtk.Notebook()

        # Scrollable container
        page = Gtk.ScrolledWindow()
        page.set_hexpand(True)
        page.set_vexpand(True)

        # Textview
        textview = Gtk.TextView()
        textview.set_editable(False)

        # Add
        page.add(textview)
        self.notebook.append_page(page, Gtk.Label('Default'))
        self.layoutGrid.attach(self.notebook, 0, 1, 4, 1)

    def Submit(self):
        """The submit box"""

        # The button
        btnSubmitText = Gtk.Button("Submit")
        btnSubmitText.set_focus_on_click(False)  # With this the focus stay on the input
        # The input
        entrySubmit = Gtk.Entry()
        entrySubmit.set_placeholder_text("Type your message here")

        # The events
        btnSubmitText.connect("clicked", self.sendMessage, entrySubmit.get_text())

        # Add
        self.layoutGrid.attach(entrySubmit, 0, 2, 2, 1)
        self.layoutGrid.attach(btnSubmitText, 2, 2, 2, 1)

    # The differents events of the buttons
    def sendMessage(self, widget, text):
        """Send a message to the channel select"""

        BasicMessage(self, Gtk.MessageType.INFO, "Titre", "tu as cliqué")

    def connectToServer(self, widget):
        """Show a dialog where the user add info of the server"""

        dialogConnection = ConnectionServer(self, self.ipServer, self.port, self.username)
        response = dialogConnection.run()

        if response == Gtk.ResponseType.OK:
            # Button Ok pressed
            # Try to connect to the server
            self.ipServer = dialogConnection.entryIp.get_text()
            self.port = dialogConnection.entryPort.get_text()
            self.username = dialogConnection.entryUser.get_text()

            # Test if inputs are filled
            if not self.ipServer == "" and not self.port == ""and not self.username == "":
                # If the entries are full
                # Try to Connect to the server
                self.redisServer.connect(self.ipServer, self.port)
                # TODO test if error connect
                ####
                self.layoutHeaderBar.props.title = "Connected to : " + self.ipServer + ":" + self.port + " as " + self.username
                #Create a new thread
                try:
                    _thread.start_new_thread(self.redisServer.getMessage, ())
                except:
                    print("Error: unable to start thread")
            else:
                # If the entries aren't full
                #show a error message
                BasicMessage(self, Gtk.MessageType.INFO, "Error", "You must fill the inputs")

        #else nothing
        dialogConnection.destroy()

    def addAChannel(self, widget):
        """Show a dialog where the user can add a channel"""

        dialogChannel = ConnectionChannel(self)
        response = dialogChannel.run()
        channel = dialogChannel.entryChannel.get_text()

        if response == Gtk.ResponseType.OK:
            if not channel == "":
                if self.redisServer.isConnected:
                    # Add the channel
                    #self.redisServer.connectToChannel(channel)
                    self.addATab(channel)
                else:
                    BasicMessage(self, Gtk.MessageType.INFO, "Error", "Your are not Connected")

            else:
                # Show Error
                BasicMessage(self, Gtk.MessageType.INFO, "Error", "You must enter the name of the channel")

        #else nothing
        dialogChannel.destroy()

    def addATab(self, name):
        """Add a tab"""

        # Scrollable container
        page = Gtk.ScrolledWindow()
        page.set_hexpand(True)
        page.set_vexpand(True)

        # Textview
        textview = Gtk.TextView()
        textview.set_editable(False)

        # Add
        page.add(textview)
        self.notebook.append_page(page, Gtk.Label(name))
        self.notebook.show_all()
        print(self.notebook.get_n_pages())  # to know the number of pages

    def deconnection(self, widget):
        """Deconnect from the server and show a dialog"""


    def removeChannel(self):
        """Remove a tab"""


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
help(redis)
