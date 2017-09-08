#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Tk, StringVar, Label, Entry, ttk
from functools import partial
from slackclient import SlackClient
import re
import config as config


def send_to_slack(message_field, input_field):
    text = input_field.get()
    if valid_zoom_id(text=text):
        post_to_slack(text)
        message_field.config(text='Sent to Slack')
        input_field.set('')
    else:
        message_field.config(text='Invalid format')


def valid_zoom_id(text):
    match = re.search('^[0-9]{3}-?[0-9]{3}-?[0-9]{3}$', text, flags=re.IGNORECASE)
    if match is not None:
        return True
    return False


def post_to_slack(text):
    sc = SlackClient(config.BOT_TOKEN)
    sc.api_call(
        "chat.postMessage",
        channel=config.VIDEO_CONF_CHANNEL,
        text=config.MESSAGE_PATTERN % text,
        as_user=True
    )


windowRoot = Tk()
windowTitle = Label(windowRoot, text='Zoom to Slack')
message = Label(windowRoot, text='')
input_box = StringVar(windowRoot)

entry_name = Entry(windowRoot, textvariable=input_box)
ttk.Style().configure("TButton", padding=1, background="#ccc")
button = ttk.Button(windowRoot, text='Send', command=partial(send_to_slack, message, input_box))

windowTitle.grid(column=0, row=0)
entry_name.grid(column=0, row=2)
message.grid(column=0, row=3)
button.grid(column=0, row=4)

windowRoot.mainloop()
