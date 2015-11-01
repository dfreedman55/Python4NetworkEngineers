from collections import OrderedDict
from ciscoconfparse import CiscoConfParse
from pprint import pprint
import re

# FUNCTIONS

def dict_network_object_groups(filename):
    dict_network_object_groups = {}
    ccp_config = CiscoConfParse(filename)
    lines = ccp_config.find_objects(r'^object-group network')
    for parent_item in lines:
        items_in_object_group = []
        for child_item in parent_item.all_children:
            items_in_object_group.append(child_item.text)
        dict_network_object_groups[parent_item.text] = items_in_object_group
    return dict_network_object_groups

#look at the previously created dictionary of object-groups
#we want to identify keys which have no dependencies inside of them
#for each key in the dictionary, grab the value
#  for each item in the value (list of configuration lines)
#    if any of the configuration lines have 'group-object' within them
#      then mark that this key has a dependency
#      and write the key and its value to a second-level dictionary
# if the key has been marked as having no dependency
#   then write the key and its value to a first-level dictionary

def first_level_network_objects(network_object_groups):
    dependency_network_objects = OrderedDict()
    no_dependency_network_objects = OrderedDict()
    for k, v in network_object_groups.items():
        no_dependencies = True
        for item in v:
            if 'group-object' in item:
                no_dependencies = False
                dependency_network_objects[k] = v
        if no_dependencies:
            no_dependency_network_objects[k] = v
    return dependency_network_objects, no_dependency_network_objects

# MAIN

network_object_groups = dict_network_object_groups('sourcefile.txt')
keep = first_level_network_objects(network_object_groups)
print '%s:\n%s\n' % ('DEPENDENCIES', keep[0])
print '%s:\n%s\n' % ('NO DEPENDENCIES', keep[1])


