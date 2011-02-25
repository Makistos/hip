# -*- coding: iso-8859-15 -*-
'''
Created on Feb 25, 2011

@author: mep
'''
from Base_Outputter import Base_Outputter

class CSV_Outputter(Base_Outputter):
    '''
    Class to print given array of dictionaries to CVS.
    '''

    def _print_header(self):
        ''' Print header based on dict key names '''
        print ';'.join(self._data[0].iterkeys())

    def _print_data(self):
        ''' Prints the data in CVS format '''
        for i in self._data:
            print ";".join(i.itervalues())

    def __str__(self):
        ''' Outputs data given on object init as CVS. '''
        retval = ''
        self._print_header()
        self._print_data()
                     
        return retval
