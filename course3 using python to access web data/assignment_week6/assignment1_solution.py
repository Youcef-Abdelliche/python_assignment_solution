import urllib.request, urllib.parse
import json

url = input("Enter location:")
print("Retrieving", url)
handler = urllib.request.urlopen(url)
data = handler.read().decode()
print("Retrieved", len(data), "characters")
js = json.loads(data)

count = 0
numbers_sum = 0
for comment in js['comments']:
    count = count + 1
    numbers_sum = numbers_sum + comment["count"]

print("Count:", count)
print("Sum:", numbers_sum)
