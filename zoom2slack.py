#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import gi
import config as config
from slack import Slack

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class Handler:
    @staticmethod
    def on_close_window(*args):
        os.remove(lock_file)
        Gtk.main_quit(*args)

    @staticmethod
    def on_send(button):
        input_field = builder.get_object("input_field")
        zoom_id = input_field.get_property("text")

        if '' != zoom_id:
            send_to_slack(zoom_id)
        else:
            set_status_bar_message("Empty Zoom ID")


def get_selected_channel():
    combo_channels = builder.get_object("combo_channels")
    index = combo_channels.get_active()
    model = combo_channels.get_model()
    return model[index][0]


def set_status_bar_message(message: str):
    status_bar = builder.get_object("status_bar")
    status_bar.set_property("label", message)


def send_to_slack(zoom_id: str):
    channel = get_selected_channel()

    slack = Slack(config)
    status = slack.send_message(zoom_id, channel)

    if slack.STATUS_SENT == status:
        message = "Zoom ID %s sent to channel %s" % (zoom_id, channel)
    elif slack.STATUS_INVALID_FORMAT == status:
        message = "Invalid Zoom ID"
    else:
        error = slack.get_last_error()
        message = "Error when sending message: %s" % error

    set_status_bar_message(message)


def list_channels():
    slack = Slack(config)
    channels = slack.get_my_channels()
    return channels


def build_channels_combo():
    combo_channels = builder.get_object("combo_channels")
    name_store = builder.get_object("store_channels")
    active_index = 0
    for key, channel_name in enumerate(list_channels()):
        name_store.append([channel_name])
        if config.VIDEO_CONF_CHANNEL == channel_name:
            active_index = key

    combo_channels.set_active(active_index)


lock_file = "var/zoom2slack.run"
if os.path.isfile(lock_file):
    print("Instance already running")
    exit(0)
else:
    lock_handle = open(lock_file, 'w')
    lock_handle.write('1')
    lock_handle.close()

builder = Gtk.Builder()
builder.add_from_file("ui.glade")
build_channels_combo()
builder.connect_signals(Handler())

window = builder.get_object("root_window")
window.show_all()

Gtk.main()
