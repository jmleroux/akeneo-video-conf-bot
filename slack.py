#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient
import re


class Slack:
    __token = ''
    __message_pattern = ''
    __target_channel = ''

    STATUS_SENT = 'sent'
    STATUS_INVALID_FORMAT = 'invalid format'
    STATUS_ERROR = 'error'

    def __init__(self, config):
        self.__token = config.BOT_TOKEN
        self.__message_pattern = config.MESSAGE_PATTERN
        self.__target_channel = config.VIDEO_CONF_CHANNEL

    def get_channel(self):
        return self.__target_channel

    def send_message(self, message: str):

        if not self.is_valid_zoom_id(message):
            return self.STATUS_INVALID_FORMAT

        sc = SlackClient(self.__token)

        sc.api_call(
            "chat.postMessage",
            channel=self.__target_channel,
            text=self.__message_pattern % message,
            as_user=True
        )

        return self.STATUS_SENT

    @staticmethod
    def is_valid_zoom_id(zoom_id: str):
        match = re.search('^[0-9]{3}-?[0-9]{3}-?[0-9]{3}$', zoom_id, flags=re.IGNORECASE)
        if match is not None:
            return True
        return False
