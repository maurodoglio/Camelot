'''
Helper Classes used in ApplicationAction, FormAction and ListAction

Not to be used outside Camelot itself
'''
import logging

from PyQt4 import QtGui, QtCore

from camelot.core.utils import ugettext as _

LOGGER = logging.getLogger('camelot.admin.abstract_action')

class AbstractAction(object):
    """Helper class with methods to be used by all Action classes
    """
    
    def get_options(self):
        """Check if the object has an **Options** attribute, and if it has,
        present the user with a form to fill in the options.  Returns if the user
        has pressed OK or Cancel
        :return: an object of type Options or None
        """
        if self.Options:
            from camelot.view.wizard.pages.form_page import FormPage
            
            class OptionsPage(FormPage):
                Data = self.Options
                icon = self._icon
                title = self._name
                sub_title = _('Please complete the options and continue')
                
            class ActionWizard(QtGui.QWizard):
            
                def __init__(self, parent=None):
                    super(ActionWizard, self).__init__(parent)
                    self.setWindowTitle(_('Options'))
                    self.options_page = OptionsPage(parent=self)
                    self.addPage(self.options_page)
                    
            wizard = ActionWizard()
            i = wizard.exec_()
            if not i:
                return None
            self.options = wizard.options_page.get_data()
            return self.options
        
class AbstractOpenFileAction(AbstractAction):
    """Some convenience methods to create a file and open it"""

    suffix = '.txt'
    
    def create_temp_file(self):
        """:return: a temporary file name"""
        import os
        import tempfile
        file_descriptor, file_name = tempfile.mkstemp(suffix=self.suffix)
        os.close(file_descriptor)
        return file_name
    
    def open_file(self, file_name):
        url = QtCore.QUrl.fromLocalFile(file_name)
        LOGGER.debug(u'open url : %s'%unicode(url))
        QtGui.QDesktopServices.openUrl(url)
