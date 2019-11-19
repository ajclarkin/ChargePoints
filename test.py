# check out json interface

import json
from urllib.request import urlopen

point = 50962
connector = 2
url = 'https://map.chargeplacescotland.org/status?bayNo=' + str(point) + '&connectorId=' + str(connector)

with urlopen(url) as response:
    for line in response:
        ret = json.loads(line)
        status = ret["status"]

    print(status)
    if status == "In use":
        print(0)
    elif status == "Available":
        print(1)
    else:
        print('who knows')
