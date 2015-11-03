from collections import OrderedDict
from ciscoconfparse import CiscoConfParse
from pprint import pprint
import re

done = False

def cd_netobjgrps(filename):
    netobjgrps = {}
    mycfg = CiscoConfParse(filename)
    lines = mycfg.find_objects(r'^object-group network')
    if lines != []:
        for parent_item in lines:
            list_child_items = []
            for child_item in parent_item.all_children:
                list_child_items.append(child_item.text)
            netobjgrps[parent_item.text] = list_child_items
        return netobjgrps

def separate_netobjgrps(netobjgrps):
    no_dependencies_netobjgrps = OrderedDict()
    dependencies_netobjgrps = OrderedDict()
    for parent_item, list_child_items in netobjgrps.items():
        no_dependency = True
        count = 0
        for item in list_child_items:
            if 'group-object' in item:
                count += 1
                no_dependency = False
                if count == 1:
                    dependencies_netobjgrps[parent_item] = list_child_items
        if no_dependency:
            no_dependencies_netobjgrps[parent_item] = list_child_items
    return [no_dependencies_netobjgrps, dependencies_netobjgrps]

def separate_l2(no_dependencies, dependencies):
    if dependencies.keys() != []:
        global done
        l2_dependencies_netobjgrps = OrderedDict()
        for parent_item, list_child_items in dependencies.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in no_dependencies.keys():
                    l2_dependencies_netobjgrps[parent_item] = list_child_items
                    dependencies.pop(parent_item)
        if dependencies.keys() == []:
            done = True
        return [dependencies, l2_dependencies_netobjgrps]

def separate_l3(dependencies, l2_items):
    if dependencies.keys() != []:
        global done
        l3_dependencies_netobjgrps = OrderedDict()
        for parent_item, list_child_items in dependencies.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l2_items.keys():
                    l3_dependencies_netobjgrps[parent_item] = list_child_items
                    dependencies.pop(parent_item)
        if dependencies.keys() == []:
            done = True
        return [dependencies, l3_dependencies_netobjgrps]

def separate_l4(dependencies, l3_items):
    if dependencies.keys() != []:
        global done
        l4_dependencies_netobjgrps = OrderedDict()
        for parent_item, list_child_items in dependencies.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l3_items.keys():
                    l4_dependencies_netobjgrps[parent_item] = list_child_item
                    dependencies.pop(parent_item)
        if dependencies.keys() == []:
            done = True
        return [dependencies, l4_dependencies_netobjgrps]

def separate_l5(dependencies, l4_items):
    if dependencies.keys() != []:
        global done
        l5_dependencies_netobjgrps = OrderedDict()
        for parent_item, list_child_items in dependencies.iteritems():
            list_grpobjects = []
            for item in list_child_items:
                if 'group-object' in item:              
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l4_items.keys():            
                    l5_dependencies_netobjgrps[parent_item] = list_child_item
                    dependencies.pop(parent_item)          
        if dependencies.keys() == []:
            done = True
        return [dependencies, l5_dependencies_netobjgrps]

# MAIN

network_object_groups = cd_netobjgrps('sourcefile.txt')
 
separation = separate_netobjgrps(network_object_groups)
print '{}:\n{}\n'.format('NO DEPENDENCIES', separation[0])
print '{}:\n{}\n'.format('DEPENDENCIES', separation[1])

if done != True:
    l2 = separate_l2(separation[0], separation[1])
    print '{}:\n{}\n'.format('STEP2: DEPENDENCIES', l2[0])
    print '{}:\n{}\n'.format('STEP2: L2 ITEMS', l2[1])

if done != True:
    l3 = separate_l3(l2[0], l2[1])
    print '{}:\n{}\n'.format('STEP3: DEPENDENCIES', l3[0])
    print '{}:\n{}\n'.format('STEP3: L3 ITEMS', l3[1])

if done != True:
    l4 = separate_l4(l3[0], l3[1])
    print '{}:\n{}\n'.format('STEP4: DEPENDENCIES', l4[0])
    print '{}:\n{}\n'.format('STEP4: L3 ITEMS', l4[1])

if done != True:
    l5 = separate_l5(l4[0], l4[1])
    print '{}:\n{}\n'.format('STEP5: DEPENDENCIES', l5[0])
    print '{}:\n{}\n'.format('STEP5: L3 ITEMS', l5[1])

if done == True:
    print 'ALL DEPENDENCIES RESOLVED'
