"""This module adds a menu item to the Nemo right-click menu which allows to Open Gitk
   on the Selected Folder/Current Directory just through the right-clicking"""

#   gitk-here.py version 1.0
#
#   Copyright 2009-2021 Giuseppe Penone <giuspen@gmail.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA 02110-1301, USA.

import gi
gi.require_version('Nemo', '3.0')
from gi.repository import Nemo, GObject, Gtk, GdkPixbuf
import urllib.parse, os, subprocess
import locale, gettext

APP_NAME = "nemo-pyextensions"
LOCALE_PATH = "/usr/share/locale/"
# internationalization
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP_NAME, LOCALE_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext
# post internationalization code starts here


class OpenGitkHere(GObject.GObject, Nemo.MenuProvider):
    """Implements the 'Open Gitk Here' extension to the Nemo right-click menu"""

    def __init__(self):
        """Nemo crashes if a plugin doesn't implement the __init__ method"""
        pass

    def _run(self, menu, selected):
        """Runs the Open Gitk Here on the given Directory"""
        uri_raw = selected.get_uri()
        if len(uri_raw) < 7: return
        curr_dir = urllib.parse.unquote(uri_raw[7:])
        if os.path.isfile(curr_dir): curr_dir = os.path.dirname(curr_dir)
        bash_string = "cd \"" + curr_dir + "\" && gitk &"
        subprocess.call(bash_string, shell=True)

    def get_file_items(self, window, sel_items):
        """Adds the 'Open Gitk Here' menu item to the Nemo right-click menu,
           connects its 'activate' signal to the 'run' method passing the selected Directory/File"""
        if len(sel_items) != 1 or sel_items[0].get_uri_scheme() != 'file': return
        item = Nemo.MenuItem(name='NemoPython::gitk',
                                 label=_('Open Gitk Here'),
                                 tip=_('Open the Gitk Workbench on the Current/Selected Directory'),
                                 icon='gitk')
        item.connect('activate', self._run, sel_items[0])
        return [item]

    def get_background_items(self, window, current_directory):
        """Adds the 'Open Gitk Here' menu item to the Nemo right-click menu,
           connects its 'activate' signal to the 'run' method passing the current Directory"""
        item = Nemo.MenuItem(name='NemoPython::gitk',
                             label=_('Open Gitk Here'),
                             tip=_('Open the Gitk Workbench on the Current Directory'),
                             icon='gitk')
        item.connect('activate', self._run, current_directory)
        return [item]
