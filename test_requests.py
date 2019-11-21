import requests

point = 50962
connector = 2
baseurl = 'https://map.chargeplacescotland.org/status'
payload = {'bayNo' : point, 'connectorId' : connector}

data = requests.get(baseurl, params=payload).json()

print(data['status'])

