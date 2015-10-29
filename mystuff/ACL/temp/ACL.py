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
#ingest file
#create list of unique acls
#create list of unique object-groups
#create list of unique group-objects
#create list of bound acls
#create list of unbound acls
#create dict of acls with entries per acl
#
#
#which object-groups exist in the firewall which are not referenced by an ACL?		list of object-groups, iterate find in any list with access-list
#											also check other object-groups for a group-object reference
#
#determine which acls reference which object groups and which object groups reference each other
#then print the tree backwards so the configuration can be recreated





# IMPORTS

from collections import OrderedDict
from ciscoconfparse import CiscoConfParse
from pprint import pprint
import re

# FUNCTIONS

def ifile(fname):
    with open(fname, 'r') as f:
        mycfg = f.read()
    return mycfg

def cl_unique_acls(mycfg):
    unique_acls = []
    for line in mycfg.split('\n'):
        if 'access-list' in line:
            if line.split(' ')[1] not in unique_acls:
                unique_acls.append(line.split(' ')[1])
    return unique_acls    

def cl_unique_objgroups(mycfg):
    unique_objgroups = []
    for line in mycfg.split('\n'):
         if ('object-group' in line) and ('access-list' not in line):
             unique_objgroups.append(line)
    return unique_objgroups

def cl_unique_grpobjects(mycfg):
    unique_grpobjects = []
    for line in mycfg.split('\n'):
        if 'group-object' in line:
            if line not in unique_grpobjects:
                unique_grpobjects.append(line)
    return unique_grpobjects

def cd_acls(mycfg):
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
    bound_acls = []
    for line in mycfg.split('\n'):
        if 'access-group' in line:
            if line.split(' ')[1] not in bound_acls:
                bound_acls.append(line.split(' ')[1])
    return bound_acls

def cl_unbound_acls(mycfg):
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
    acls = cd_acls(mycfg)
    acl_config = []
    for aclname, aclentries in acls.items():
        for i, aclentry in enumerate(aclentries):
            acl_config.append(aclentry)
    acl_config = '\n'.join(acl_config)
    unique_objgroups = cl_unique_objgroups(mycfg)
    unbound_objgroups = []
    for item in unique_objgroups:
        if ('object-group network' in item):
             item = objgroup_remove_type(item)
             if item not in acl_config:
                 item = objgroup_insert_type(item, 'network')
                 unbound_objgroups.append(item)
        if ('object-group protocol' in item):
            item = objgroup_remove_type(item)
            if item not in acl_config:    
                item = objgroup_insert_type(item, 'protocol')
                unbound_objgroups.append(item) 
        if ('object-group service' in item):
            item = objgroup_remove_type(item)
            if item not in acl_config:    
                item = objgroup_insert_type(item, 'service')
                unbound_objgroups.append(item) 
    return unbound_objgroups

# FORMATTING FUNCTIONS

def objgroup_remove_type(item):
    item = item.split(' ')
    item.pop(1)   
    item = ' '.join(item)
    return item

def objgroup_insert_type(item, type):
    item = item.split(' ')
    item.insert(1, type)           
    item = ' '.join(item)  
    return item

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
