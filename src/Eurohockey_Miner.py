# -*- coding: iso-8859-15 -*-
'''
Created on Feb 24, 2011

@author: poutima
'''

from Base_Miner import Base_Miner
import re

class Eurohockey_Miner(Base_Miner):
    '''
    A data miner for the Eurohockey web page.
    
    Currently this only digs out rosters, the old version also dug out player stats but 
    I'm yet to decide on how to print that to a 2D data format.
    
    @todo This should also be converted to use Beautiful Soup.
    '''

    _fields = ['Gender', 'Born', 'Height', 'Weight', 'Position', 'Shoots', 'Drafted']
    _team = ''
    _league = ''
    _season = ''
    _curr_field = ''
    
    def __init__(self, *params):
        '''
        Eurohockey_Miner requires id for team, league and season to construct the base URL.
        '''
        pars = params[0].split(',')
        self._team = str(pars[0])
        self._league = str(pars[1])
        self._season = str(pars[2])
        
    @property
    def link_filter(self):
        return 'players/show_player.cgi\?serial=(\d+)\">(.+)</a></td>'
    
    @property
    def base_url(self):
        return 'http://www.eurohockey.net/players/show_roster.cgi?team=' + self._team + '&league=' + self._league + '&season=' + self._season
    
    def sub_url(self, id):
        return "http://www.eurohockey.net/players/show_player.cgi?serial=" + id

    def _read_line(self, line, record):
#        global begin_record
#        global col
        
        if self._curr_field != '':
            val = re.search('<td>(.*)</td>', line).group(1)
            record[self._curr_field] = val
            self._curr_field = ''        
            return
#        if '</tr' in line and begin_record == 1:
#            begin_record = 0
    #        playerSeasonInfo = PlayerSeasonInfo(infoFields)
    #        self.seasons = self.seasons + [playerSeasonInfo]
    #        infoFields = []
 #       if begin_record == 1:
    #       col = col + 1
    #       tmp_match =  re.search('<td>(.+)</td>', line.strip())
    #       if tmp_match:
    #           infoFields = infoFields + [tmp_match.group(1)]
 #           pass
        if '<th>' in line:
            #print line
            #test = re.compile(')
            field = re.search('<th>(.+)</th>', line.strip()).group(1)
            #print "field: " + field
            if field in self._fields:
                self._curr_field = field
        if '<h1>' in line:
            # Player name & nationality are in the header only
            name = re.search('<h1>(.+) \((.+)\)</h1>', line.strip())
            record['Name'] = name.group(1)
            record['Nationality'] = name.group(2) 
            
        if '<tr class=\"even\"' in line or '<tr class=\"odd\"' in line: 
    #     begin_record = 1
    #     col = 0
            pass

    def read_record(self, data):
        retval = {}
        
        for line in data:
            self._read_line(line, retval)
            
        return retval
    