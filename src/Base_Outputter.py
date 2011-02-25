# -*- coding: iso-8859-15 -*-
'''
Created on Feb 25, 2011

@author: poutima
'''

from copy import deepcopy
from abc import ABCMeta, abstractproperty, abstractmethod

class Base_Outputter(object):
    __metaclass__ = ABCMeta    
    '''
    Base class for different kinds of printers that print arrays of dictionaries.
    '''

    _data = {}

    def __init__(self, data):
        '''
        Constructor
        '''
        self._data = deepcopy(data)
