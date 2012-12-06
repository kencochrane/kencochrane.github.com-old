#!/usr/bin/env python

from MySQLdb import connect
from MySQLdb.cursors import DictCursor
import os

OUTPUT_DIR = '/tmp/blog_convert/'

FILE_NAME = "{slug}.{ext}"

TEMPLATE = """
:date: {blog_date}
:tags: {tags}
:category: blog
:slug: {slug}
:author: Ken Cochrane
:title: {title}

{content}

"""


db = connect(host='127.0.0.1', user='root', passwd='', db='blog')

dict_curr = DictCursor(db)
dict_curr.execute("select * from blog_entries")

results = dict_curr.fetchall()

for result in results:
    slug = result.get('slug', None)
    title = result.get('title', None)
    orig_tags = result.get('tags', "")
    blog_date = result.get('pub_date')
    content = result.get('body')
    format = result.get('format', 'REST')
    if format == 'REST':
        ext = 'rst'
    else:
        ext = 'html'
    output_file = os.path.join(OUTPUT_DIR, FILE_NAME.format(slug=slug, ext=ext))
    tags=",".join(orig_tags.split(" "))
    print(title)
    with file(output_file, 'w') as f:
        f.write(TEMPLATE.format(
                            blog_date=blog_date,
                            tags=tags,
                            slug=slug,
                            title=title,
                            content=content,
                        )
                    )