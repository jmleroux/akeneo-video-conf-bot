#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402

import configparser
import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import GObject, Gio, Gdk, Gtk

__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class ConfigurationWindow(Gtk.ApplicationWindow):

    CONFIG_FILENAME = 'config.ini'

    def __init__(self, application):
        self.Application = application

        # Read GUI from file and retrieve objects from Gtk.Builder
        try:
            self.builder = Gtk.Builder.new_from_file("window_config.glade")
            self.load_config_file()
            self.builder.connect_signals(self)
        except GObject.GError:
            print("Error reading GUI file")
            raise

        self.MainWindow = self.builder.get_object("config_window")
        self.MainWindow.set_application(application)
        self.MainWindow.show()

    def __get_config_from_file(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILENAME)
        return config

    def __save_config_to_file(self, config):
        with open(self.CONFIG_FILENAME, 'w') as configfile:
            config.write(configfile)

    def load_config_file(self):
        config = self.__get_config_from_file()
        field = self.builder.get_object("input_bot_token")
        field.set_text(config['DEFAULT']['bot_token'])
        field = self.builder.get_object("input_bot_id")
        field.set_text(config['DEFAULT']['bot_id'])
        field = self.builder.get_object("input_channel_list")
        field.set_text(config['DEFAULT']['channel_list'])
        field = self.builder.get_object("input_default_channel")
        field.set_text(config['DEFAULT']['default_channel'])
        field = self.builder.get_object("input_message_pattern")
        text_buffer = field.get_buffer()
        message_pattern = config['DEFAULT']['message_pattern'].replace('%', '%%')
        text_buffer.set_text(message_pattern)

    def save_config_file(self):
        config = self.__get_config_from_file()
        field = self.builder.get_object("input_bot_token")
        config['DEFAULT']['BOT_TOKEN'] = field.get_text()
        field = self.builder.get_object("input_bot_id")
        config['DEFAULT']['BOT_ID'] = field.get_text()
        field = self.builder.get_object("input_channel_list")
        config['DEFAULT']['channel_list'] = field.get_text()
        field = self.builder.get_object("input_default_channel")
        config['DEFAULT']['DEFAULT_CHANNEL'] = field.get_text()
        field = self.builder.get_object("input_message_pattern")
        text_buffer = field.get_buffer()
        config['DEFAULT']['message_pattern'] = text_buffer.get_text(*text_buffer.get_bounds(), include_hidden_chars=False)
        self.__save_config_to_file(config)

    def set_status_bar_message(self, message: str):
        status_bar = self.builder.get_object("status_bar")
        context = status_bar.get_context_id('info')
        status_bar.push(context, message)

    def reset_input(self):
        input_field = self.builder.get_object("input_field")
        input_field.set_text("")

    # ---------------------------------------------------------------------------------
    # handlers
    # ---------------------------------------------------------------------------------

    def close(self, *args):
        self.MainWindow.destroy()

    def on_click_ok(self, *args):
        self.save_config_file()
        self.close(*args)

    def on_click_cancel(self, *args):
        self.close(*args)
