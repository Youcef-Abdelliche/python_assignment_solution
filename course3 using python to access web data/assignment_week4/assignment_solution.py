from bs4 import BeautifulSoup
import urllib.request

url = "http://py4e-data.dr-chuck.net/comments_974961.html"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup('span')

count = 0
numbers_sum = 0
for tag in tags:
    count = count+1
    numbers_sum = numbers_sum + int(tag.contents[0])
print('Count', count)
print('Sum', numbers_sum)