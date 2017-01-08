# -*- coding: utf-8 -*-

import json
from jinja2 import Environment, PackageLoader


with open('tistory.json') as fp:
    posts = json.load(fp)

#posts = posts[460:468]

env = Environment(loader=PackageLoader('wp', 'templates'))
template = env.get_template('post.xml')
export =  template.render(posts=posts).encode("utf8")
#print posts[0]

# to save the results
with open("export.xml", "wb") as fp:
    fp.write(export)
