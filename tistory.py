from bs4 import BeautifulSoup
import requests
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

## fetch url
url = 'http://iam312.pe.kr/526'
r = requests.get(url, headers=headers)
raw_html = r.text

## to file
#with open("test.html", "w") as f:
#        f.write(raw_html.encode("utf-8"))

## from file
#with open("test.html", "r") as f:
#    raw_html = f.read()

soup = BeautifulSoup(raw_html, 'html.parser')

###############################
# title
###############################
title = soup.find("h3", class_="tit_post").text
print "*" * 30
print title
print "-" * 30


###############################
# reg date
###############################
reg_date = soup.find("span", class_="info_post").text
print "*" * 30
print reg_date.split("\n")[1].strip()
print "-" * 30



###############################
# contents
###############################
# remove ccl
ccl = soup.find('div', style="width:100%;margin-top:30px;clear:both;height:30px")
ccl.decompose()

# remove category
cate = soup.find('div', class_="another_category another_category_color_gray")
cate.decompose()

# remove Exifinfo
exifinfos = soup.find_all('span', class_="ExifInfo")
for exifinfo in exifinfos :
    exifinfo.decompose()

_content = soup.find("div", class_="area_view")
content = ''.join(map(str, _content.contents))
print "*" * 30
print content.strip()
print "-" * 30

