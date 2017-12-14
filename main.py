#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        Gtk.main_quit(*args)

    @staticmethod
    def on_send(button):
        send_to_slack()

    @staticmethod
    def on_delete_messages(button):
        delete_messages()


def get_selected_channel():
    combo_channels = builder.get_object("combo_channels")
    index = combo_channels.get_active()
    model = combo_channels.get_model()
    return model[index][0]


def set_status_bar_message(message: str):
    status_bar = builder.get_object("status_bar")
    status_bar.set_property("label", message)


def delete_messages():
    channel = get_selected_channel()

    slack = Slack(config)
    status = slack.delete_messages(channel)

    if slack.STATUS_OK == status:
        message = "Messages deleted from channel %s" % channel
    else:
        error = slack.get_last_error()
        message = "Error when deleting messages: %s" % error

    set_status_bar_message(message)


def send_to_slack():
    input_field = builder.get_object("input_field")
    zoom_id = input_field.get_property("text")

    channel = get_selected_channel()

    slack = Slack(config)

    if not zoom_id:
        message = "Empty Zoom ID"
    elif not is_valid_input(zoom_id):
        message = "Invalid Zoom ID"
    else:
        status = slack.send_message(zoom_id, channel)

        if slack.STATUS_SENT == status:
            message = "Zoom ID %s sent to channel %s" % (zoom_id, channel)
            reset_input()
        else:
            error = slack.get_last_error()
            message = "Error when sending message: %s" % error

    set_status_bar_message(message)


def is_valid_input(zoom_id: str):
    if not zoom_id:
        return False

    return True
    # match = re.search('^[0-9]{3}-?[0-9]{3}-?[0-9]{3}$', zoom_id, flags=re.IGNORECASE)
    # return match is not None


def reset_input():
    input_field = builder.get_object("input_field")
    input_field.set_text("")


def list_channels():
    slack = Slack(config)
    channels = slack.get_my_channels()
    return channels


def build_channels_combo():
    combo_channels = builder.get_object("combo_channels")
    name_store = builder.get_object("store_channels")
    active_index = 0
    for key, channel in enumerate(list_channels()):
        name_store.append([
            channel['name']
        ])
        if config.VIDEO_CONF_CHANNEL == channel['name']:
            active_index = key

    combo_channels.set_active(active_index)


builder = Gtk.Builder()
builder.add_from_file("ui.glade")
build_channels_combo()
builder.connect_signals(Handler())

window = builder.get_object("root_window")
window.show_all()

Gtk.main()
