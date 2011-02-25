# -*- coding: iso-8859-15 -*-
'''
Created on Feb 24, 2011

@author: poutima
'''

from Base_Miner import Base_Miner
from BeautifulSoup import BeautifulSoup
import re

class WOT_Miner(Base_Miner):
    '''
    A data miner for World of Tanks tankopedia.
    
    Not everything is read ATM, but it is easy to add new fields to the output as needed.
    
    This class tries to figure out the best possible combination for a given tank rather
    than outputting every configuration. So the best gun is selected, for instance, based
    on penetration and damage.
    
    @todo Figure out and print tanks tier.
    '''

    _tiers = {}

    def __init__(self, *params):
        ''' 
        This method will create a dictionary for the tank tiers because this info
        is not avaible on the tank's own page. The only place to retrieve this info is from 
        the tech tree images. Shucks.
        '''
        self._tiers = dict({'MS-1':1,
                            'SU-18':2,      'T-26':2,       'BT-2':2,      'AT-1':2,
                            'SU-26':3,      'T-46':3,       'BT-7':3,      'SU-76':3,
                            'SU-5':4,       'T-28':4,       'A-20':4,      'SU-85B':4,
                            'SU-8':5,       'KV':5,         'T-34':5,      'SU-85':5,
                            'SU-14':6,      'S-51':6,       'KV-3':6,      'KV-1S':6,      'T-34-85':6, 'SU-100':6,
                            'Object 212':7, 'IS':7,         'T-43':7,      'SU-152':7,
                            'IS-3':8,       'T-44':8,       'ISU-152':8,
                            'IS-4':9,       'T-54':9,       'Object 704':9,
                            'IS-7':10,
                            'M3 Stuart':11, 'Valentine':11, 'A-32':11, 'Churchill':11,     'KV-220':11,
                            'Matilda':11,
                            
                            'Leichttraktor':1,
                            'Panzerjäger I':2, 'PzKpfw 35 (t)':2,    'PzKpfw II':2,          'Sturmpanzer I Bison':2,
                            'Marder II':3,      'PzKpfw 38 (t)':3,    'PzKpfw II Luchs':3,    'PzKpfw III Ausf. A':3,  'Wespe':3,        'Sturmpanzer II':3,
                            'Hetzer':4,         'VK 1602 Leopard':4,  'PzKpfw III':4, 'Grille':4,
                            'StuG III':5,       'PzKpfw III/IV':5,    'PzKpfw IV':5,          'Hummel':5,
                            'JagdPz IV':6,      'VK 3001 (P)':6,      'VK 3001 (H)':6,        'VK 3601 (H)':6,         'GW Panther':6,
                            'Jagdpanther':7,    'VK 3002 (DB)':7,     'PzKpfw VI Tiger':7,    'GW Tiger':7,
                            'Ferdinand':8,      'PzKpfw V Panther':8, 'PzKpfw VIB Tiger II':8,
                            'Jagdtiger':9,      'Panther II':9,       'VK 4502 (P) Ausf. B':9,
                            'Maus':10,
                            'PzKpfw 38H735 (f)':11, 'PzKpfw S35 739 (f)':11, 'PzKpfw B2 740(f)':11, 'PzKpfw V-IV':11,
                            'PzKpfw V-IV Alpha':11,
                            
                            'T1 Cunningham':1,
                            'T57':2,           'T2 Medium Tank':2, 'M2 Light Tank':2,
                            'M37':3,           'M2 Medium Tank':3, 'M3 Stuart':3,
                            'M7 Priest':4,     'M3 Lee':4,         'M5 Stuart':4,
                            'M41':5,           'T1 Heavy':5,       'M4 Sherman':5,    'M7':5,
                            'M12':6,           'M6':6,             'M4A3E8 Sherman':6,
                            'M40/M43':7,       'T29':7,            'T20':7,
                            'T32':8,           'T23':8,
                            'T34':9,           'M26 Pershing':9,
                            'T30':10,
                            'T2 Light Tank':11,'Ram-II':11,        'T-14':11,         'M6A2E1':11
                            })

        
    @property
    def link_filter(self):
        return '<a href=\"/encyclopedia/(.+)\">'
    
    @property
    def base_url(self):
        return 'http://game.worldoftanks.eu/encyclopedia/'
    
    def sub_url(self, id):
        return 'http://game.worldoftanks.eu/encyclopedia/' + id

    def _read_line(self, line, record):
        pass

    def _read_general(self, soup, record):
        for row in soup.findAll('tr'):
            cells = row.findAll('td')
            info = (cells[0].renderContents())
            if len(cells) > 1:
                val = cells[1].renderContents()        
            if info == 'Hit Points':
                record['HP'] = val
            elif info == 'Speed limit':
                record['MaxSpeed'] = val
            elif info == 'Engine power':
                record['Engine'] = val
            elif info == 'Hull armor (mm)':
                armor = cells[1].renderContents().split('<br />')
                record['hull_front'] = re.search('.*\s(\d+).*',armor[0]).group(1)
                record['hull_sides'] = re.search('.*\s(\d+).*',armor[1]).group(1)
                record['hull_back'] = re.search('.*\s(\d+).*',armor[2]).group(1)
            elif info == 'Turret armor (mm)':
                armor = cells[1].renderContents().split('<br />')
                record['turret_front'] = re.search('.*\s(\d+).*',armor[0]).group(1)
                record['turret_sides'] = re.search('.*\s(\d+).*',armor[1]).group(1)
                record['turret_back'] = re.search('.*\s(\d+).*',armor[2]).group(1)
            elif info == 'Traverse Speed':
                record['traverse'] = val
            elif info == 'View range':
                record['view_range'] = val
                
        # Some vehicles don't have a turret
        if not record.has_key('turret_front'):
            record['turret_front'] = record['hull_front']
            record['turret_sides'] = record['hull_sides']
            record['turret_back'] = record['hull_back']

    def _read_guns(self, soup, record):
        max_penet = 0
        max_damage = 0
        for row in soup.findNext('table').findAll('tr'):
            cells = row.findAll('td')
            #level = cells[0].renderContents()
            #name = cells[1].renderContents()
            damage = cells[2].renderContents()
            penet = cells[3].renderContents()
            rof = cells[4].renderContents()
            #price = cells[5].renderContents()
        
            norm_penetration = re.search('(\d+)\/(\d+)(\/(\d+))*', penet)
            norm_damage = re.search('(\d+)\/(\d+)(\/(\d))*', damage)
            #norm_damage = re.search('((\d+)\/){2,3}', damage)
            if norm_penetration > max_penet or (norm_penetration == max_penet and norm_damage > max_damage):
                record['damage'] = norm_damage.group(1)
                record['penetration'] = norm_penetration.group(1)
                record['rof'] = rof
                max_penet = record['penetration']
                max_damage = record['damage']

    def _read_head(self, soup, record):
        if soup != None:
            max_armor_front = 0
            max_armor_sides = 0
            max_armor_back = 0
            max_traverse = 0
            for row in soup.findNext('table').findAll('tr'):
                cells = row.findAll('td')
                armor = cells[2].renderContents()
                traverse = cells[3].renderContents()
                range = cells[4].renderContents()
                #price = cells[3].renderContents()
                armor_split = re.search('(\d+)\/(\d+)\/(\d+)', armor)
                better = False
                if (armor_split.group(1) > max_armor_front):
                    better = True
                elif armor_split.group(1) == max_armor_front:
                    if armor_split.group(2) > max_armor_sides:
                        better = True
                    elif armor_split.group(2) == max_armor_sides:
                        if armor_split.group(3) > max_armor_back:
                            better = True
                        elif armor_split.group(3) == max_armor_back:
                            if traverse > max_traverse:
                                better = True
                
                if better == True:
                    record['turret_front'] = armor_split.group(1)
                    record['turret_sides'] = armor_split.group(2)
                    record['turret_back'] = armor_split.group(3)
                    record['traverse'] = traverse
                    record['view_range'] = range
                    max_armor_front = record['turret_front']
                    max_armor_sides = record['turret_sides']
                    max_armor_back = record['turret_back']
                    max_traverse = record['traverse']

    def _read_engine(self, soup, record):
        max_power = 0
        for row in soup.findNext('table').findAll('tr'):
            cells = row.findAll('td')
            power = cells[2].renderContents()
            if power > max_power:
                record['power'] = power
                max_power = power                
    
    def _read_transmission(self, soup, record):
        max_traverse = 0
        for row in soup.findNext('table').findAll('tr'):
            cells = row.findAll('td')
            traverse = cells[3].renderContents()
            if traverse > max_traverse:
                record['traverse'] = traverse
                max_traverse = traverse

    def _read_radio(self, soup, record):
        max_range = 0
        for row in soup.findNext('table').findAll('tr'):
            cells = row.findAll('td')
            range = cells[2].renderContents()
            if range > max_range:
                record['radio_range'] = range
                max_range = range
        
    def read_record(self, data):
        retval = {}
        
        soup = BeautifulSoup(''.join(data))
        
        # Name
        s = soup.find('h2', 'title_lowercase')
        retval['full_name'] = s.renderContents()
        
        # General info 
        s = soup.find('table', 't-tankdescr-game')
        self._read_general(s, retval)
        
        # Gun info
        s = soup.find('h3', 'b-tankdescr-title b-tankdescr-title_guns')
        self._read_guns(s, retval)
                
        # Turret
        s = soup.find('h3', 'b-tankdescr-title b-tankdescr-title_head')
        self._read_head(s, retval)
            
        # Engine
        s = soup.find('h3', 'b-tankdescr-title  b-tankdescr-title_engine')
        self._read_engine(s, retval)
        
        # Transmission
        s = soup.find('h3', 'b-tankdescr-title  b-tankdescr-title_transm')
        self._read_transmission(s, retval)
        
        # Radio
        s = soup.find('h3', 'b-tankdescr-title  b-tankdescr-title_radio')
        self._read_radio(s, retval)

        # Tier
        full_name = re.search('(Light Tank|Medium Tank|Heavy Tank|SPG|Tank Destroyer|Premium Tank)\s(.+)', retval['full_name'])
        
        if self._tiers.has_key(full_name.group(2)):
            retval['tier'] = str(self._tiers[full_name.group(2)])
        else:
            retval['tier'] = '0'
        retval['name'] = full_name.group(2)
        retval['type'] = full_name.group(1)
        return retval
