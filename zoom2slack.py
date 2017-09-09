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
        input_field = builder.get_object("input_field")
        zoom_id = input_field.get_property("text")

        if '' != zoom_id:
            self.send_to_slack(zoom_id)
        else:
            status_bar = builder.get_object("status_bar")
            status_bar.set_property("label", "Empty Zoom ID")

    def send_to_slack(self, zoom_id: str):
        message = "Zoom ID %s sent to channel %s" % (zoom_id, config.VIDEO_CONF_CHANNEL)
        status_bar = builder.get_object("status_bar")

        slack = Slack(config)
        status = slack.send_message(zoom_id)

        if slack.STATUS_SENT == status:
            builder.get_object("status_bar")
            status_bar.set_property("label", message)
        elif slack.STATUS_INVALID_FORMAT == status:
            status_bar.set_property("label", "Invalid Zoom ID")
        else:
            status_bar.set_property("label", "Error when sending message")


builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(Handler())

window = builder.get_object("root_window")
window.show_all()

Gtk.main()
