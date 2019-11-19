import requests

point = 50962
connector = 2
baseurl = 'https://map.chargeplacescotland.org/status'
payload = {'bayNo' : point, 'connectorId' : connector}

# ret = requests.get(baseurl, params=payload)
data = requests.get(baseurl, params=payload).json()
# print(ret.text)

# data = ret.json()
print(data['status'])
# with urlopen(url) as response:
#     for line in response:
#         ret = json.loads(line)
#         status = ret["status"]

    # print(status)
    # if status == "In use":
    #     print(0)
    # elif status == "Available":
    #     print(1)
    # else:
    #     print('who knows')
