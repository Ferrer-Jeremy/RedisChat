# -*- coding: utf-8 -*-
import redis
import time

# TODO connection exception


class RedisServer():

    def __init__(self):
        self.ipServer = ""
        self.port = ""
        self.isConnected = False
        self.isOnChannel = False

    def connect(self, host, port):
        self.redisSender = redis.StrictRedis(host=host, port=port, db=0)
        self.redisReceiver = redis.StrictRedis(host=host, port=port, db=0)
        self.pubsub = self.redisReceiver.pubsub()
        self.isConnected = True

    def deconnect(self):
        self.redis.close()
        self.isConnected = False

    def connectToChannel(self, nameChannel):
        self.pubsub.subscribe(nameChannel)

    def getMessage(self):
        time.sleep(1)
        if self.isConnected and self.isOnChannel:
            message = self.pubsub.get_message()
            if not message is None:
                # Work on the string before return
                return(message['data'])

    def sendAMessage(self, channel, username, message):
        self.redisSender.publish(channel, username + " : " + message)

    def unsubcribe(self):
        """"""
