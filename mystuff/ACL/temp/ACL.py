from collections import OrderedDict
from ciscoconfparse import CiscoConfParse
# from pprint import pprint
# import re

nog_done = False
sog_done = False
pog_done = False

'''NAMING CONVENTION
cd = create dictionary
nog = network object group
sog = service object group
pog = protocol object group
sep = separate
dep = dependencies
dct = dictionaries

FUNCTIONS
nog_cd			sog_cd			pog_cd
nog_sep			sog_sep			pog_sep
nog_sep_l2		sog_sep_l2		pog_sep_l2
nog_sep_l3		sog_sep_l3		pog_sep_l3
nog_sep_l4		sog_sep_l4		pog_sep_l4
nog_sep_l5		sog_sep_l5		pog_sep_l5
nog_sep_l6		sog_sep_l6		pog_sep_l6
nog_sep_l7		sog_sep_l7		pog_sep_l7
nog_sep_l8		sog_sep_l8		pog_sep_l8

DICTIONARIES
nog_all			sog_all			pog_all
nog_dep_none    	sog_dep_none	        pog_dep_none
nog_dep			sog_dep			pog_dep
nog_dep_l2		sog_dep_l2		pog_dep_l2
nog_dep_l3		sog_dep_l3		pog_dep_l3
nog_dep_l4		sog_dep_l4		pog_dep_l4
nog_dep_l5		sog_dep_l5		pog_dep_l5
nog_dep_l6		sog_dep_l6		pog_dep_l6
nog_dep_l7		sog_dep_l7		pog_dep_l7
nog_dep_l8		sog_dep_l8		pog_dep_l8

RESULTS
nog_dct_all		sog_dct_all		pog_dct_all
nog_dct_sep		sog_dct_sep		pog_dct_sep
nog_dct_l2		sog_dct_l2		pog_dct_l2
nog_dct_l3		sog_dct_l3		pog_dct_l3
nog_dct_l4		sog_dct_l4		pog_dct_l4
nog_dct_l5		sog_dct_l5		pog_dct_l5
nog_dct_l6		sog_dct_l6		pog_dct_l6
nog_dct_l7		sog_dct_l7		pog_dct_l7
nog_dct_l8		sog_dct_l8		pog_dct_l8'''

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
        return nog_all


def nog_sep(nog_all):
    nog_dep_none = OrderedDict()
    nog_dep = OrderedDict()
    for parent_item, list_child_items in nog_all.items():
        no_dependency = True
        count = 0
        for item in list_child_items:
            if 'group-object' in item:
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in nog_dep_none.keys():
                    nog_dep_l2[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l2_items.keys():
                    nog_dep_l3[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l3_items.keys():
                    nog_dep_l4[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l4_items.keys():
                    nog_dep_l5[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l5_items.keys():
                    nog_dep_l6[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l6_items.keys():
                    nog_dep_l7[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group network ' + item.strip().split(' ')[1]
                if name in l7_items.keys():
                    nog_dep_l8[parent_item] = list_child_items
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
        return sog_all


def sog_sep(sog_all):
    sog_dep_none = OrderedDict()
    sog_dep = OrderedDict()
    for parent_item, list_child_items in sog_all.items():
        no_dependency = True
        count = 0
        for item in list_child_items:
            if 'group-object' in item:
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group service ' + item.strip().split(' ')[1]
                if name in sog_dep_none.keys():
                    sog_dep_l2[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group service ' + item.strip().split(' ')[1]
                if name in l2_items.keys():
                    sog_dep_l3[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group service ' + item.strip().split(' ')[1]
                if name in l3_items.keys():
                    sog_dep_l4[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group service ' + item.strip().split(' ')[1]
                if name in l4_items.keys():
                    sog_dep_l5[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group service ' + item.strip().split(' ')[1]
                if name in l5_items.keys():
                    sog_dep_l6[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group service ' + item.strip().split(' ')[1]
                if name in l6_items.keys():
                    sog_dep_l7[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group service ' + item.strip().split(' ')[1]
                if name in l7_items.keys():
                    sog_dep_l8[parent_item] = list_child_items
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
        return pog_all


def pog_sep(pog_all):
    pog_dep_none = OrderedDict()
    pog_dep = OrderedDict()
    for parent_item, list_child_items in pog_all.items():
        no_dependency = True
        count = 0
        for item in list_child_items:
            if 'group-object' in item:
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group protocol ' + item.strip().split(' ')[1]
                if name in pog_dep_none.keys():
                    pog_dep_l2[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group protocol ' + item.strip().split(' ')[1]
                if name in l2_items.keys():
                    pog_dep_l3[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group protocol ' + item.strip().split(' ')[1]
                if name in l3_items.keys():
                    pog_dep_l4[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group protocol ' + item.strip().split(' ')[1]
                if name in l4_items.keys():
                    pog_dep_l5[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group protocol ' + item.strip().split(' ')[1]
                if name in l5_items.keys():
                    pog_dep_l6[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group protocol ' + item.strip().split(' ')[1]
                if name in l6_items.keys():
                    pog_dep_l7[parent_item] = list_child_items
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
                if 'group-object' in item:
                    list_grpobjects.append(item)
            for item in list_grpobjects:
                name = 'object-group protocol ' + item.strip().split(' ')[1]
                if name in l7_items.keys():
                    pog_dep_l8[parent_item] = list_child_items
                    pog_dep.pop(parent_item)
        if pog_dep.keys() == []:
            pog_done = True
        return [pog_dep, pog_dep_l8]

# NETWORK OBJECT GROUP MAIN

nog_dct_all = nog_cd('sourcefile.txt')

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
    except TypeError:
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
        print '{}:\n{}\n'.format('STEP5: NOG DEPENDENCIES', nog_dct_l6[0])
        print '{}:\n{}\n'.format('STEP5: L6 ITEMS', nog_dct_l6[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is not True:
    try:
        nog_dct_l7 = nog_sep_l7(nog_dct_l6[0], nog_dct_l6[1])
        print '{}:\n{}\n'.format('STEP5: NOG DEPENDENCIES', nog_dct_l7[0])
        print '{}:\n{}\n'.format('STEP5: L7 ITEMS', nog_dct_l7[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is not True:
    try:
        nog_dct_l8 = nog_sep_l8(nog_dct_l7[0], nog_dct_l7[1])
        print '{}:\n{}\n'.format('STEP5: NOG DEPENDENCIES', nog_dct_l8[0])
        print '{}:\n{}\n'.format('STEP5: L8 ITEMS', nog_dct_l8[1])
    except TypeError:
        nog_done = True
    except NameError:
        nog_done = True

if nog_done is True:
    print 'ALL NOG DEPENDENCIES RESOLVED\n'

# SERVICE OBJECT GROUP MAIN

sog_dct_all = sog_cd('sourcefile.txt')

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
        print '{}:\n{}\n'.format('STEP5: SOG DEPENDENCIES', sog_dct_l5[0])
        print '{}:\n{}\n'.format('STEP5: L5 ITEMS', sog_dct_l5[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l6 = sog_sep_l6(sog_dct_l5[0], sog_dct_l5[1])
        print '{}:\n{}\n'.format('STEP5: SOG DEPENDENCIES', sog_dct_l6[0])
        print '{}:\n{}\n'.format('STEP5: L6 ITEMS', sog_dct_l6[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l7 = sog_sep_l7(sog_dct_l6[0], sog_dct_l6[1])
        print '{}:\n{}\n'.format('STEP5: SOG DEPENDENCIES', sog_dct_l7[0])
        print '{}:\n{}\n'.format('STEP5: L7 ITEMS', sog_dct_l7[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is not True:
    try:
        sog_dct_l8 = sog_sep_l8(sog_dct_l7[0], sog_dct_l7[1])
        print '{}:\n{}\n'.format('STEP5: SOG DEPENDENCIES', sog_dct_l8[0])
        print '{}:\n{}\n'.format('STEP5: L8 ITEMS', sog_dct_l8[1])
    except TypeError:
        sog_done = True
    except NameError:
        sog_done = True

if sog_done is True:
    print 'ALL SOG DEPENDENCIES RESOLVED\n'

# PROTOCOL OBJECT GROUP MAIN

pog_dct_all = pog_cd('sourcefile.txt')

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
        print '{}:\n{}\n'.format('STEP5: POG DEPENDENCIES', pog_dct_l6[0])
        print '{}:\n{}\n'.format('STEP5: L6 ITEMS', pog_dct_l6[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is not True:
    try:
        pog_dct_l7 = pog_sep_l7(pog_dct_l6[0], pog_dct_l6[1])
        print '{}:\n{}\n'.format('STEP5: POG DEPENDENCIES', pog_dct_l7[0])
        print '{}:\n{}\n'.format('STEP5: L7 ITEMS', pog_dct_l7[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is not True:
    try:
        pog_dct_l8 = pog_sep_l8(pog_dct_l7[0], pog_dct_l7[1])
        print '{}:\n{}\n'.format('STEP5: POG DEPENDENCIES', pog_dct_l8[0])
        print '{}:\n{}\n'.format('STEP5: L8 ITEMS', pog_dct_l8[1])
    except TypeError:
        pog_done = True
    except NameError:
        pog_done = True

if pog_done is True:
    print 'ALL POG DEPENDENCIES RESOLVED'

# PRINT ALL DICTIONARIES

def print_nog_dcts():
    try:
        with open('output.txt', 'w') as f:
            for key, value in nog_dct_sep[0].iteritems():
                f.write(key\n)
                for item in value:
                    f.write(item\n)
            for key, value in nog_dct_l2[1].iteritems():
                f.write(key\n)
                for item in value:
                    f.write(item\n)
            for key, value in nog_dct_l3[1].iteritems(): 
                f.write(key\n)
                for item in value:
                    f.write(item\n)
            for key, value in nog_dct_l4[1].iteritems(): 
                f.write(key\n)
                for item in value:
                    f.write(item\n)
            for key, value in nog_dct_l5[1].iteritems(): 
                f.write(key\n)
                for item in value:
                    f.write(item\n)
            for key, value in nog_dct_l6[1].iteritems(): 
                f.write(key\n)
                for item in value:
                    f.write(item\n)
            for key, value in nog_dct_l7[1].iteritems(): 
                f.write(key\n)
                for item in value:
                    f.write(item\n)
            for key, value in nog_dct_l8[1].iteritems(): 
                f.write(key\n)
                for item in value:
                    f.write(item\n)
    except TypeError:
        pass
    except NameError:
        pass

print_nog_dcts()
