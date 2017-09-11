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
            status_bar = builder.get_object("status_bar")
            status_bar.set_property("label", "Empty Zoom ID")


def send_to_slack(zoom_id: str):
    message = "Zoom ID %s sent to channel %s" % (zoom_id, config.VIDEO_CONF_CHANNEL)
    status_bar = builder.get_object("status_bar")

    slack = Slack(config)
    combo_channels = builder.get_object("combo_channels")
    index = combo_channels.get_active()
    model = combo_channels.get_model()
    channel = model[index][0]
    status = slack.send_message(zoom_id, channel)

    if slack.STATUS_SENT == status:
        builder.get_object("status_bar")
        status_bar.set_property("label", message)
    elif slack.STATUS_INVALID_FORMAT == status:
        status_bar.set_property("label", "Invalid Zoom ID")
    else:
        error = slack.get_last_error()
        status_bar.set_property("label", "Error when sending message: %s" % error)


def list_channels():
    slack = Slack(config)
    result = slack.channels_list()
    channels = []
    for channel in result['channels']:
        channels.append("#" + channel['name'])
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
