#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402

import gi
import configparser

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import GObject, Gio, Gdk, Gtk
from slack import Slack
from window_config import ConfigurationWindow


__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class AppWindow(Gtk.ApplicationWindow):

    CONFIG_FILENAME = 'config.ini'

    def __init__(self, application):
        self.Application = application

        # Read GUI from file and retrieve objects from Gtk.Builder
        try:
            self.builder = Gtk.Builder.new_from_file("window_main.glade")
            self.build_channels_combo()
            self.builder.connect_signals(self)
        except GObject.GError:
            print("Error reading GUI file")
            raise

        # Fire up the main window
        self.MainWindow = self.builder.get_object("root_window")
        self.MainWindow.set_application(application)
        self.MainWindow.show()

    def build_channels_combo(self):
        combo_channels = self.builder.get_object("combo_channels")
        name_store = self.builder.get_object("store_channels")
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILENAME)
        # slack = Slack(config['DEFAULT'])
        # channels = slack.get_my_channels()
        channels = config['DEFAULT']['channel_list'].split(",")
        active_index = 0
        for key, channel in enumerate(channels):
            name_store.append([
                channel
            ])
            if config['DEFAULT']['default_channel'] == channel:
                active_index = key

        combo_channels.set_active(active_index)

    def get_selected_channel(self):
        combo_channels = self.builder.get_object("combo_channels")
        index = combo_channels.get_active()
        model = combo_channels.get_model()
        return model[index][0]

    def set_status_bar_message(self, message: str):
        status_bar = self.builder.get_object("status_bar")
        context = status_bar.get_context_id('info')
        status_bar.push(context, message)

    def reset_input(self):
        input_field = self.builder.get_object("input_field")
        input_field.set_text("")

    def switch_image(self, image_name):
        image_field = self.builder.get_object("image1")
        image_field.set_from_file('img/' + image_name)

    # ---------------------------------------------------------------------------------
    # handlers
    # ---------------------------------------------------------------------------------

    def close(self, *args):
        self.MainWindow.destroy()

    def on_close_window(self, *args):
        self.close(*args)

    def on_send(self, button):
        input_field = self.builder.get_object("input_field")
        zoom_id = input_field.get_property("text")

        channel = self.get_selected_channel()

        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILENAME)
        slack = Slack(config['DEFAULT'])

        if not zoom_id:
            message = "Empty Zoom ID"
        else:
            status = slack.send_message(zoom_id, channel)

            if slack.STATUS_SENT == status:
                message = "Zoom ID %s sent to channel %s" % (zoom_id, channel)
                self.reset_input()
                self.switch_image('mutenroshi_02.png')
            else:
                error = slack.get_last_error()
                message = "Error when sending message: %s" % error

        self.set_status_bar_message(message)

    def on_delete_messages(self, button):
        self.switch_image('mutenroshi_01.png')
        channel = self.get_selected_channel()

        message = "Deleting from channel %s" % channel
        self.set_status_bar_message(message)

        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILENAME)
        slack = Slack(config['DEFAULT'])
        status = slack.delete_messages(channel)

        if slack.STATUS_OK == status:
            message = "Messages deleted from channel %s" % channel
        else:
            error = slack.get_last_error()
            message = "Error when deleting messages: %s" % error

        self.set_status_bar_message(message)

    def on_reload_channels(self, button):
        self.switch_image('mutenroshi_01.png')
        message = "Reloading channels"
        self.set_status_bar_message(message)
        self.builder.get_object("combo_channels").get_model().clear()
        self.build_channels_combo()
        message = "Channels reloaded"
        self.set_status_bar_message(message)

    def on_configuration_click(self, button):
        ConfigurationWindow(self.Application)
