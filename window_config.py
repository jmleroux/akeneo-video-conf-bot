#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402

import gi
import config as config
import time

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import GObject, Gio, Gdk, Gtk

__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class ConfigurationWindow(Gtk.ApplicationWindow):
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

        # Fire up the main window
        self.MainWindow = self.builder.get_object("config_window")
        self.MainWindow.set_application(application)
        self.MainWindow.show()

    def load_config_file(self):
        return True

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

    def on_click_cancel(self, *args):
        self.close(*args)
