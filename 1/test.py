# -*- coding: utf-8 -*-
from full_areas import locations
import json


areas = {}

for loc in locations:
    # if loc["name"] in ["北京", "河北", "天津", "山东"]:
    if loc["name"]:
        print '  u"'+loc["name"]+'" : [ '
        d = []
        
        for s in loc["sub"]:
            print '    u"' + s["name"] + '", '
            d.append(s["name"])

        areas[loc["name"]] = d

        print '  ],'

# print json.dumps(areas, sort_keys=True, indent=4*' ')