#!/usr/bin/python
'''
Created on Feb 25, 2011

@author: poutima
'''

import pprint
import csv
import getopt
import sys

def print_tanks(tanks):
    pp = pprint.PrettyPrinter(indent=4)
    
    for row in tanks:
        pp.pprint(row)

def usage():
    print "Figure it out!"

def top_values(tanks):
    tank = list(tanks)[0]
    best_tanks = dict({'HP':tank, 'MaxSpeed':tank, 'turret_front':tank, 'turret_sides':tank, 'turret_back':tank, 
                       'hull_front':tank, 'hull_sides':tank, 'hull_back':tank,
                       'penetration':tank, 'damage':tank, 'traverse':tank})
    
    fields = ['HP', 'MaxSpeed', 'penetration', 'damage', 'traverse',
              'turret_front', 'turret_sides', 'turret_back', 
              'hull_front', 'hull_sides', 'hull_back']
    
    for tank in tanks:
        for field in fields:
            if tank[field] > best_tanks[field][field]:
                best_tanks[field] = tank

    print "\nBest tanks by values:\n"
    print "Name\t\t\t\ttier\t\tvalue\n\n"
    for field in fields:
        tank = best_tanks[field] 
        print field + ": " + tank['full_name'] + '\t\t[' + tank['tier'] + "]\t\t (" + tank[field] + ")" 
        
            
def filter_func(tank, use_tanks, target):
    retval = False
    
    if use_tanks == True:
        key = 'name'
    else:
        key = 'tier'
    
    for name in target:
        if tank[key] == name:
            retval =  True
            #print 'Tank: ' + tank['name'] + ' & Tier: ' + tank['tier'] + ' & Target: ' + str(target)
             
    return retval

def main(argv):
    tanks = csv.DictReader(open('tanks.csv', 'r'), delimiter = ';')
    has_tanks = False
    
    try:
        opts, args = getopt.getopt(argv, 'o:t:f:ph', ['operation=', 'target=', 'fields=', 'print', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        if opt in ('-o', '--operation'):
            operation = arg
        if opt in ('-t', '--target'):
            target = arg.split(',')        
            for t in target:
                if t.isdigit() == False:
                    has_tanks = True
        if opt in ('-f', '--fields'):
            fields = arg.split(',')
        if opt in ('-p', '--print'):
            print_tanks(tanks)
            sys.exit(2)
    
    selected = filter(lambda x: filter_func(x, has_tanks, target), tanks)
 
    if len(selected) == 0:
        print "No matching targets!"
        sys.exit(2)

    # Analyze selected tanks    
    
    # First let's find out the best values for armor, penetration, speed, traverse and damage
    top_values(selected)
        
    
if __name__ == '__main__':
    main(sys.argv[1:])
    
    