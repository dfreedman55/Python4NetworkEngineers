# IMPORTS

from collections import OrderedDict
from ciscoconfparse import CiscoConfParse
from pprint import pprint
import re

# INTERFACE ACL FUNCTIONS

def create_listintfacls(filename):
    '''
    Find 'access-group' objects in configuration file
    '''
    config = CiscoConfParse('sourcefile.txt')
    lines = config.find_objects('access-group')
    mylist = []
    for parent_item in lines:
        mylist.append(parent_item.text)
    return mylist

def create_dictintfacls(listintfacls):
    '''
    Create interface ACLs dictionary where keys are individual interfaces and values are the corresponding ACLs bound to those interfaces
    '''
    for intfacl in listintfacls:
        config = CiscoConfParse('sourcefile.txt')
        lines = config.find_objects(intfacl)
        for parent_item in lines:
            dictintfacls[parent_item.text.split(' ')[4]] = parent_item.text.split(' ')[1]

def print_dictintfacls(dictintfacls):
    '''
    For all items in the interface ACLs dictionary, print the keys and the associated child values
    '''
    for k,v in dictintfacls.items():
        print k, v

def print_intfacl(dictintfacls,intfacl):
    '''
    Print a specific interface ACL from the dictionary
    '''
    print '%s: %s' % (intfacl, dictintfacls[intfacl])
#    for item in dictintfacls.get(intfacl):
#        print item

# NETWORK OBJECT-GROUP FUNCTIONS

def create_listnetobjgrps(filename):
    '''
    Find 'object-group network <name>' objects in configuration file
    '''
    config = CiscoConfParse('sourcefile.txt')
    lines = config.find_objects('object-group network')
    mylist = []
    for parent_item in lines:
        mylist.append(parent_item.text)
    return mylist

def create_dictnetobjgrps(listnetobjgrps):
    '''
    Create object group dictionary where keys are individual 'object-group network <name>' strings and values are the corresponding list of children configuration lines
    '''
    for objgrp in listnetobjgrps:
        config = CiscoConfParse('sourcefile.txt')
        lines = config.find_objects(objgrp)
        listnetobjgrps = []
        for parent_item in lines:
            for child_item in parent_item.all_children:
                listnetobjgrps.append(child_item.text)
            dictnetobjgrps[parent_item.text] = listnetobjgrps

def print_dictnetobjgrps(dictnetobjgrps):
    '''
    For all items in object group dictionary, print the keys and the associated child values
    '''
    for k,v in dictnetobjgrps.items():
        print k
        for i,v in enumerate(v):
            print v

def print_netobj(dictnetobjgrps,netobj):
    '''
    Print a specific network object-group from the dictionary
    '''
    print netobj
    for item in dictnetobjgrps.get(netobj):
        print item

# MAIN

listintfacls = create_listintfacls('sourcefile.txt')					# UNTESTED:  create a list of interface ACLs
dictintfacls = {}									# UNTESTED:  define a dictionary for the interface ACLs
create_dictintfacls(listintfacls)			                		# UNTESTED:  populate dictionary with interface ACLs

listnetobjgrps = create_listnetobjgrps('sourcefile.txt')				# create a list of network object-groups
dictnetobjgrps = {}									# define a dictionary for network object-groups
create_dictnetobjgrps(listnetobjgrps)							# populate dictionary with network object-groups

# OUTPUT EXAMPLES

print ''
print 'PRETTY PRINT THE DICTIONARY OF NETWORK OBJECT-GROUPS:\n'
pprint(dictnetobjgrps)									# pretty print the dictionary of network object-groups
print ''

print 'ITERATE THROUGH THE DICTIONARY OF NETWORK OBJECT-GROUPS:\n'
print_dictnetobjgrps(dictnetobjgrps)							# iterate through the dictionary of network object-groups
print ''

print 'PRINT A SPECIFIC NETWORK OBJECT-GROUP FROM THE DICTIONARY:\n'
print_netobj(dictnetobjgrps, 'object-group network gr-proview-application-services')	# print a specific network object-group from the dictionary
print ""

print 'PRETTY PRINT THE DICTIONARY OF INTERFACE ACLS:\n'				# UNTESTED
pprint(dictintfacls)
print ''

print 'INTERATE THROUGH THE DICTIONARY OF INTERFACE ACLS:\n'
print_dictintfacls(dictintfacls)
print ''

print 'PRINT A SPECIFIC INTERFACE ACL FROM THE DICTIONARY:\n'
print_intfacl(dictintfacls, 'outside')
print ''
