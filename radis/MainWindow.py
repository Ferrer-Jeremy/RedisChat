#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import gi

from radis.DialogMessage import ConnectionServer, BasicMessage, ConnectionChannel
from radis.RedisServer import RedisServer
from radis.ThreadMessage import MyThread

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    """The main window"""

    def __init__(self):
        Gtk.Window.__init__(self, title="Chat")
        self.set_default_size(500, 450)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.ipServer = ""
        self.port = ""
        self.username = ""
        self.dictTextview = {}

        # Create an instance of redisServer
        self.redisServer = RedisServer()

        # Layout
        self.layoutGrid = Gtk.Grid()

        self.header()  # Add header
        self.tabs()  # Add the channels tab
        self.submit()  # Add the submit box

        self.add(self.layoutGrid)  # Add the base layout

    def header(self):  # Check if my use of Gtk.HeaderBar() is legit
        """The header, toolbar"""
        self.layoutHeaderBar = Gtk.HeaderBar()

        # The buttons with icons
        btnConnectionServer = Gtk.Button(
            None, image=Gtk.Image(stock=Gtk.STOCK_CONNECT))
        btnAddChannel = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_ADD))
        btnDeconnection = Gtk.Button(
            None, image=Gtk.Image(stock=Gtk.STOCK_STOP))

        # The labels & tooltips
        self.layoutHeaderBar.props.title = "Deconnect"
        btnConnectionServer.set_tooltip_text("Connect to a server")
        btnAddChannel.set_tooltip_text("Add a channel in a tab")
        btnDeconnection.set_tooltip_text("Deconnect from the server")

        # The events
        btnConnectionServer.connect("clicked", self.connectToServer)
        btnAddChannel.connect("clicked", self.addAChannel)
        btnDeconnection.connect("clicked", self.deconnection)

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
        textview.set_cursor_visible(False)
        # textview.set_wrap_mode()

        # Add
        page.add(textview)
        self.dictTextview['Default'] = textview
        self.notebook.append_page(page, Gtk.Label('Default'))
        self.layoutGrid.attach(self.notebook, 0, 1, 4, 1)

    def submit(self):
        """The submit box"""

        # The button
        btnSubmitText = Gtk.Button("Submit")
        # With this the focus stay on the input
        btnSubmitText.set_focus_on_click(False)
        # The input
        self.entrySubmit = Gtk.Entry()
        self.entrySubmit.set_placeholder_text("Type your message here")

        # The events
        btnSubmitText.connect("clicked", self.sendMessage)
        self.entrySubmit.connect("activate", self.sendMessage)

        # Add
        self.layoutGrid.attach(self.entrySubmit, 0, 2, 2, 1)
        self.layoutGrid.attach(btnSubmitText, 2, 2, 2, 1)

    def updateTextview(self, channel, username, text):
        """Update the text when we send a message or receive one"""

        textFormat = username + " : " + text + "\n"
        textview = self.dictTextview[channel]
        # We get the textbuffer
        textbuffer = textview.get_buffer()
        # Position the iterator at the end of the buffer
        bufferIterator = textbuffer.get_end_iter()
        # Insert text at the position of the iterator
        textbuffer.insert(bufferIterator, textFormat, len(textFormat))

    # The differents events of the buttons
    def sendMessage(self, widget):
        """Send a message to the active tab"""

        # we get the name of the tab
        nbPage = self.notebook.get_current_page()
        tab = self.notebook.get_nth_page(nbPage)
        channel = self.notebook.get_tab_label_text(tab)
        # We get the text to send
        text = self.username + "§" + self.entrySubmit.get_text()
        # If we're connected and there is something to send'
        if not text == "" and self.redisServer.isConnected and text is not None:
            # We send a msg and reset the field
            self.redisServer.sendAMessage(channel, text)
            self.entrySubmit.set_text("")

    def connectToServer(self, widget):
        """Show a dialog where the user add details of the server"""

        dialogConnection = ConnectionServer(
            self, self.ipServer, self.port, self.username)
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
                isConnect = self.redisServer.connect(
                    self.ipServer, self.port, self.username)
                # If error connect
                if isConnect:
                    self.layoutHeaderBar.props.title = "Connected to : " + \
                        self.ipServer + ":" + self.port + " as " + self.username
                    # Create a new thread
                    self.startThread()
                else:
                    BasicMessage(self, Gtk.MessageType.ERROR, "Error",
                                 "Connection impossible. Verify your connection details")
            else:
                # If the entries aren't full
                # show a error message
                BasicMessage(self, Gtk.MessageType.ERROR,
                             "Error", "You must fill the details")

        # at the end we destroy the dialogelse the user press cancel ot the red
        # cross
        dialogConnection.destroy()

    def addAChannel(self, widget):
        """Show a dialog where the user can add a channel"""

        # If we're connected
        if self.redisServer.isConnected:
            # lunch the dialog
            dialogChannel = ConnectionChannel(self)
            response = dialogChannel.run()
            channel = dialogChannel.entryChannel.get_text()

            # if ok was pressed
            if response == Gtk.ResponseType.OK:
                # if the field wasn't empty
                if not channel == "":
                    # Add the channel
                    self.redisServer.connectToChannel(channel)
                    self.addATab(channel)
                else:
                    BasicMessage(self, Gtk.MessageType.INFO, "Error",
                                 "You must enter the name of the channel")
                # else nclose the dialog
                dialogChannel.destroy()
        else:
            # else show error
            BasicMessage(self, Gtk.MessageType.ERROR,
                         "Error", "Your are not Connected")

    def addATab(self, name):
        """Add a tab"""

        # Scrollable container
        page = Gtk.ScrolledWindow()
        page.set_hexpand(True)
        page.set_vexpand(True)

        # Textview
        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        # textview.set_wrap_mode()

        # Add
        page.add(textview)
        self.dictTextview[name] = textview
        self.notebook.append_page(page, Gtk.Label(name))
        self.notebook.show_all()
        print("A channel was added : " + name)

    def deconnection(self, widget):
        """Deconnect from the server and show a dialog"""

        # if we're connected
        if self.redisServer.isConnected:
            # we deconnect, set the title to deconect and stop the thread
            self.redisServer.deconnect()
            self.layoutHeaderBar.props.title = "Deconnect"
            self.stopThread()
            BasicMessage(self, Gtk.MessageType.INFO,
                         "Error", "You are now deconnected")
        else:
            BasicMessage(self, Gtk.MessageType.ERROR,
                         "Error", "You are not connected")

    def removeChannel(self):
        """Remove a tab and unsubscribe of this channel"""

    def startThread(self):
        """Lauch multi thread"""

        self.thread1 = MyThread(self)
        self.thread1.start()

    def stopThread(self):
        """Stop the multi thread"""

        # If the thread doesn't exist throw an error
        try:
            self.thread1.loop = False
        except Exception as ex:
            print("Try to stop a thread that doesn't exist ?? NICE !!!!'" + str(ex))

    def stopMain(self, widget, event, data=None):
        """Replace the parent method to close the thread befor closing"""
        self.stopThread()
        Gtk.main_quit()


win = MyWindow()
win.connect("delete-event", win.stopMain)
win.show_all()
Gtk.main()
