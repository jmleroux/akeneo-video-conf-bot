#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import config as config
from slack import Slack

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def on_close_window(self, *args):
        Gtk.main_quit(*args)

    def on_send(self, button):
        print("Hello World!")

    def send_to_slack(message_field, input_field):
        text = input_field.get()

        slack = Slack(config)
        slack.send_message(text)
        # message_field.config(text='Sent to Slack')
        # input_field.set('')

builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(Handler())

window = builder.get_object("root_window")
window.show_all()

Gtk.main()

# from tkinter import Tk, StringVar, Label, Entry, ttk
# from functools import partial
# from slackclient import SlackClient
# import config as config
#
#
# def send_to_slack(message_field, input_field):
#     text = input_field.get()
#
#     sc = SlackClient(config.BOT_TOKEN)
#
#     sc.api_call(
#         "chat.postMessage",
#         channel=config.VIDEO_CONF_CHANNEL,
#         text=config.MESSAGE_PATTERN % text,
#         as_user=True
#     )
#     message_field.config(text='Sent to Slack')
#     input_field.set('')
#
#
# windowRoot = Tk()
# windowTitle = Label(windowRoot, text='Zoom to Slack')
# message = Label(windowRoot, text='')
# input_box = StringVar(windowRoot)
#
# entry_name = Entry(windowRoot, textvariable=input_box)
# ttk.Style().configure("TButton", padding=1, background="#ccc")
# button = ttk.Button(windowRoot, text='Send', command=partial(send_to_slack, message, input_box))
#
# windowTitle.grid(column=0, row=0)
# entry_name.grid(column=0, row=2)
# message.grid(column=0, row=3)
# button.grid(column=0, row=4)
#
# windowRoot.mainloop()
