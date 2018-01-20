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
    # Main initialization routine
    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self.connect("activate", self.new_window)

    def new_window(self, *args):
        AppWindow(self)


def main():
    application = MyApplication("jmleroux.zoom2slack", Gio.ApplicationFlags.FLAGS_NONE)
    application.run()


if __name__ == "__main__": main()
