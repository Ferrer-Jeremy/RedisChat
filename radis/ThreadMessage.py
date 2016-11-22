# -*- coding: utf-8 -*-
import threading
import time


class MyThread (threading.Thread):
    """The second thread to get the messages"""

    def __init__(self, mainWindow):
        super(MyThread, self).__init__()
        self.mainWindow = mainWindow
        self.loop = True

    def run(self):
        print("Starting Thread for scan messages")
        while(self.loop):
            time.sleep(1)
            data = self.mainWindow.redisServer.getMessage()
            if not data is None:
                channel = data['channel'].decode("utf-8")
                try:  # if you subscribe to a channel data return an int
                    messageRaw = data['data'].decode("utf-8").split("§")
                    username = messageRaw[0]
                    message = messageRaw[1]
                    self.mainWindow.updateTextview(channel, username, message)
                # throw an exception if data[channel] isn't a binary string'
                except Exception as ex:
                    print(ex)
        print("Exiting Thread for scan messages")
