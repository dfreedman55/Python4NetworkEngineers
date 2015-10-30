#ifile = ingest file
#sfile = standardize file
#cl = create list
#cd = create dict
#cod = create ordered dict
#pl = print list
#pd = print dict
#pod = print ordered dict
#find = find
#
#DONE
#ingest file
#create list of unique acls
#create list of unique object-groups
#create list of unique group-objects
#create list of bound acls
#create list of unbound acls
#create dict of acls with entries per acl
#create list of object-groups with same name but different types
#
# PENDING
#
#determine which acls reference which object groups and which object groups reference each other
#then print the tree backwards so the configuration can be recreated
#
#create function to rename object groups based on type * (complex)
#	 - have to create a duplicate object group under a new name
#	 - create a new acl line which refers to that new object group
#        - remove old acl referring to old object group
#        - remove old object group
#        - do this one object group at a time for the entire configuration

# IMPORTS

from collections import OrderedDict
#from ciscoconfparse import CiscoConfParse
from pprint import pprint
import re

# FUNCTIONS

def ifile(fname):
    '''
    Ingest file and return as variable mycfg
    '''
    with open(fname, 'r') as f:
        mycfg = f.read()
    return mycfg

def cl_unique_acls(mycfg):
    '''
    Create list of unique ACL names within the configuration
    '''
    unique_acls = []
    for line in mycfg.split('\n'):
        if 'access-list' in line:
            if line.split(' ')[1] not in unique_acls:
                unique_acls.append(line.split(' ')[1])
    return unique_acls    

def cl_unique_objgroups(mycfg):
    '''
    Create list of unique object-groups within the configuration
    '''
    unique_objgroups = []
    for line in mycfg.split('\n'):
         if ('object-group' in line) and ('access-list' not in line):
             unique_objgroups.append(line)
    return unique_objgroups

def cl_unique_grpobjects(mycfg):
    '''
    Create list of unique group-objects (nested object-groups) within the configuration
    '''
    unique_grpobjects = []
    for line in mycfg.split('\n'):
        if 'group-object' in line:
            if line not in unique_grpobjects:
                unique_grpobjects.append(line)
    return unique_grpobjects

def cd_acls(mycfg):
    '''
    Create dictionary of ACLs and their respective ACL entries
    '''
    unique_acls = cl_unique_acls(mycfg)
    acls = {}
    for index, aclname in enumerate(unique_acls):
        current_acl = []
        for line in mycfg.strip().split('\n'):
            if (unique_acls[index] in line) and ('access-group' not in line):
                current_acl.append(line)
        acls[unique_acls[index]] = current_acl
    return acls

def cl_bound_acls(mycfg):
    '''
    Create list of ACLs which are actually bound to interfaces
    '''
    bound_acls = []
    for line in mycfg.split('\n'):
        if 'access-group' in line:
            if line.split(' ')[1] not in bound_acls:
                bound_acls.append(line.split(' ')[1])
    return bound_acls

def cl_unbound_acls(mycfg):
    '''
    Create list of ACLs which are not actually bound to interfaces
    '''
    unique_acls = cl_unique_acls(mycfg)
    bound_acls = cl_bound_acls(mycfg)
    unbound_acls = []
    for item in unique_acls:
        if item in bound_acls:
            pass
        else:
            unbound_acls.append(item)
    return unbound_acls

def cl_unbound_objgroups(mycfg):
    '''
    Create list of object groups which are not referenced directly by an ACL (unbound object group list) - for loop
    Object groups referenced indirectly by other object groups (nested) are bound (remove from unbound object group list) - while loop
    '''
    acl_config = create_config_from_acl_dict()
    unique_grpobjects = cl_unique_grpobjects(mycfg)
    unique_objgroups = cl_unique_objgroups(mycfg)
    unbound_objgroups = []
    for item in unique_objgroups:
        if ('object-group' in item):
            track_type = item.split(' ')[1]
            item = objgroup_remove_type(item)
            if item not in acl_config:
                item = objgroup_insert_type(item, track_type)
                unbound_objgroups.append(item)
    i = 0
    while i < len(unbound_objgroups):
        for item in unbound_objgroups:
            if ('  group-object ' + item.split(' ')[2]) in unique_grpobjects:
                unbound_objgroups.remove(item)
                i += 1
            else:
                i = 0
    return unbound_objgroups

def cl_duplicate_objgroup_names(mycfg):
    ''' 
    Create list of object-groups which have different <types> (network/protocol/service) but the same <name>
    Ideally these items should be fixed because they can cause problems with the rest of the functionality of this script
    '''
    unique_objgroups = cl_unique_objgroups(mycfg)
    temp = '\n'.join(unique_objgroups)
    unique_names = []						
    identify_duplicates = []					
    duplicate_names = []				
    for item in temp.split('\n'):				# look through all object-group names in the list of unique_objgroups
        if item.split(' ')[2] not in unique_names:
            unique_names.append(item.split(' ')[2])		# if you've never encountered that object-group name before, store the name in this list
        else:
            identify_duplicates.append(item.split(' ')[2])	# if you've seen encountered that object-group name before, store the name in this list (duplicate identified)
    for item in identify_duplicates:				# create and return list of duplicates
        for objgroup in unique_objgroups:
            if item in objgroup:
                duplicate_names.append(objgroup)
    return duplicate_names
   
# FORMATTING FUNCTIONS

def objgroup_remove_type(item):
    '''
    Remove <type> from "object-group <type> <name>" before comparison to the group-objects list
    '''
    item = item.split(' ')
    item.pop(1)   
    item = ' '.join(item)
    return item

def objgroup_insert_type(item, type):
    '''
    Insert <type> into "object-group <type> <name>" after comparison to the group-objects list
    '''
    item = item.split(' ')
    item.insert(1, type)           
    item = ' '.join(item)  
    return item

def create_config_from_acl_dict():
    '''
    Create a list of all ACL entries within the ACL dictionary and join the items in the list to create a cohesive representation of the entire ACL configuration
    '''
    acls = cd_acls(mycfg)
    acl_config = []
    for aclname, aclentries in acls.items():
        for i, aclentry in enumerate(aclentries):
            acl_config.append(aclentry)
    acl_config = '\n'.join(acl_config)
    return acl_config

# MAIN

mycfg = ifile('sourcefile.txt')
print '%s:\n%s\n' % ('UNIQUE ACLS', cl_unique_acls(mycfg))
print 'ACLS:'
pprint(cd_acls(mycfg))
print ''
print '%s:\n%s\n' % ('UNIQUE OBJECT GROUPS', cl_unique_objgroups(mycfg))
print '%s:\n%s\n' % ('UNIQUE GROUP OBJECTS', cl_unique_grpobjects(mycfg))
print '%s:\n%s\n' % ('BOUND ACLS', cl_bound_acls(mycfg))
print '%s:\n%s\n' % ('UNBOUND ACLS', cl_unbound_acls(mycfg))
print '%s:\n%s\n' % ('UNBOUND OBJECT GROUPS', cl_unbound_objgroups(mycfg))
print '%s:\n%s\n' % ('DUPLICATE OBJECT GROUP NAMES', cl_duplicate_objgroup_names(mycfg))
