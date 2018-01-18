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


class MyApplication(Gtk.Application):
    # Main initialization routine
    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self.connect("activate", self.new_window)

    def new_window(self, *args):
        AppWindow(self)


class AppWindow(object):
    def __init__(self, application):
        self.Application = application

        # Read GUI from file and retrieve objects from Gtk.Builder
        try:
            builder = Gtk.Builder.new_from_file("ui.glade")
            self.build_channels_combo(builder)
            builder.connect_signals(self)
        except GObject.GError:
            print("Error reading GUI file")
            raise

        # Fire up the main window
        self.MainWindow = builder.get_object("root_window")
        self.MainWindow.set_application(application)
        self.MainWindow.show()

    def close(self, *args):
        self.MainWindow.destroy()

    def build_channels_combo(self, builder):
        combo_channels = builder.get_object("combo_channels")
        name_store = builder.get_object("store_channels")
        active_index = 0
        for key, channel in enumerate(self.list_channels()):
            name_store.append([
                channel['name']
            ])
            if config.VIDEO_CONF_CHANNEL == channel['name']:
                active_index = key

        combo_channels.set_active(active_index)

    def get_selected_channel(self, builder):
        combo_channels = builder.get_object("combo_channels")
        index = combo_channels.get_active()
        model = combo_channels.get_model()
        return model[index][0]

    def set_status_bar_message(self, builder, message: str):
        status_bar = builder.get_object("status_bar")
        status_bar.set_property("label", message)

    def delete_messages(self, builder):
        channel = self.get_selected_channel(builder)

        slack = Slack(config)
        status = slack.delete_messages(channel)

        if slack.STATUS_OK == status:
            message = "Messages deleted from channel %s" % channel
        else:
            error = slack.get_last_error()
            message = "Error when deleting messages: %s" % error

        self.set_status_bar_message(message)

    def send_to_slack(self, builder):
        input_field = builder.get_object("input_field")
        zoom_id = input_field.get_property("text")

        channel = self.get_selected_channel(builder)

        slack = Slack(config)

        if not zoom_id:
            message = "Empty Zoom ID"
        elif not self.is_valid_input(zoom_id):
            message = "Invalid Zoom ID"
        else:
            status = slack.send_message(zoom_id, channel)

            if slack.STATUS_SENT == status:
                message = "Zoom ID %s sent to channel %s" % (zoom_id, channel)
                self.reset_input()
            else:
                error = slack.get_last_error()
                message = "Error when sending message: %s" % error

        self.set_status_bar_message(message)

    def is_valid_input(self, zoom_id: str):
        if not zoom_id:
            return False

        return True

    def reset_input(self, builder):
        input_field = builder.get_object("input_field")
        input_field.set_text("")

    def list_channels(self):
        slack = Slack(config)
        channels = slack.get_my_channels()
        return channels

    def on_close_window(*args):
        Gtk.main_quit(*args)

    def on_send(self, button):
        self.send_to_slack()

    def on_delete_messages(self, button):
        self.delete_messages()


def main():
    application = MyApplication("com.bachsau.example", Gio.ApplicationFlags.FLAGS_NONE)
    application.run()


if __name__ == "__main__": main()
