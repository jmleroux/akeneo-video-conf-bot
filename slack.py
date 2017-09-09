#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient


class Slack:
    __token = ''
    __message_pattern = ''
    __target_channel = ''

    def __init__(self, config):
        self.__token = config.BOT_TOKEN
        self.__message_pattern = config.MESSAGE_PATTERN
        self.__target_channel = config.VIDEO_CONF_CHANNEL

    def send_message(self, message):
        sc = SlackClient(self.__token)

        sc.api_call(
            "chat.postMessage",
            channel=self.__target_channel,
            text=self.__message_pattern % message,
            as_user=True
        )
