import json
import requests
import pprint

url = 'http://127.0.0.1:5000/api_post'

# r = requests.post(url, data=json.dumps(payload), headers=headers)
r = requests.post(url, data="hogehoge".encode('utf-8'))
# pprint.pprint(r.text)
print(r.text)
input()
