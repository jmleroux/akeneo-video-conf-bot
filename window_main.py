#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402

import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

import config as config
from gi.repository import GObject, Gio, Gdk, Gtk
from slack import Slack

__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class AppWindow(object):
    def __init__(self, application):
        self.Application = application

        # Read GUI from file and retrieve objects from Gtk.Builder
        try:
            self.builder = Gtk.Builder.new_from_file("ui.glade")
            self.build_channels_combo()
            self.builder.connect_signals(self)
        except GObject.GError:
            print("Error reading GUI file")
            raise

        # Fire up the main window
        self.MainWindow = self.builder.get_object("root_window")
        self.MainWindow.set_application(application)
        self.MainWindow.show()

    def close(self, *args):
        self.MainWindow.destroy()

    def build_channels_combo(self):
        combo_channels = self.builder.get_object("combo_channels")
        name_store = self.builder.get_object("store_channels")
        active_index = 0
        for key, channel in enumerate(self.list_channels()):
            name_store.append([
                channel['name']
            ])
            if config.VIDEO_CONF_CHANNEL == channel['name']:
                active_index = key

        combo_channels.set_active(active_index)

    def get_selected_channel(self):
        combo_channels = self.builder.get_object("combo_channels")
        index = combo_channels.get_active()
        model = combo_channels.get_model()
        return model[index][0]

    def set_status_bar_message(self, message: str):
        status_bar = self.builder.get_object("status_bar")
        status_bar.set_property("label", message)

    def delete_messages(self):
        channel = self.get_selected_channel()

        slack = Slack(config)
        status = slack.delete_messages(channel)

        if slack.STATUS_OK == status:
            message = "Messages deleted from channel %s" % channel
        else:
            error = slack.get_last_error()
            message = "Error when deleting messages: %s" % error

        self.set_status_bar_message(message)

    def send_to_slack(self):
        input_field = self.builder.get_object("input_field")
        zoom_id = input_field.get_property("text")

        channel = self.get_selected_channel()

        slack = Slack(config)

        if not zoom_id:
            message = "Empty Zoom ID"
        else:
            status = slack.send_message(zoom_id, channel)

            if slack.STATUS_SENT == status:
                message = "Zoom ID %s sent to channel %s" % (zoom_id, channel)
                self.reset_input()
            else:
                error = slack.get_last_error()
                message = "Error when sending message: %s" % error

        self.set_status_bar_message(message)

    def reset_input(self):
        input_field = self.builder.get_object("input_field")
        input_field.set_text("")

    @staticmethod
    def list_channels():
        slack = Slack(config)
        channels = slack.get_my_channels()
        return channels

    def on_close_window(self, *args):
        self.close(*args)

    def on_send(self, button):
        self.send_to_slack()

    def on_delete_messages(self, button):
        self.delete_messages()
