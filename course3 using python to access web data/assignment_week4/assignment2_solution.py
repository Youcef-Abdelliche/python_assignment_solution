from bs4 import BeautifulSoup
import urllib.request

url = "http://py4e-data.dr-chuck.net/known_by_Kiarra.html"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup('a')
print("Retrieving:", tags[17].get('href', None))
count = 0
pos = 18

while count < 6:
    url = tags[17].get('href', None)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    print("Retrieving:", tags[17].get('href', None))
    count = count + 1
