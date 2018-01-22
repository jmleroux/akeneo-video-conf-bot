#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient

__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class Slack:

    STATUS_OK = 'ok'
    STATUS_SENT = 'sent'
    STATUS_ERROR = 'error'

    __user_id = ''
    __token = ''
    __last_error = ''
    __slack_client = None
    __channels = []

    def __init__(self, user_id: str, bot_token: str):
        self.__user_id = user_id
        self.__token = bot_token
        self.__slack_client = SlackClient(self.__token)

    def get_last_error(self):
        return self.__last_error

    def get_my_channels(self):

        if not self.__channels:
            result = self.__slack_client.api_call(
                "channels.list",
                exclude_archived=1
            )

            if not result['ok']:
                self.__last_error = result['error']
                return self.__channels

            self.__channels = []
            for channel in result['channels']:
                if self.__user_id in channel['members']:
                    self.__channels.append(channel)

        return self.__channels

    def send_message(self, message: str, channel: str):
        result = self.__slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=message,
            as_user=True
        )

        if result['ok']:
            return self.STATUS_SENT
        else:
            self.__last_error = result['error']
            return self.STATUS_ERROR

    def get_channel_messages(self, channel_name: str):
        channel_id = self.get_channel_id(channel_name)
        result = self.__slack_client.api_call(
            "channels.history",
            channel=channel_id
        )

        if not result['ok']:
            self.__last_error = result['error']
            return self.STATUS_ERROR

        messages = []
        for message in result['messages']:
            messages.append(message)

        return messages

    def delete_messages(self, channel: str):
        messages = self.get_channel_messages(channel)
        channel_id = self.get_channel_id(channel)
        for message in messages:
            if self.__user_id == message['user']:
                self.__slack_client.api_call(
                    "chat.delete",
                    channel=channel_id,
                    ts=message['ts']
                )

        return self.STATUS_OK

    def get_channel_id(self, channel_name: str):
        channels = self.get_my_channels()
        for channel in channels:
            if self.__user_id in channel['members'] and channel['name'] == channel_name:
                return channel['id']

        return None
