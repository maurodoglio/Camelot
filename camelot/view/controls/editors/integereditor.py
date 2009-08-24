
from customeditor import *
from camelot.view.art import Icon
from math import floor

class IntegerEditor(CustomEditor):
  """Widget for editing an integer field, with a calculator"""

  def __init__(self,
               parent=None,
               minimum=camelot_minint,
               maximum=camelot_maxint,
               editable=True,
               **kwargs):
    CustomEditor.__init__(self, parent)
    action = QtGui.QAction(self)
    action.setShortcut(Qt.Key_F3)
    self.setFocusPolicy(Qt.StrongFocus)
    self.spinBox = QtGui.QDoubleSpinBox(parent)
    self.spinBox.setReadOnly(not editable)
    self.spinBox.setRange(minimum, maximum)
    self.spinBox.setDecimals(0)
    self.spinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
    self.spinBox.setSingleStep(1)
    self.spinBox.addAction(action)
    calculatorButton = QtGui.QToolButton()
    icon = Icon('tango/16x16/apps/accessories-calculator.png').getQIcon()
    calculatorButton.setIcon(icon)
    calculatorButton.setAutoRaise(True)
    calculatorButton.setFixedHeight(20)

    self.connect(calculatorButton,
                 QtCore.SIGNAL('clicked()'),
                 lambda:self.popupCalculator(self.spinBox.value()))
    self.connect(action,
                 QtCore.SIGNAL('triggered(bool)'),
                 lambda:self.popupCalculator(self.spinBox.value()))
    self.connect(self.spinBox,
                 QtCore.SIGNAL('editingFinished()'),
                 lambda:self.editingFinished(self.spinBox.value()))

    layout = QtGui.QHBoxLayout()
    layout.setMargin(0)
    layout.setSpacing(0)
    layout.addWidget(self.spinBox)
    if editable:
      layout.addWidget(calculatorButton)
    else:
      self.spinBox.setEnabled(False)
    self.setFocusProxy(self.spinBox)
    self.setLayout(layout)

  def set_value(self, value):
    value = CustomEditor.set_value(self, value)
    if value!=None:
      value = str(value).replace(',', '.')
      self.spinBox.setValue(eval(value))
    else:
      self.spinBox.setValue(0)

  def get_value(self):
    self.spinBox.interpretText()
    value = self.spinBox.value()
    return CustomEditor.get_value(self) or value

  def popupCalculator(self, value):
    from camelot.view.controls.calculator import Calculator
    calculator = Calculator(self)
    calculator.setValue(value)
    self.connect(calculator,
                 QtCore.SIGNAL('calculationFinished'),
                 self.calculationFinished)
    calculator.exec_()

  def calculationFinished(self, value):
    self.spinBox.setValue(floor(float(value)))
    self.emit(QtCore.SIGNAL('editingFinished()'), value)

  def editingFinished(self, value):
    self.emit(QtCore.SIGNAL('editingFinished()'), value)
