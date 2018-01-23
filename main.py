#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402

import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import GObject, Gio, Gdk, Gtk
from window_main import AppWindow

__author__ = "JM Leroux <jmleroux.pro@gmail.com"
__license__ = "OSL 3.0"


class MyApplication(Gtk.Application):

    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)

    def do_activate(self):
        AppWindow(self)

    def do_startup(self):
        Gtk.Application.do_startup(self)


def main():
    application = MyApplication("jmleroux.slack-messenger", Gio.ApplicationFlags.FLAGS_NONE)
    application.run()


if __name__ == "__main__":
    main()
