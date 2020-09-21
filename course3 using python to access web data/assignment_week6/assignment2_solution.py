import urllib.request, urllib.parse
import json

url = "http://py4e-data.dr-chuck.net/json?"

while True:
    address = input("Enter location:")
    if len(address) < 1: break
    params = {
        "address": address,
        "key": 42
    }
    url = url + urllib.parse.urlencode(params)
    print("Retrieving", url)
    handler = urllib.request.urlopen(url)
    data = handler.read().decode()
    print("Retrieved", len(data), "characters")

    try:
        js = json.loads(data)
    except:
        js = None
    if js is None or 'status' not in js or js['status'] != 'OK':
        print("============= Failure =============")
        break
    place_id = js["results"][0]['place_id']
    print("Place id", place_id)
