#!/usr/bin/env python

a = range(10)
a.append('whatever')
a.append('hello')
a.append({})
a[-1]['name'] = 'router1'
a[-1]['ip_addr'] = '10.10.10.1'
a[-1]['attribs'] = range(6)

import yaml
import json

with open('output-filename.json', 'w') as f:
 json.dump(a, f)

with open('output-filename.yaml', 'w') as f:
 yaml.dump(a, f, default_flow_style=False)

