# This uses a webhooks applet on IFTTT:
#   IF: webhooks endpoint activated
#   THEN: notify including webhooks value 1

import requests

def IFTTTNotification(message = 'No message body specified'):
    ifttt_key = 'dWRTQgkMw1GE482jbxDeZQ'
    ifttt_endpoint = 'chargepoint_available'
    ifttt_url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'

    url = ifttt_url.format(ifttt_endpoint, ifttt_key)
    post_data = {'value1': message}



    response = requests.post(url, data=post_data)
    print(response.text)



IFTTTNotification('Here is your test message Andrew')


