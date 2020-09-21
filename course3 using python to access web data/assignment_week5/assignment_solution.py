import xml.etree.ElementTree as ET
import urllib.request

url = input("Enter location:")
print("Retrieving", url)
data = urllib.request.urlopen(url).read().decode()
xml_data = ET.fromstring(data)

count = 0
numbers_sum = 0

comments = xml_data.findall("comments/comment")
for comment in comments:
    count = count + 1
    numbers_sum = numbers_sum + int(comment.find('count').text)
print("Count:", count)
print("Sum:", numbers_sum)
