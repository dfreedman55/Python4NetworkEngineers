# IMPORTS

from collections import OrderedDict
from ciscoconfparse import CiscoConfParse
from pprint import pprint
import re

# FILE HANDLING FUNCTIONS

def ingest_file(filename):
    with open('sourcefile.txt', 'r') as f:
        my_config = f.read()
    return my_config

# ACL PROCESSING FUNCTIONS

def create_listuniqueacl(my_config):
    for item in my_config.strip().split('\n'):
        if 'access-list' in item:
            if item.split(' ')[1] not in my_acl_list:
                my_acl_list.append(item.split(' ')[1])

def create_dictacls(my_config, my_acl_list):
    for index, aclname in enumerate(my_acl_list):
        my_current_acl = []
        for line in my_config.strip().split('\n'):
            if my_acl_list[index] in line:
                my_current_acl.append(line)
        in_acl_dict[my_acl_list[index]] = my_current_acl

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

# NETWORK OBJECT-GROUP FUNCTIONS

def create_listobjgrps(filename):
    '''
    Find 'object-group network <name>' objects in configuration file
    '''
    config = CiscoConfParse('sourcefile.txt')
    lines = config.find_objects('object-group')
    mylist = []
    for parent_item in lines:
	if 'access-list' not in parent_item.text:
	    mylist.append(parent_item.text)
    return mylist

def create_dictobjgrps(listobjgrps):
    '''
    Create object group dictionary where keys are individual 'object-group network <name>' strings and values are the corresponding list of children configuration lines
    '''
    for objgrp in listobjgrps:
        config = CiscoConfParse('sourcefile.txt')
        lines = config.find_objects(objgrp)
        listobjgrps = []
        for parent_item in lines:
            for child_item in parent_item.all_children:
                listobjgrps.append(child_item.text)
            dictobjgrps[parent_item.text] = listobjgrps

def print_dictobjgrps(dictnetobjgrps):
    '''
    For all items in object group dictionary, print the keys and the associated child values
    '''
    for k,v in dictobjgrps.items():
        print k
        for i,v in enumerate(v):
            print v

def print_netobj(dictobjgrps,netobj):
    '''
    Print a specific network object-group from the dictionary
    '''
    print netobj
    for item in dictobjgrps.get(netobj):
        print item

# MAIN

my_config = ingest_file('sourcefile.txt')						# ingest source configuration file (.txt)

my_acl_list = []									# define a list for unique ACLs names
create_listuniqueacl(my_config)								# populate list with unique ACL names

in_acl_dict = {}									# define a dictionary for ACLs
create_dictacls(my_config, my_acl_list)							# populate dictionary with ACLs

listintfacls = create_listintfacls('sourcefile.txt')					# create a list of interface ACLs
dictintfacls = {}									# define a dictionary for the interface ACLs
create_dictintfacls(listintfacls)			                		# populate dictionary with interface ACLs

listobjgrps = create_listobjgrps('sourcefile.txt')					# create a list of network object-groups
dictobjgrps = {}									# define a dictionary for network object-groups
create_dictobjgrps(listobjgrps)								# populate dictionary with network object-groups

# OUTPUT EXAMPLES

print ''
print 'PRINT ACL DICTIONARY'
pprint(in_acl_dict)
print ''

print 'PRETTY PRINT THE DICTIONARY OF NETWORK OBJECT-GROUPS:\n'
pprint(dictobjgrps)									# pretty print the dictionary of network object-groups
print ''

print 'ITERATE THROUGH THE DICTIONARY OF NETWORK OBJECT-GROUPS:\n'
print_dictobjgrps(dictobjgrps)								# iterate through the dictionary of network object-groups
print ''

print 'PRINT A SPECIFIC NETWORK OBJECT-GROUP FROM THE DICTIONARY:\n'
print_netobj(dictobjgrps, 'object-group network gr-proview-application-services')	# print a specific network object-group from the dictionary
print ""

print 'PRETTY PRINT THE DICTIONARY OF INTERFACE ACLS:\n'				# pretty print the dictionary of interface ACLs
pprint(dictintfacls)
print ''

print 'ITERATE THROUGH THE DICTIONARY OF INTERFACE ACLS:\n'				# iterate through the dictionary of interface ACLs
print_dictintfacls(dictintfacls)
print ''

print 'PRINT A SPECIFIC INTERFACE ACL FROM THE DICTIONARY:\n'				# print a specific interface ACL binding
print_intfacl(dictintfacls, 'outside')
print ''




####################################################################################################################################################
#
#(applied_python)[dfreedman@ip-172-30-0-111 ACL]$ cat ACL.py 
#
# FUNCTIONS
#
#def find_og_members(groupname):
#    config = CiscoConfParse('sourcefile.txt')
#    lines = config.find_objects(groupname)
#    my_og_dict = OrderedDict()
#    i = 0
#    for parent_item in lines:
#        if 'access-list' not in parent_item.text:
#            print parent_item.text
#            my_og_dict[i] = parent_item.text
#            i += 1
#            for child_item in parent_item.all_children:
#                if 'group-object' in child_item.text:
#                    #print child_item.text
#                    go_name = child_item.text.strip().split(' ')[1]
#                    go_return = find_og_members(go_name)
#                    my_og_dict[i] = go_return
#                    #print parent_item.text
#                else:
#                    my_og_dict[i] = child_item.text
#                    #print child_item.text
#                i += 1
#    return my_og_dict
#
## INGEST ORIGINAL .TXT FILE
#with open('sourcefile.txt', 'r') as f:
#    my_temp_config = f.read()
#
## WRITE STANDARDIZED .TXT FILE (ACL FORMATTING LOWERCASE)      # remove this:  OUTSIDE_IN is not the same as OUTSIDE_in (only one can be applied to interface)
#with open('standardized.txt', 'w') as f:
#    for item in my_temp_config.strip().split('\n'):
#        f.write(item.lower() + '\n')
#
## INGEST STANDARDIZED .TXT FILE
#with open('standardized.txt', 'r') as f:
#    my_config = f.read()
#


# INGEST ORIGINAL .TXT FILE
with open('sourcefile.txt', 'r') as f:
    my_config = f.read()

# DETERMINE UNIQUE ACLS
my_acl_list = []                                                # UNIQUE ACL NAMES LISTED IN THE ORDER IN WHICH THEY ARE ENCOUNTERED IN THE CONFIGURATION
for item in my_config.strip().split('\n'):
    if 'access-list' in item:
        if item.split(' ')[1] not in my_acl_list:
            my_acl_list.append(item.split(' ')[1])

# FOR EACH ACL CREATE CONFIG CROSS SECTION
in_acl_dict = {}
for index, aclname in enumerate(my_acl_list):
    my_current_acl = []
    for line in my_config.strip().split('\n'):
        if my_acl_list[index] in line:
            my_current_acl.append(line)
    in_acl_dict[my_acl_list[index]] = my_current_acl

pprint(in_acl_dict)
#
#for item in in_acl_dict['outside_in']:
#    print item
#
#
#

# FOR EACH ACL DETERMINE COMPONENT PARTS OF CURRENT ACL
#




out_acl_dict = {}
for aclname, aclentries in in_acl_dict.items():                 # FOR EACH ACLNAME/LISTOFACLENTRIES IN {DICTIONARY}
    #print aclname                                              # PRINT ACLNAME
    for index, aclentry in enumerate(aclentries):               # FOR EACH INDEX/ACLENTRY IN [LISTOFACLENTRIES]
        #print index, aclentry                                  # PRINT INDEX ACLENTRY

        my_acl_objects = re.search(r'access-list (.+?) extended permit (.+?) (.+?) (.+?) (.+?) (.+?) (.+)', aclentry)
        print my_acl_objects




#       print 'FULL: %s' % my_acl_objects.group(0)
#       print 'NAME: %s' % my_acl_objects.group(1)
#       print 'SRC: %s' % my_acl_objects.group(2)
#       print 'VAL: %s' % my_acl_objects.group(3)
#       print 'DST: %s' % my_acl_objects.group(4)
#       print 'VAL: %s' % my_acl_objects.group(5)
#       print 'PRT: %s' % my_acl_objects.group(6)
#       print 'VAL: %s' % my_acl_objects.group(7)
#       print '\n'
#
#        if 'object-group' not in aclentry:
#               print 'ADD ACL AS IS TO DICTIONARY'
#               print 'ACLENTRY: %s' % aclentry
#               print '\n'

        if ('object-group' in aclentry) and (aclentry.count('object-group') == 3) and ('object-group' in my_acl_objects.group(2)) and ('object-group' in my_acl_objects.group(4)) and ('object-group' in my_acl_objects.group(6)):
                print 'IDENTIFY SRC AND DST AND PRT OBJECT GROUPS'
                print 'ACLENTRY: %s' % aclentry
                print 'SRC: %s' % my_acl_objects.group(3)
                print 'DST: %s' % my_acl_objects.group(5)
                print 'PRT: %s' % my_acl_objects.group(7)
                src_og = find_og_members(my_acl_objects.group(3))
                dst_og = find_og_members(my_acl_objects.group(5))
                prt_og = find_og_members(my_acl_objects.group(7))
                print '\n'
                print src_og
                print dst_og
                print prt_og

#       if ('object-group' in aclentry) and (aclentry.count('object-group') == 2) and ('object-group' in my_acl_objects.group(2)) and ('object-group' in my_acl_objects.group(4)) and ('object-group' not in my_acl_objects.group(6)):
#               print 'IDENTIFY SRC AND DST OBJECT GROUPS'
#               print 'ACLENTRY: %s' % aclentry
#               print 'SRC: %s' % my_acl_objects.group(3)
#               print 'DST: %s' % my_acl_objects.group(5)
#               print 'PRT: %s' % my_acl_objects.group(7)
#               src_og = find_og_members(my_acl_objects.group(3))
#               dst_og = find_og_members(my_acl_objects.group(5))
#               print '\n'
#
#       if ('object-group' in aclentry) and (aclentry.count('object-group') == 2) and ('object-group' in my_acl_objects.group(2)) and ('object-group' not in my_acl_objects.group(4)) and ('object-group' in my_acl_objects.group(6)):
#               print 'IDENTIFY SRC AND PRT OBJECT GROUPS'
#               print 'ACLENTRY: %s' % aclentry
#               print 'SRC: %s' % my_acl_objects.group(3)
#               print 'DST: %s' % my_acl_objects.group(5)
#               print 'PRT: %s' % my_acl_objects.group(7)
#               src_og = find_og_members(my_acl_objects.group(3))
#               prt_og = find_og_members(my_acl_objects.group(7))
#               print '\n'
#
#       if ('object-group' in aclentry) and (aclentry.count('object-group') == 2) and ('object-group' not in my_acl_objects.group(2)) and ('object-group' in my_acl_objects.group(4)) and ('object-group' in my_acl_objects.group(6)):
#               print 'IDENTIFY DST AND PRT OBJECT GROUPS'
#               print 'ACLENTRY: %s' % aclentry
#               print 'SRC: %s' % my_acl_objects.group(3)
#               print 'DST: %s' % my_acl_objects.group(5)
#               print 'PRT: %s' % my_acl_objects.group(7)
#               dst_og = find_og_members(my_acl_objects.group(5))
#               prt_og = find_og_members(my_acl_objects.group(7))
#               print '\n'
#
#       if ('object-group' in aclentry) and (aclentry.count('object-group') == 1) and ('object-group' in my_acl_objects.group(2)) and ('object-group' not in my_acl_objects.group(4)) and ('object-group' not in my_acl_objects.group(6)):
#               print 'IDENTIFY SRC OBJECT GROUP'
#               print 'ACLENTRY: %s' % aclentry
#               print 'SRC: %s' % my_acl_objects.group(3)
#               print 'DST: %s' % my_acl_objects.group(5)
#               print 'PRT: %s' % my_acl_objects.group(7)
#               src_og = find_og_members(my_acl_objects.group(3))
#               print '\n'
#
#       if ('object-group' in aclentry) and (aclentry.count('object-group') == 1) and ('object-group' not in my_acl_objects.group(2)) and ('object-group' in my_acl_objects.group(4)) and ('object-group' not in my_acl_objects.group(6)):
#               print 'IDENTIFY DST OBJECT GROUP'
#               print 'ACLENTRY: %s' % aclentry
#               print 'SRC: %s' % my_acl_objects.group(3)
#               print 'DST: %s' % my_acl_objects.group(5)
#               print 'PRT: %s' % my_acl_objects.group(7)
#               dst_og = find_og_members(my_acl_objects.group(5))
#               print '\n'
#
#       if ('object-group' in aclentry) and (aclentry.count('object-group') == 1) and ('object-group' not in my_acl_objects.group(2)) and ('object-group' not in my_acl_objects.group(4)) and ('object-group' in my_acl_objects.group(6)):
#               print 'IDENTIFY PRT OBJECT GROUP'
#               print 'ACLENTRY: %s' % aclentry
#               print 'SRC: %s' % my_acl_objects.group(3)
#               print 'DST: %s' % my_acl_objects.group(5)
#               print 'PRT: %s' % my_acl_objects.group(7)
#               prt_og = find_og_members(my_acl_objects.group(7))
#               print '\n'
#
#
#
#
#
#
#
#
#
#
#
#
# TEMPLATE ACL
#myacl = 'access-list Customer_access_in extended permit object-group gr-proview-application-services object-group DM_INLINE_NETWORK_42 object-group gr-proview-servers'
#
#                                 1                       2     3     4     5     6     7
#mylist = re.search(r'access-list (.+?) extended permit (.+?) (.+?) (.+?) (.+?) (.+?) (.+)', myacl)
#                                 name                   src   val   dst   val   prt   val
#>>> mylist.group(0)
#'access-list Customer_access_in extended permit object-group gr-proview-application-services object-group DM_INLINE_NETWORK_42 object-group gr-proview-servers'
#>>> mylist.group(1)
#'Customer_access_in'
#>>> mylist.group(2)
#'object-group'
#>>> mylist.group(3)
#'gr-proview-application-services'
#>>> mylist.group(4)
#'object-group'
#>>> mylist.group(5)
#'DM_INLINE_NETWORK_42'
#>>> mylist.group(6)
#'object-group'
#>>> mylist.group(7)
#'gr-proview-servers'
#>>>
#consider using CiscoConfParse parent/child relationship for this
#out_acl_dict = OrderedDict{'dmz_in': [ {source: [objects], destination: [objects], ports: [objects]} ] }

