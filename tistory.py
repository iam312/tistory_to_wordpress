# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

### to file
##with open("test.html", "w") as f:
##        f.write(raw_html.encode("utf-8"))

# from file
with open("test.html", "r") as f:
    raw_html = f.read()

def parse(raw_html) :
    post = {}

    soup = BeautifulSoup(raw_html, 'html.parser')

    ###############################
    # title
    ###############################
    title = soup.find("h3", class_="tit_post").text
    post['title'] = title
#    print "*" * 30
#    print title
#    print "-" * 30


    ###############################
    # reg date
    ###############################
    regdate = soup.find("span", class_="info_post").text
    post['regdate'] = regdate.split("\n")[1].strip()
#    print "*" * 30
#    print regdate.split("\n")[1].strip()
#    print "-" * 30



    ###############################
    # contents
    ###############################
    # remove ccl
    ccl = soup.find('div', style="width:100%;margin-top:30px;clear:both;height:30px")
    ccl.decompose()

    # remove category
    cate = soup.find('div', class_="another_category another_category_color_gray")
    if cate is not None :
        cate.decompose()

    # remove Exifinfo
    exifinfos = soup.find_all('span', class_="ExifInfo")
    for exifinfo in exifinfos :
        exifinfo.decompose()

    _content = soup.find("div", class_="area_view")
    #content = ''.join(map(str, _content.contents))
    content = ''.join(map(lambda s: s.encode('utf8'), _content.contents))
    post['contents'] = content.strip()
#    print "*" * 30
#    print content.strip()
#    print "-" * 30

    comments = []
    comments_area = soup.find("ul", class_="list_reply")
    if comments_area is not None :
        _comments = comments_area.find_all("li")
        for _comment in _comments :
            secret = False
            if 'rp_secret' in  _comment['class'] :
                secret = True

            reply_reply = False
            if 're_reply' in  _comment['class'] :
                reply_reply = True

            if secret :
                comment_regdate = "2001.01.01 00:00:00"
                comment_author = "anonymous"
                comment_text = "secret comment."
            else :
                comment_regdate = _comment.find("span", "txt_date")
                comment_regdate.a.decompose()
                comment_regdate = comment_regdate.text
                comment_author = _comment.find("span", "tit_nickname")
                comment_author = comment_author.text
                comment_text = _comment.find("span", "txt_reply")
                comment_text = comment_text.text
            comment = {}
            comment["author"] = comment_author
            comment["regdate"] = comment_regdate
            comment["text"] = comment_text
            comment["reply_reply"] = reply_reply
            comments.append(comment)

        post['comments'] = comments
    #    print "*" * 30
    #    print comments
    #    print "-" * 30

    return post

#post = parse(raw_html)
#print post

def fetch() :
    posts = []

    for id in range(1, 557) :
    #for id in range(526, 527) :
    #for id in range(269, 270) :
        # fetch url
        url = 'http://iam312.pe.kr/{}'.format(id)
        print url
        r = requests.get(url, headers=headers)
        if not r.status_code == requests.codes.ok :
            continue

        raw_html = r.text

        post = parse(raw_html)
        posts.append(post)

    return posts

posts = fetch()
#print posts
#print posts

import json
with open('tistory.json', 'w') as fp:
    json.dump(posts, fp)

