#  ============================================================================
#
#  Copyright (C) 2007-2011 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file license.txt included in the packaging of
#  this file.  Please review this information to ensure GNU
#  General Public Licensing requirements will be met.
#
#  If you are unsure which license is appropriate for your use, please
#  visit www.python-camelot.com or contact project-camelot@conceptive.be
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ============================================================================

"""
This is part of a test implementation of the new actions draft, it is not
intended for production use
"""

from camelot.admin.action.base import Action
from application_action import ( ApplicationActionGuiContext,
                                 ApplicationActionModelContext )

class FormActionModelContext( ApplicationActionModelContext ):
    """On top of the attributes of the 
    :class:`camelot.admin.action.application_action.ApplicationActionModelContext`, 
    this context contains :
        
    .. attribute:: current_row
    
        the row in the list that is currently displayed in the form
        
    .. attribute:: collection_count
    
        the number of objects that can be reached in the form.
                
    .. attribute:: session
    
        The session to which the objects in the list belong.
        
    """
    
    def __init__( self ):
        super( ListActionModelContext, self ).__init__()
        self._model = None
        self.admin = None
        self.current_row = 0
        self.collection_count = 0
        
    @property
    def session( self ):
        return self._model.get_query_getter()().session
        
    def get_object( self ):
        """
        :return: the object currently displayed in the form, None if no object
            is displayed yet
        """
        if self.current_row:
            return self._model._get_object( self.current_row )
    
    def get_collection( self, yield_per = None ):
        """
        :param yield_per: an integer number giving a hint on how many objects
            should fetched from the database at the same time.
        :return: a generator over the objects in the list
        """
        for obj in self._model.get_collection():
            yield obj
        
class FormActionGuiContext( ApplicationActionGuiContext ):
    
    model_context = FormActionModelContext
    
    def __init__( self ):
        """The context for an :class:`Action` on a form.  On top of the attributes of the 
        :class:`camelot.admin.action.application_action.ApplicationActionGuiContext`, 
        this context contains :
    
        .. attribute:: widget_mapper
    
           the :class:`QtGui.QDataWidgetMapper` class that relates to the form 
           widget
           
        """
        super( FormActionGuiContext, self ).__init__()
        self.widget_mapper = None

    def create_model_context( self ):
        context = super( FormActionGuiContext, self ).create_model_context()
        context._model = self.widget_mapper.model()
        context.collection_count = context._model.rowCount()
        self.current_row = self.widget_mapper.currentIndex()
        return context
        
    def copy( self ):
        new_context = super( FormActionGuiContext, self ).copy()
        new_context.widget_mapper = self.widget_mapper
        return new_context