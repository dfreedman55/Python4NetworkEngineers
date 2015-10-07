#!/usr/bin/env python

import json
import yaml
import pprint

with open('output-filename.json', 'r') as f:
 a_json = json.load(f)

with open('output-filename.yaml', 'r') as f:
 a_yaml = yaml.load(f)

pprint.pprint(a_json)
pprint.pprint(a_yaml)

