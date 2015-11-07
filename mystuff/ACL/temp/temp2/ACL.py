# INITIALIZATION


from collections import OrderedDict
from ciscoconfparse import CiscoConfParse
# from pprint import pprint
# import re

nog_done = False
sog_done = False
pog_done = False

inputfile = raw_input('Type name of source file:')

# ACL FUNCTIONS


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


def create_config_from_acl_dict():
    '''
    Create a list of all ACL entries within the ACL dictionary
    Join the items in the list to create a cohesive representation of config
    '''
    acls = cd_acls(mycfg)
    acl_config = []
    for aclname, aclentries in acls.items():
        for i, aclentry in enumerate(aclentries):
            acl_config.append(aclentry)
    acl_config = '\n'.join(acl_config)
    return acl_config


def cl_unique_grpobjects(mycfg):
    '''
    Create list of unique group-objects (nested) within the configuration
    '''
    unique_grpobjects = []
    for line in mycfg.split('\n'):
        if 'group-object' in line:
            if line not in unique_grpobjects:
                unique_grpobjects.append(line)
    return unique_grpobjects


def cl_unique_objgroups(mycfg):
    '''
    Create list of unique object-groups within the configuration
    '''
    unique_objgroups = []
    for line in mycfg.split('\n'):
        if ('object-group' in line) and ('access-list' not in line):
            unique_objgroups.append(line)
    return unique_objgroups


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
    Create list of object groups which are not referenced directly by an ACL
    (unbound object group list) - for loop
    Object groups referenced indirectly by other object groups are bound
    (remove from unbound object group list) - while loop
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


# FORMATTING FUNCTIONS

def objgroup_remove_type(item):
    '''
    Remove <type> from "object-group <type> <name>"
    Before comparison to the group-objects list
    '''
    item = item.split(' ')
    item.pop(1)
    item = ' '.join(item)
    return item


def objgroup_insert_type(item, type):
    '''
    Insert <type> into "object-group <type> <name>"
    After comparison to the group-objects list
    '''
    item = item.split(' ')
    item.insert(1, type)
    item = ' '.join(item)
    return item


# NETWORK OBJECT GROUP FUNCTIONS


def nog_cd(filename):
    nog_all = {}
    mycfg = CiscoConfParse(filename)
    lines = mycfg.find_objects(r'^object-group network')
    if lines != []:
        for parent_item in lines:
            list_child_items = []
            for child_item in parent_item.all_children:
                list_child_items.append(child_item.text)
            nog_all[parent_item.text] = list_child_items
    lines = mycfg.find_objects(r'^object network')
    if lines != []:
        for parent_item in lines:
            list_child_items = []
            for child_item in parent_item.all_children:
                list_child_items.append(child_item.text)
            nog_all[parent_item.text] = list_child_items
    return nog_all


def nog_sep(nog_all):
    nog_dep_none = OrderedDict()
    nog_dep = OrderedDict()
    for parent_item, list_child_items in nog_all.items():
        no_dependency = True
        count = 0
        for item in list_child_items:
            if ('group-object' in item) or ('network-object' in item):
                count += 1
                no_dependency = False
                if count == 1:
                    nog_dep[parent_item] = list_child_items
        if no_dependency:
            nog_dep_none[parent_item] = list_child_items
    return [nog_dep_none, nog_dep]


def nog_sep_l2(nog_dep_none, nog_dep):
    if nog_dep.keys() != []:
        global nog_done
        nog_dep_l2 = OrderedDict()
        for parent_item, list_child_items in nog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('network-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group network ' + item.strip().split(' ')[1]
                if 'network-object object' in item:
                    name = 'object network ' + item.strip().split(' ')[2]
                if name in nog_dep_none.keys():
                    nog_dep_l2[parent_item] = list_child_items
                    if nog_dep.get(parent_item) is not None:
                        nog_dep.pop(parent_item)
        if nog_dep.keys() == []:
            nog_done = True
        return [nog_dep, nog_dep_l2]


def nog_sep_l3(nog_dep, l2_items):
    if nog_dep.keys() != []:
        global nog_done
        nog_dep_l3 = OrderedDict()
        for parent_item, list_child_items in nog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('network-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group network ' + item.strip().split(' ')[1]
                if 'network-object object' in item:
                    name = 'object network ' + item.strip().split(' ')[2]
                if name in l2_items.keys():
                    nog_dep_l3[parent_item] = list_child_items
                    if nog_dep.get(parent_item) is not None:
                        nog_dep.pop(parent_item)
        if nog_dep.keys() == []:
            nog_done = True
        return [nog_dep, nog_dep_l3]


def nog_sep_l4(nog_dep, l3_items):
    if nog_dep.keys() != []:
        global nog_done
        nog_dep_l4 = OrderedDict()
        for parent_item, list_child_items in nog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('network-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group network ' + item.strip().split(' ')[1]
                if 'network-object object' in item:
                    name = 'object network ' + item.strip().split(' ')[2]
                if name in l3_items.keys():
                    nog_dep_l4[parent_item] = list_child_items
                    if nog_dep.get(parent_item) is not None:
                        nog_dep.pop(parent_item)
        if nog_dep.keys() == []:
            nog_done = True
        return [nog_dep, nog_dep_l4]


def nog_sep_l5(nog_dep, l4_items):
    if nog_dep.keys() != []:
        global nog_done
        nog_dep_l5 = OrderedDict()
        for parent_item, list_child_items in nog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('network-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group network ' + item.strip().split(' ')[1]
                if 'network-object object' in item:
                    name = 'object network ' + item.strip().split(' ')[2]
                if name in l4_items.keys():
                    nog_dep_l5[parent_item] = list_child_items
                    if nog_dep.get(parent_item) is not None:
                        nog_dep.pop(parent_item)
        if nog_dep.keys() == []:
            nog_done = True
        return [nog_dep, nog_dep_l5]


def nog_sep_l6(nog_dep, l5_items):
    if nog_dep.keys() != []:
        global nog_done
        nog_dep_l6 = OrderedDict()
        for parent_item, list_child_items in nog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('network-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group network ' + item.strip().split(' ')[1]
                if 'network-object object' in item:
                    name = 'object network ' + item.strip().split(' ')[2]
                if name in l5_items.keys():
                    nog_dep_l6[parent_item] = list_child_items
                    if nog_dep.get(parent_item) is not None:
                        nog_dep.pop(parent_item)
        if nog_dep.keys() == []:
            nog_done = True
        return [nog_dep, nog_dep_l6]


def nog_sep_l7(nog_dep, l6_items):
    if nog_dep.keys() != []:
        global nog_done
        nog_dep_l7 = OrderedDict()
        for parent_item, list_child_items in nog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('network-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group network ' + item.strip().split(' ')[1]
                if 'network-object object' in item:
                    name = 'object network ' + item.strip().split(' ')[2]
                if name in l6_items.keys():
                    nog_dep_l7[parent_item] = list_child_items
                    if nog_dep.get(parent_item) is not None:
                        nog_dep.pop(parent_item)
        if nog_dep.keys() == []:
            nog_done = True
        return [nog_dep, nog_dep_l7]


def nog_sep_l8(nog_dep, l7_items):
    if nog_dep.keys() != []:
        global nog_done
        nog_dep_l8 = OrderedDict()
        for parent_item, list_child_items in nog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('network-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group network ' + item.strip().split(' ')[1]
                if 'network-object object' in item:
                    name = 'object network ' + item.strip().split(' ')[2]
                if name in l7_items.keys():
                    nog_dep_l8[parent_item] = list_child_items
                    if nog_dep.get(parent_item) is not None:
                        nog_dep.pop(parent_item)
        if nog_dep.keys() == []:
            nog_done = True
        return [nog_dep, nog_dep_l8]


# SERVICE OBJECT GROUP FUNCTIONS


def sog_cd(filename):
    sog_all = {}
    mycfg = CiscoConfParse(filename)
    lines = mycfg.find_objects(r'^object-group service')
    if lines != []:
        for parent_item in lines:
            list_child_items = []
            for child_item in parent_item.all_children:
                list_child_items.append(child_item.text)
            sog_all[parent_item.text] = list_child_items
    lines = mycfg.find_objects(r'^object service')
    if lines != []:
        for parent_item in lines:
            list_child_items = []
            for child_item in parent_item.all_children:
                list_child_items.append(child_item.text)
            sog_all[parent_item.text] = list_child_items
    return sog_all


def sog_sep(sog_all):
    sog_dep_none = OrderedDict()
    sog_dep = OrderedDict()
    for parent_item, list_child_items in sog_all.items():
        no_dependency = True
        count = 0
        for item in list_child_items:
            if ('group-object' in item) or ('service-object' in item):
                count += 1
                no_dependency = False
                if count == 1:
                    sog_dep[parent_item] = list_child_items
        if no_dependency:
            sog_dep_none[parent_item] = list_child_items
    return [sog_dep_none, sog_dep]


def sog_sep_l2(sog_dep_none, sog_dep):
    if sog_dep.keys() != []:
        global sog_done
        sog_dep_l2 = OrderedDict()
        for parent_item, list_child_items in sog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('service-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group service ' + item.strip().split(' ')[1]
                if 'service-object object' in item:
                    name = 'object service ' + item.strip().split(' ')[2]
                if name in sog_dep_none.keys():
                    sog_dep_l2[parent_item] = list_child_items
                    if sog_dep.get(parent_item) is not None:
                        sog_dep.pop(parent_item)
        if sog_dep.keys() == []:
            sog_done = True
        return [sog_dep, sog_dep_l2]


def sog_sep_l3(sog_dep, l2_items):
    if sog_dep.keys() != []:
        global sog_done
        sog_dep_l3 = OrderedDict()
        for parent_item, list_child_items in sog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('service-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group service ' + item.strip().split(' ')[1]
                if 'service-object object' in item:
                    name = 'object service ' + item.strip().split(' ')[2]
                if name in l2_items.keys():
                    sog_dep_l3[parent_item] = list_child_items
                    if sog_dep.get(parent_item) is not None:
                        sog_dep.pop(parent_item)
        if sog_dep.keys() == []:
            sog_done = True
        return [sog_dep, sog_dep_l3]


def sog_sep_l4(sog_dep, l3_items):
    if sog_dep.keys() != []:
        global sog_done
        sog_dep_l4 = OrderedDict()
        for parent_item, list_child_items in sog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('service-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group service ' + item.strip().split(' ')[1]
                if 'service-object object' in item:
                    name = 'object service ' + item.strip().split(' ')[2]
                if name in l3_items.keys():
                    sog_dep_l4[parent_item] = list_child_items
                    if sog_dep.get(parent_item) is not None:
                        sog_dep.pop(parent_item)
        if sog_dep.keys() == []:
            sog_done = True
        return [sog_dep, sog_dep_l4]


def sog_sep_l5(sog_dep, l4_items):
    if sog_dep.keys() != []:
        global sog_done
        sog_dep_l5 = OrderedDict()
        for parent_item, list_child_items in sog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('service-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group service ' + item.strip().split(' ')[1]
                if 'service-object object' in item:
                    name = 'object service ' + item.strip().split(' ')[2]
                if name in l4_items.keys():
                    sog_dep_l5[parent_item] = list_child_items
                    if sog_dep.get(parent_item) is not None:
                        sog_dep.pop(parent_item)
        if sog_dep.keys() == []:
            sog_done = True
        return [sog_dep, sog_dep_l5]


def sog_sep_l6(sog_dep, l5_items):
    if sog_dep.keys() != []:
        global sog_done
        sog_dep_l6 = OrderedDict()
        for parent_item, list_child_items in sog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('service-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group service ' + item.strip().split(' ')[1]
                if 'service-object object' in item:
                    name = 'object service ' + item.strip().split(' ')[2]
                if name in l5_items.keys():
                    sog_dep_l6[parent_item] = list_child_items
                    if sog_dep.get(parent_item) is not None:
                        sog_dep.pop(parent_item)
        if sog_dep.keys() == []:
            sog_done = True
        return [sog_dep, sog_dep_l6]


def sog_sep_l7(sog_dep, l6_items):
    if sog_dep.keys() != []:
        global sog_done
        sog_dep_l7 = OrderedDict()
        for parent_item, list_child_items in sog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('service-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group service ' + item.strip().split(' ')[1]
                if 'service-object object' in item:
                    name = 'object service ' + item.strip().split(' ')[2]
                if name in l6_items.keys():
                    sog_dep_l7[parent_item] = list_child_items
                    if sog_dep.get(parent_item) is not None:
                        sog_dep.pop(parent_item)
        if sog_dep.keys() == []:
            sog_done = True
        return [sog_dep, sog_dep_l7]


def sog_sep_l8(sog_dep, l7_items):
    if sog_dep.keys() != []:
        global sog_done
        sog_dep_l8 = OrderedDict()
        for parent_item, list_child_items in sog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('service-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group service ' + item.strip().split(' ')[1]
                if 'service-object object' in item:
                    name = 'object service ' + item.strip().split(' ')[2]
                if name in l7_items.keys():
                    sog_dep_l8[parent_item] = list_child_items
                    if sog_dep.get(parent_item) is not None:
                        sog_dep.pop(parent_item)
        if sog_dep.keys() == []:
            sog_done = True
        return [sog_dep, sog_dep_l8]


# PROTOCOL OBJECT GROUP FUNCTIONS


def pog_cd(filename):
    pog_all = {}
    mycfg = CiscoConfParse(filename)
    lines = mycfg.find_objects(r'^object-group protocol')
    if lines != []:
        for parent_item in lines:
            list_child_items = []
            for child_item in parent_item.all_children:
                list_child_items.append(child_item.text)
            pog_all[parent_item.text] = list_child_items
    lines = mycfg.find_objects(r'^object protocol')
    if lines != []:
        for parent_item in lines:
            list_child_items = []
            for child_item in parent_item.all_children:
                list_child_items.append(child_item.text)
            pog_all[parent_item.text] = list_child_items
    return pog_all


def pog_sep(pog_all):
    pog_dep_none = OrderedDict()
    pog_dep = OrderedDict()
    for parent_item, list_child_items in pog_all.items():
        no_dependency = True
        count = 0
        for item in list_child_items:
            if ('group-object' in item) or ('protocol-object' in item):
                count += 1
                no_dependency = False
                if count == 1:
                    pog_dep[parent_item] = list_child_items
        if no_dependency:
            pog_dep_none[parent_item] = list_child_items
    return [pog_dep_none, pog_dep]


def pog_sep_l2(pog_dep_none, pog_dep):
    if pog_dep.keys() != []:
        global pog_done
        pog_dep_l2 = OrderedDict()
        for parent_item, list_child_items in pog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('protocol-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group protocol ' + item.strip().split(' ')[1]
                if 'protocol-object object' in item:
                    name = 'object protocol ' + item.strip().split(' ')[2]
                if name in pog_dep_none.keys():
                    pog_dep_l2[parent_item] = list_child_items
                    if pog_dep.get(parent_item) is not None:
                        pog_dep.pop(parent_item)
        if pog_dep.keys() == []:
            pog_done = True
        return [pog_dep, pog_dep_l2]


def pog_sep_l3(pog_dep, l2_items):
    if pog_dep.keys() != []:
        global pog_done
        pog_dep_l3 = OrderedDict()
        for parent_item, list_child_items in pog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('protocol-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group protocol ' + item.strip().split(' ')[1]
                if 'protocol-object object' in item:
                    name = 'object protocol ' + item.strip().split(' ')[2]
                if name in l2_items.keys():
                    pog_dep_l3[parent_item] = list_child_items
                    if pog_dep.get(parent_item) is not None:
                        pog_dep.pop(parent_item)
        if pog_dep.keys() == []:
            pog_done = True
        return [pog_dep, pog_dep_l3]


def pog_sep_l4(pog_dep, l3_items):
    if pog_dep.keys() != []:
        global pog_done
        pog_dep_l4 = OrderedDict()
        for parent_item, list_child_items in pog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('protocol-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group protocol ' + item.strip().split(' ')[1]
                if 'protocol-object object' in item:
                    name = 'object protocol ' + item.strip().split(' ')[2]
                if name in l3_items.keys():
                    pog_dep_l4[parent_item] = list_child_items
                    if pog_dep.get(parent_item) is not None:
                        pog_dep.pop(parent_item)
        if pog_dep.keys() == []:
            pog_done = True
        return [pog_dep, pog_dep_l4]


def pog_sep_l5(pog_dep, l4_items):
    if pog_dep.keys() != []:
        global pog_done
        pog_dep_l5 = OrderedDict()
        for parent_item, list_child_items in pog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('protocol-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group protocol ' + item.strip().split(' ')[1]
                if 'protocol-object object' in item:
                    name = 'object protocol ' + item.strip().split(' ')[2]
                if name in l4_items.keys():
                    pog_dep_l5[parent_item] = list_child_items
                    if pog_dep.get(parent_item) is not None:
                        pog_dep.pop(parent_item)
        if pog_dep.keys() == []:
            pog_done = True
        return [pog_dep, pog_dep_l5]


def pog_sep_l6(pog_dep, l5_items):
    if pog_dep.keys() != []:
        global pog_done
        pog_dep_l6 = OrderedDict()
        for parent_item, list_child_items in pog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('protocol-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group protocol ' + item.strip().split(' ')[1]
                if 'protocol-object object' in item:
                    name = 'object protocol ' + item.strip().split(' ')[2]
                if name in l5_items.keys():
                    pog_dep_l6[parent_item] = list_child_items
                    if pog_dep.get(parent_item) is not None:
                        pog_dep.pop(parent_item)
        if pog_dep.keys() == []:
            pog_done = True
        return [pog_dep, pog_dep_l6]


def pog_sep_l7(pog_dep, l6_items):
    if pog_dep.keys() != []:
        global pog_done
        pog_dep_l7 = OrderedDict()
        for parent_item, list_child_items in pog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('protocol-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group protocol ' + item.strip().split(' ')[1]
                if 'protocol-object object' in item:
                    name = 'object protocol ' + item.strip().split(' ')[2]
                if name in l6_items.keys():
                    pog_dep_l7[parent_item] = list_child_items
                    if pog_dep.get(parent_item) is not None:
                        pog_dep.pop(parent_item)
        if pog_dep.keys() == []:
            pog_done = True
        return [pog_dep, pog_dep_l7]


def pog_sep_l8(pog_dep, l7_items):
    if pog_dep.keys() != []:
        global pog_done
        pog_dep_l8 = OrderedDict()
        for parent_item, list_child_items in pog_dep.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if ('group-object' in item) or ('protocol-object object' in item):
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                if 'group-object' in item:
                    name = 'object-group protocol ' + item.strip().split(' ')[1]
                if 'protocol-object object' in item:
                    name = 'object protocol ' + item.strip().split(' ')[2]
                if name in l7_items.keys():
                    pog_dep_l8[parent_item] = list_child_items
                    if pog_dep.get(parent_item) is not None:
                        pog_dep.pop(parent_item)
        if pog_dep.keys() == []:
            pog_done = True
        return [pog_dep, pog_dep_l8]


# PRINTING FUNCTIONS


def print_nog_dcts():
    try:
        with open('output.txt', 'a') as f:
            f.write('######################################################\n')
            f.write('MIGRATION CONFIGS:\n')
            f.write('######################################################\n')
            for key, value in nog_dct_sep[0].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in nog_dct_l2[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in nog_dct_l3[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in nog_dct_l4[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in nog_dct_l5[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in nog_dct_l6[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in nog_dct_l7[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in nog_dct_l8[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
    except TypeError:
        pass
    except NameError:
        pass


def print_sog_dcts():
    try:
        with open('output.txt', 'a') as f:
            for key, value in sog_dct_sep[0].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in sog_dct_l2[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in sog_dct_l3[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in sog_dct_l4[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in sog_dct_l5[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in sog_dct_l6[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in sog_dct_l7[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in sog_dct_l8[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
    except TypeError:
        pass
    except NameError:
        pass


def print_pog_dcts():
    try:
        with open('output.txt', 'a') as f:
            for key, value in pog_dct_sep[0].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in pog_dct_l2[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in pog_dct_l3[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in pog_dct_l4[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in pog_dct_l5[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in pog_dct_l6[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in pog_dct_l7[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
            for key, value in pog_dct_l8[1].iteritems():
                f.write(key + '\n')
                for item in value:
                    f.write(item + '\n')
    except TypeError:
        pass
    except NameError:
        pass


def print_acls():
    try:
        with open('output.txt', 'w') as f:
            f.write('######################################################\n')
            f.write('LIST OF ACLs IN CONFIGURATION:\n')
            f.write('######################################################\n')
            for item in acls_unique:
                f.write(item + '\n')
            f.write('\n')
    except:
        pass


def print_acls_bound():
    try:
        with open('output.txt', 'a') as f:
            f.write('######################################################\n')
            f.write('LIST OF BOUND ACLs:\n')
            f.write('######################################################\n')
            for item in acls_bound:
                f.write(item + '\n')
            f.write('\n')
    except:
        pass


def print_acls_unbound():
    try:
        with open('output.txt', 'a') as f:
            f.write('######################################################\n')
            f.write('LIST OF ORPHANED ACLs:\n')
            f.write('######################################################\n')
            for item in acls_unbound:
                f.write(item + '\n')
            f.write('\n')
    except:
        pass


def print_objs_unbound():
    try:
        with open('output.txt', 'a') as f:
            f.write('######################################################\n')
            f.write('LIST OF ORPHANED OBJECT-GROUPS:\n')
            f.write('######################################################\n')
            for item in objs_unbound:
                f.write(item + '\n')
            f.write('\n')
    except:
        pass


def print_config(acls):
    with open('output.txt', 'a') as f:
        for k, v in acls.items():
            for item in v:
                if k in acls_bound:
                    f.write(item + '\n')
        f.write('\n')


# MAIN


# NETWORK OBJECT GROUPS


nog_dct_all = nog_cd(inputfile)

nog_dct_sep = nog_sep(nog_dct_all)
print '{}:\n{}\n'.format('NO NOG DEPENDENCIES', nog_dct_sep[0])
print '{}:\n{}\n'.format('NOG DEPENDENCIES', nog_dct_sep[1])

if nog_done is not True:
    try:
        nog_dct_l2 = nog_sep_l2(nog_dct_sep[0], nog_dct_sep[1])
        print '{}:\n{}\n'.format('STEP2: NOG DEPENDENCIES', nog_dct_l2[0])
        print '{}:\n{}\n'.format('STEP2: L2 ITEMS', nog_dct_l2[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is not True:
    try:
        nog_dct_l3 = nog_sep_l3(nog_dct_l2[0], nog_dct_l2[1])
        print '{}:\n{}\n'.format('STEP3: NOG DEPENDENCIES', nog_dct_l3[0])
        print '{}:\n{}\n'.format('STEP3: L3 ITEMS', nog_dct_l3[1])
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is not True:
    try:
        nog_dct_l4 = nog_sep_l4(nog_dct_l3[0], nog_dct_l3[1])
        print '{}:\n{}\n'.format('STEP4: NOG DEPENDENCIES', nog_dct_l4[0])
        print '{}:\n{}\n'.format('STEP4: L4 ITEMS', nog_dct_l4[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is not True:
    try:
        nog_dct_l5 = nog_sep_l5(nog_dct_l4[0], nog_dct_l4[1])
        print '{}:\n{}\n'.format('STEP5: NOG DEPENDENCIES', nog_dct_l5[0])
        print '{}:\n{}\n'.format('STEP5: L5 ITEMS', nog_dct_l5[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is not True:
    try:
        nog_dct_l6 = nog_sep_l6(nog_dct_l5[0], nog_dct_l5[1])
        print '{}:\n{}\n'.format('STEP6: NOG DEPENDENCIES', nog_dct_l6[0])
        print '{}:\n{}\n'.format('STEP6: L6 ITEMS', nog_dct_l6[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is not True:
    try:
        nog_dct_l7 = nog_sep_l7(nog_dct_l6[0], nog_dct_l6[1])
        print '{}:\n{}\n'.format('STEP7: NOG DEPENDENCIES', nog_dct_l7[0])
        print '{}:\n{}\n'.format('STEP7: L7 ITEMS', nog_dct_l7[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is not True:
    try:
        nog_dct_l8 = nog_sep_l8(nog_dct_l7[0], nog_dct_l7[1])
        print '{}:\n{}\n'.format('STEP8: NOG DEPENDENCIES', nog_dct_l8[0])
        print '{}:\n{}\n'.format('STEP8: L8 ITEMS', nog_dct_l8[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is True:
    print 'ALL NOG DEPENDENCIES RESOLVED\n'


# SERVICE OBJECT GROUPS


sog_dct_all = sog_cd(inputfile)

sog_dct_sep = sog_sep(sog_dct_all)
print '{}:\n{}\n'.format('NO SOG DEPENDENCIES', sog_dct_sep[0])
print '{}:\n{}\n'.format('SOG DEPENDENCIES', sog_dct_sep[1])

if sog_done is not True:
    try:
        sog_dct_l2 = sog_sep_l2(sog_dct_sep[0], sog_dct_sep[1])
        print '{}:\n{}\n'.format('STEP2: SOG DEPENDENCIES', sog_dct_l2[0])
        print '{}:\n{}\n'.format('STEP2: L2 ITEMS', sog_dct_l2[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l3 = sog_sep_l3(sog_dct_l2[0], sog_dct_l2[1])
        print '{}:\n{}\n'.format('STEP3: SOG DEPENDENCIES', sog_dct_l3[0])
        print '{}:\n{}\n'.format('STEP3: L3 ITEMS', sog_dct_l3[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l4 = sog_sep_l4(sog_dct_l3[0], sog_dct_l3[1])
        print '{}:\n{}\n'.format('STEP4: SOG DEPENDENCIES', sog_dct_l4[0])
        print '{}:\n{}\n'.format('STEP4: L4 ITEMS', sog_dct_l4[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l5 = sog_sep_l5(sog_dct_l4[0], sog_dct_l4[1])
    except TypeError:
        print '{}:\n{}\n'.format('STEP5: SOG DEPENDENCIES', sog_dct_l5[0])
        print '{}:\n{}\n'.format('STEP5: L5 ITEMS', sog_dct_l5[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l6 = sog_sep_l6(sog_dct_l5[0], sog_dct_l5[1])
        print '{}:\n{}\n'.format('STEP6: SOG DEPENDENCIES', sog_dct_l6[0])
        print '{}:\n{}\n'.format('STEP6: L6 ITEMS', sog_dct_l6[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l7 = sog_sep_l7(sog_dct_l6[0], sog_dct_l6[1])
        print '{}:\n{}\n'.format('STEP7: SOG DEPENDENCIES', sog_dct_l7[0])
        print '{}:\n{}\n'.format('STEP7: L7 ITEMS', sog_dct_l7[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l8 = sog_sep_l8(sog_dct_l7[0], sog_dct_l7[1])
        print '{}:\n{}\n'.format('STEP8: SOG DEPENDENCIES', sog_dct_l8[0])
        print '{}:\n{}\n'.format('STEP8: L8 ITEMS', sog_dct_l8[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is True:
    print 'ALL SOG DEPENDENCIES RESOLVED\n'


# PROTOCOL OBJECT GROUPS


pog_dct_all = pog_cd(inputfile)

pog_dct_sep = pog_sep(pog_dct_all)
print '{}:\n{}\n'.format('NO POG DEPENDENCIES', pog_dct_sep[0])
print '{}:\n{}\n'.format('POG DEPENDENCIES', pog_dct_sep[1])

if pog_done is not True:
    try:
        pog_dct_l2 = pog_sep_l2(pog_dct_sep[0], pog_dct_sep[1])
        print '{}:\n{}\n'.format('STEP2: POG DEPENDENCIES', pog_dct_l2[0])
        print '{}:\n{}\n'.format('STEP2: L2 ITEMS', pog_dct_l2[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is not True:
    try:
        pog_dct_l3 = pog_sep_l3(pog_dct_l2[0], pog_dct_l2[1])
        print '{}:\n{}\n'.format('STEP3: POG DEPENDENCIES', pog_dct_l3[0])
        print '{}:\n{}\n'.format('STEP3: L3 ITEMS', pog_dct_l3[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is not True:
    try:
        pog_dct_l4 = pog_sep_l4(pog_dct_l3[0], pog_dct_l3[1])
        print '{}:\n{}\n'.format('STEP4: POG DEPENDENCIES', pog_dct_l4[0])
        print '{}:\n{}\n'.format('STEP4: L4 ITEMS', pog_dct_l4[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is not True:
    try:
        pog_dct_l5 = pog_sep_l5(pog_dct_l4[0], pog_dct_l4[1])
        print '{}:\n{}\n'.format('STEP5: POG DEPENDENCIES', pog_dct_l5[0])
        print '{}:\n{}\n'.format('STEP5: L5 ITEMS', pog_dct_l5[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is not True:
    try:
        pog_dct_l6 = pog_sep_l6(pog_dct_l5[0], pog_dct_l5[1])
        print '{}:\n{}\n'.format('STEP6: POG DEPENDENCIES', pog_dct_l6[0])
        print '{}:\n{}\n'.format('STEP6: L6 ITEMS', pog_dct_l6[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is not True:
    try:
        pog_dct_l7 = pog_sep_l7(pog_dct_l6[0], pog_dct_l6[1])
        print '{}:\n{}\n'.format('STEP7: POG DEPENDENCIES', pog_dct_l7[0])
        print '{}:\n{}\n'.format('STEP7: L7 ITEMS', pog_dct_l7[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is not True:
    try:
        pog_dct_l8 = pog_sep_l8(pog_dct_l7[0], pog_dct_l7[1])
        print '{}:\n{}\n'.format('STEP8: POG DEPENDENCIES', pog_dct_l8[0])
        print '{}:\n{}\n'.format('STEP8: L8 ITEMS', pog_dct_l8[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is True:
    print 'ALL POG DEPENDENCIES RESOLVED'


# GENERATE OUTPUT

mycfg = ifile(inputfile)
acls = cd_acls(mycfg)
acls_unique = cl_unique_acls(mycfg)
acls_bound = cl_bound_acls(mycfg)
acls_unbound = cl_unbound_acls(mycfg)
# objs_unbound = cl_unbound_objgroups(mycfg)

# print '%s:\n%s\n' % ('UNIQUE ACLS', cl_unique_acls(mycfg))
# print '%s:\n%s\n' % ('BOUND ACLS', cl_bound_acls(mycfg))
# print '%s:\n%s\n' % ('UNBOUND ACLS', cl_unbound_acls(mycfg))
# print '%s:\n%s\n' % ('UNBOUND OBJECT GROUPS', cl_unbound_objgroups(mycfg))


print_acls()
# print_acls_bound()
print_acls_unbound()
# print_objs_unbound()

print_nog_dcts()
print_sog_dcts()
print_pog_dcts()
print_config(acls)

