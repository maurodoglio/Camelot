"""This module provides a singleton workspace that can be used by views
and widget to create new windows or raise existing ones"""

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

import logging

logger = logging.getLogger('camelot.view.workspace')

class DesktopWorkspace(QtGui.QMdiArea):
  def __init__(self, *args):
    QtGui.QMdiArea.__init__(self, *args)
    self.setOption(QtGui.QMdiArea.DontMaximizeSubWindowOnActivation)
    self.setBackground(QtGui.QBrush(QtGui.QColor('white')))
    self.setActivationOrder(QtGui.QMdiArea.ActivationHistoryOrder)

  def addSubWindow(self, widget, *args):
    subwindow = QtGui.QMdiArea.addSubWindow(self, widget, *args)
    if hasattr(widget, 'closeAfterValidation'):
      subwindow.connect(widget, widget.closeAfterValidation, subwindow, QtCore.SLOT("close()"))

class NoDesktopWorkspace(QtCore.QObject):
  def __init__(self):
    QtCore.QObject.__init__(self)
    self._windowlist = []

  def addSubWindow(self, widget, *args):
    self.widget = widget
    self.widget.setParent(None)
    self.widget.show()
    self._windowlist.append(self.widget)
    self.connect(widget, QtCore.SIGNAL('WidgetClosed()'), self.removeWidgetFromWorkspace)
    
  def subWindowList(self):
    return self._windowlist
  
  def removeWidgetFromWorkspace(self):
    self._windowlist.remove(self.widget)
    
_workspace_ = []
        
def construct_workspace(*args, **kwargs):
  _workspace_.append(DesktopWorkspace())
  return _workspace_[0]
  
def construct_no_desktop_workspace(*args, **kwargs):
  _workspace_.append(NoDesktopWorkspace())
  return _workspace_[0]

def get_workspace():
  print _workspace_
  return _workspace_[0]
