
from customdelegate import *
from camelot.view.art import Icon

class StarDelegate(CustomDelegate):
  """Delegate for integer values from (1 to 5)(Rating Delegate)

.. image:: ../_static/rating.png
"""

  editor = editors.StarEditor

  def __init__(self, parent, editable=True, maximum=5, **kwargs):
    CustomDelegate.__init__(self,
                            parent=parent,
                            editable=editable,
                            maximum=maximum,
                            **kwargs)
    self.maximum = maximum
    
  def paint(self, painter, option, index):
    painter.save()
    self.drawBackground(painter, option, index)
    stars = index.model().data(index, Qt.EditRole).toInt()[0]
    editor = editors.StarEditor(parent=None, maximum=self.maximum, editable=self.editable)
    rect = option.rect
    rect = QtCore.QRect(rect.left()+3, rect.top()+6, rect.width()-5, rect.height())
    for i in range(5):
      if i+1<=stars:
        icon = Icon('tango/16x16/status/weather-clear.png').getQPixmap()
        QtGui.QApplication.style().drawItemPixmap(painter, rect, 1, icon)
        rect = QtCore.QRect(rect.left()+20, rect.top(), rect.width(), rect.height())
    painter.restore()