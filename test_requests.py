import requests
import certifi


point = 50961
connector = 1
baseurl = 'https://map.chargeplacescotland.org/status'
payload = {'bayNo' : point, 'connectorId' : connector}

#data = requests.get(baseurl, params=payload).json()

data = requests.get(baseurl, params=payload)
print(data.url)
#print(data['status'])
print(data.text)

