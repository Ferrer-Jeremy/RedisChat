# -*- coding: utf-8 -*-
import redis


class RedisServer():
    """Connect, deconnect subscribe, unsucribe, send message , get messages"""
    #We need to create 2 instances of StrictRedis because we cannot subscribe to a channel and send a message to a channel at the same time

    def __init__(self):
        self.ipServer = ""
        self.port = ""
        self.isConnected = False
        self.isOnChannel = False

    def connect(self, host, port, name):
        """Connect to a server"""

        # catch if the field were properly filled
        try:
            self.redisSender = redis.StrictRedis(host=host, port=port, db=0)
            self.redisReceiver = redis.StrictRedis(host=host, port=port, db=0)
            self.pubsub = self.redisReceiver.pubsub()
        except Exception as ex:  # if the details are not good eg: port: eghfyef
            print(ex)
            return False

        # send a request to the server for testing if the details are right (redis doesn't connect you until you send a request)
        try:
            self.redisSender.get(None)  # getting None returns None or throws an exception if you are not connected
        except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError) as ex:
            print(ex)
            self.isConnected = False
            return False

        # Set the name of the connection on the server
        self.redisSender.client_setname(name)
        print("Connected to : " + host + ":" + port + " as " + name)
        self.isConnected = True
        return True

    def deconnect(self):
        """Deconnect from the server"""

        print("Try to deconnect : " + str(self.redisSender.execute_command("QUIT")))
        self.redisSender = None
        self.isConnected = False

    def connectToChannel(self, channel):
        """Subscribe to a channel"""

        self.pubsub.subscribe(channel)
        print("Subscribe to channel : " + channel)
        self.isOnChannel = True

    def getMessage(self):
        """This method is call by the second thread to get the messages"""

        if self.isConnected and self.isOnChannel:
            message = self.pubsub.get_message()
            if not message is None:
                print("A message was received")
                return(message)
            else:
                return None

    def sendAMessage(self, channel, message):
        """Send a message"""

        self.redisSender.publish(channel, message)
        print("A message was sent on the channel : " + channel)

    def unsubcribe(self, channel):
        """Unsuscribe from a channel"""

        self.redisReceiver.unsubscribe(channel)
        print("Unsubscribe from channel : " + channel)