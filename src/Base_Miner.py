# -*- coding: iso-8859-15 -*-
'''
Created on Feb 24, 2011

@author: poutima
'''

from abc import ABCMeta, abstractproperty, abstractmethod

class Base_Miner(object):
    __metaclass__ = ABCMeta
    
    '''
    Base class for data miners. Main script (hip.py) expects data miners to implement this IF.
    '''

    @abstractproperty
    def base_url(self):
        ''' Returns base address to web page with data to mine.'''
        raise NotImplementedError
    
    @abstractproperty
    def link_filter(self):
        ''' Regexp pattern that matches the sub-page links.'''
        raise NotImplementedError
 
    _fields = ''
    _curr_record = {}
    
    def __init__(self, *params):
        '''
        Constructor for the miner. Params can be used to e.g. give web page address or other 
        identifying info.
        '''
        raise NotImplementedError
    
    def pre_read(self):
        ''' A function that is run before the actual data mining. See WOT_Miner for an example. '''  
        pass
    
    @abstractmethod
    def sub_url(self, id):
        ''' Returns a fully qualified URL to sub-page with item id.'''
        raise NotImplementedError
    
    @abstractmethod
    def read_record(self, data):
        ''' Reads and returns a single sub-page as a dictionary.'''
        raise NotImplementedError    
    


    