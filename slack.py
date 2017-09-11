#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient
import re

__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class Slack:
    __token = ''
    __message_pattern = ''
    __target_channel = ''
    __last_error = ''

    STATUS_SENT = 'sent'
    STATUS_INVALID_FORMAT = 'invalid format'
    STATUS_ERROR = 'error'

    def __init__(self, config):
        self.__token = config.BOT_TOKEN
        self.__message_pattern = config.MESSAGE_PATTERN
        self.__target_channel = config.VIDEO_CONF_CHANNEL

    def get_channel(self):
        return self.__target_channel

    def get_last_error(self):
        return self.__last_error

    def send_message(self, message: str, channel: str):

        if not self.is_valid_zoom_id(message):
            return self.STATUS_INVALID_FORMAT

        sc = SlackClient(self.__token)

        result = sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=self.__message_pattern % message,
            as_user=True
        )

        print(result)
        if result['ok']:
            return self.STATUS_SENT
        else:
            self.__last_error = result['error']
            return self.STATUS_ERROR

    def channels_list(self):
        sc = SlackClient(self.__token)

        result = sc.api_call(
            "channels.list",
            exclude_archived=1,
            exclude_members=1
        )

        return result

    @staticmethod
    def is_valid_zoom_id(zoom_id: str):
        match = re.search('^[0-9]{3}-?[0-9]{3}-?[0-9]{3}$', zoom_id, flags=re.IGNORECASE)
        if match is not None:
            return True
        return False
