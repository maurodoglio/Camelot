from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.core.constants import camelot_small_icon_width
from camelot.core.utils import variant_to_pyobject
from camelot.view.proxy import ValueLoading
from camelot.view.utils import local_date_format

class DateDelegate(CustomDelegate):
    """Custom delegate for date values"""
  
    __metaclass__ = DocumentationMetaclass
    
    editor = editors.DateEditor
    
    def __init__(self, parent=None, **kwargs):
        CustomDelegate.__init__(self, parent, **kwargs)
        self.date_format = local_date_format()
        self._width = self._font_metrics.averageCharWidth() * (len(self.date_format) + 4)  + (camelot_small_icon_width*2) * 2
    
    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        dateObj = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        field_attributes = variant_to_pyobject(index.model().data(index, Qt.UserRole))
        editable, background_color = True, None
        if field_attributes != ValueLoading:
            editable = field_attributes.get( 'editable', True )
            background_color = field_attributes.get( 'background_color', None )
        
        if dateObj not in (None, ValueLoading):
            formattedDate = QtCore.QDate(dateObj).toString(self.date_format)
        else:
            formattedDate = "0/0/0"
          
        rect = option.rect
        rect = QtCore.QRect(rect.left()+3, rect.top()+6, 16, 16)
        fontColor = QtGui.QColor()

        if( option.state & QtGui.QStyle.State_Selected ):
            painter.fillRect(option.rect, option.palette.highlight())
            if editable:
                Color = option.palette.highlightedText().color()
                fontColor.setRgb(Color.red(), Color.green(), Color.blue())
            else:
                fontColor.setRgb(130,130,130)
        else:
            if editable:
                painter.fillRect(option.rect, background_color or option.palette.base())
                fontColor.setRgb(0,0,0)
            else:
                painter.fillRect(option.rect, background_color or option.palette.window())
                fontColor.setRgb(130,130,130)

              
              
        painter.setPen(fontColor.toRgb())
        rect = QtCore.QRect(option.rect.left()+23,
                            option.rect.top(),
                            option.rect.width()-23,
                            option.rect.height())
        
        painter.drawText(rect.x()+2,
                         rect.y(),
                         rect.width()-4,
                         rect.height(),
                         Qt.AlignVCenter | Qt.AlignRight,
                         str(formattedDate))
        
        painter.restore()
