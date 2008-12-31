#  ============================================================================
#
#  Copyright (C) 2007-2008 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  this file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact
#  project-camelot@conceptive.be.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ============================================================================

"""
Python structures to represent interface forms.
These structures can be transformed to QT forms.
"""

import logging
logger = logging.getLogger('camelot.view.forms')

from PyQt4 import QtGui

from camelot.view.controls.editors import One2ManyEditor
from camelot.view.controls.editors import RichTextEditor

def structure_to_form(structure):
  """Convert a python data structure to a form, using the following rules :
  
  if structure is an instance of Form, return structure
  if structure is a list, create a Form from this list
  """
  if isinstance(structure, Form):
    return structure
  return Form(structure)


class Form(object):
  """Use the QFormLayout widget to render a form"""
  
  def __init__(self, content, scrollbars=False):
    """@param content: a list with the field names and forms to render"""
    assert isinstance(content, list)
    self._content = content
    self._scrollbars = scrollbars
    self._fields = []
    for c in content:
      if isinstance(c, Form):
        self._fields.extend(c.get_fields())
      else:
        assert isinstance(c, (str, unicode))
        self._fields.append(c)

  def get_fields(self):
    """@return : the fields, visible in this form"""
    return self._fields
  
  def render(self, widgets, parent=None):
    """@param widgets: a dictionary mapping each field in this form to a tuple
    of (label, widget editor) 

    @return : a QWidget into which the form is rendered
    """
    logger.debug('rendering %s' % self.__class__.__name__) 
    form_layout = QtGui.QFormLayout()
    form_layout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow) 
    for field in self._content:
      if isinstance(field, Form):
        form_layout.addRow(field.render(widgets, parent))
      if field in widgets:
        label, editor = widgets[field]
        if isinstance(editor, One2ManyEditor) or\
           isinstance(editor, RichTextEditor):
          form_layout.addRow(label)
          form_layout.addRow(editor)
        else:
          form_layout.addRow(label, editor)


    form_widget = QtGui.QWidget()
    form_widget.setSizePolicy(QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding)
    form_widget.setLayout(form_layout)
    
    if self._scrollbars:
      scroll_area = QtGui.QScrollArea()
      scroll_area.setWidget(form_widget)
      scroll_area.setWidgetResizable(True)
      scroll_area.setFrameStyle(QtGui.QFrame.NoFrame)
      return scroll_area
    
    return form_widget
  

class TabForm(Form):
  """Render forms within a QTabWidget"""
  
  def __init__(self, tabs):
    """@param tabs: a list of tuples of (tab_label, tab_form)"""
    assert isinstance(tabs, list)
    for tab in tabs:
      assert isinstance(tab, tuple)
    self.tabs = [(tab_label, structure_to_form(tab_form))
                 for tab_label, tab_form in tabs]
    super(TabForm, self).__init__(sum((tab_form.get_fields()
                                  for tab_label, tab_form in self.tabs), []))
  
  def render(self, widgets, parent=None):
    logger.debug('rendering %s' % self.__class__.__name__) 
    widget = QtGui.QTabWidget(parent)
    for tab_label, tab_form in self.tabs:      
      widget.addTab(tab_form.render(widgets, widget), tab_label)
    return widget
  

class HBoxForm(Form):
  """Render different forms in a horizontal box"""
  
  def __init__(self, columns):
    """@param columns: a list of forms to display in the different columns
    of the horizontal box"""
    assert isinstance(columns, list)
    self.columns = [structure_to_form(col) for col in columns]
    super(HBoxForm, self).__init__(sum((column_form.get_fields()
                                  for column_form in self.columns), []))

  def render(self, widgets, parent=None):
    logger.debug('rendering %s' % self.__class__.__name__) 
    widget = QtGui.QHBoxLayout()
    for form in self.columns:
      widget.addWidget(form.render(widgets, parent))
    return widget
  

class VBoxForm(Form):
  """Render different forms or widgets in a vertical box"""
  
  def __init__(self, rows):
    """@param rows: a list of forms to display in the different columns
    of the horizontal box
    """
    assert isinstance(rows, list)
    self.rows = [structure_to_form(row) for row in rows]
    super(VBoxForm, self).__init__(sum((row_form.get_fields() for row_form in self.rows), []))

  def render(self, widgets, parent=None):
    logger.debug('rendering %s' % self.__class__.__name__) 
    widget = QtGui.QVBoxLayout()
    for form in self.rows:
      widget.addWidget(form.render(widgets, parent))
    return widget


class WidgetOnlyForm(Form):
  """Renders a single widget without its label, typically a one2many widget"""
  
  def __init__(self, field):
    assert isinstance(field, (str, unicode))
    super(WidgetOnlyForm, self).__init__([field])
    
  def render(self, widgets, parent=None):
    logger.debug('rendering %s' % self.__class__.__name__) 
    label, editor = widgets[self.get_fields()[0]]
    return editor
