#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on Feb 23, 2011

@author: mep
'''
from urllib import urlopen
import re
import sys
import getopt

from Eurohockey_Miner import Eurohockey_Miner
from WOT_Miner import WOT_Miner
from CVS_Outputter import CVS_Outputter

fields = []
begin_record = 0
tmp_record = {}
curr_field = ''
next_field = ''

def usage():
    print "Usage:"
    print"\t"

def main(argv):
    miner_name = ''
    params = ''
    
    try:
        opts, args = getopt.getopt(argv, 'm:p:h', ['miner=', 'params=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-m', '--miner'):
            miner_name = arg
        elif opt in ('-p', '--params'):
            params = arg
        else:
            usage()
            sys.exit(2)

    if (miner_name == 'eh'):
        miner = Eurohockey_Miner(params)
    elif (miner_name == 'wot'):
        miner = WOT_Miner(params)
    else:
        usage()
        sys.exit(2)
        
    url_address = miner.base_url
    
    test = re.compile(miner.link_filter)
    
    sub_links = map(lambda x: miner.sub_url(x), map(lambda x: re.search(miner.link_filter,x).group(1), filter(test.search, map(lambda x: x.strip(), urlopen(url_address)))))
    
    for url in sub_links:
        tmp_record = {}
        tmp_record = miner.read_record(urlopen(url))

        if tmp_record != None:         
            fields.append(tmp_record)

    # Format and print the records
    printer = CVS_Outputter(fields)
    print printer

if __name__ == '__main__':
    main(sys.argv[1:])
