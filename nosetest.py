#!/usr/bin/env python3

import sys
import os
import nose
import unittest.mock as mock
import builtins

pyqt4   = mock.Mock()
plt     = mock.Mock()
figcanv = mock.Mock()
navtool = mock.Mock()

orig_import = __import__


def import_mock(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'matplotlib.backends.backend_qt4agg':
        print(fromlist)

    if name == 'PyQt4':
        return pyqt4
    elif name == 'matplotlib.pyplot':
        return plt
    elif name == 'matplotlib.backends.backend_qt4agg' and fromlist == ('FigureCanvasQTAgg',):
        return figcanv
    elif name == 'matplotlib.backends.backend_qt4' and fromlist == ('NavigationToolbar2QT',):
        return navtool
    return orig_import(name, globals, locals, fromlist, level)

with mock.patch('builtins.__import__', import_mock) as mc:
    nose.main()
