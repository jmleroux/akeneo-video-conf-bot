#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient

__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class Slack:
    STATUS_OK = 'ok'
    STATUS_SENT = 'sent'
    STATUS_ERROR = 'error'
    STATUS_CHANNELS_RELOAD = 'channels_reload'

    def __init__(self, user_id: str, bot_token: str):
        self.__user_id = user_id
        self.__token = bot_token
        self.__slack_client = SlackClient(self.__token)
        self.__current_status = Slack.STATUS_OK
        self.__last_error = ''
        self.__my_channels = []

    def get_current_status(self):
        return self.__current_status

    def get_last_error(self):
        return self.__last_error

    def my_channels(self):
        return self.__my_channels

    def channels_generator(self):
        """
        Generator method
        Get all channels
        """
        self.__current_status = self.STATUS_CHANNELS_RELOAD
        result = self.__slack_client.api_call(
            "channels.list",
            exclude_archived=1
        )

        if not result['ok']:
            self.__current_status = self.STATUS_ERROR
            self.__last_error = result['error']
            return self.__channels

        self.__channels = []
        for channel in result['channels']:
            yield channel

        self.__current_status = self.STATUS_OK

    def my_channels_generator(self):
        """
        Generator method
        Get channels the user belongs to and store their name and ID in cache
        """
        for channel in self.channels_generator():
            print('Fetching members of channel "{}"'.format(channel['name']))
            members = self.__slack_client.api_call(
                "conversations.members",
                channel=channel['id'],
                limit=200
            )

            if self.__user_id in members['members']:
                channel['members'] = members['members']
                self.__my_channels.append({
                    'channel_id': channel['id'],
                    'channel_name': channel['name'],
                })

            yield channel

    def send_message(self, message: str, channel_id: str):
        """
        Send message to a channel
        :param message: str
        :param channel_id: str Channel ID
        """
        result = self.__slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            as_user=True
        )

        if result['ok']:
            return self.STATUS_SENT
        else:
            self.__last_error = result['error']
            return self.STATUS_ERROR

    def get_channel_messages(self, channel_name: str):
        """
        Generator method
        Get all channel's messages

        :param channel_name: str
        """
        channel_id = self.get_channel_id(channel_name)
        result = self.__slack_client.api_call(
            "channels.history",
            channel=channel_id
        )

        if not result['ok']:
            self.__last_error = result['error']
            return self.STATUS_ERROR

        for message in result['messages']:
            yield message

    def delete_messages(self, channel_name: str):
        """
        Delete all user's messages in a channel
        :param channel_name: str
        :return:
        """
        messages = self.get_channel_messages(channel_name)
        channel_id = self.get_channel_id(channel_name)
        for message in messages:
            if 'user' in message and self.__user_id == message['user']:
                self.__slack_client.api_call(
                    "chat.delete",
                    channel=channel_id,
                    ts=message['ts']
                )

        return self.STATUS_OK

    def get_channel_id(self, channel_name: str):
        """
        Find the channel ID from its name
        :param channel_name:
        :return: str
        """
        channels = self.channels_generator()
        for channel in channels:
            if channel['name'] == channel_name:
                return channel['id']

        return None

    def get_channel_members(self, channel_id: str):
        """
        Find all members in a channel
        :param channel_id:
        :return:
        """
        members = self.__slack_client.api_call(
            "conversations.members",
            channel=channel_id,
            limit=200
        )

        if 'members' in members:
            return members['members']

        return []
