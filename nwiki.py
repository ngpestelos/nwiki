#!/usr/bin/env python

import web, os
from couchdb import Server
from datetime import datetime
from markdown import markdown

urls = (
  '/w/About', 'AboutPage',
  '/w/edit/(.*)', 'WikiEditor',
  '/w/(.*)', 'WikiPage',
  '/w', 'StartPage'
)

startPage = 'Welcome'

render = web.template.render('static/', base='site')

# don't create docs for these pages
#watch = ['browse', 'edit', 'about', 'home']

app = web.application(urls, globals())

db = Server()['nwiki']

def create(name, content):
    doc = {'content' : content, 'created' : datetime.today().ctime(), \
      'title': name, 'type' : 'article'}
    return db.create(doc)

def read(name):
    results = db.view('articles/by_title', key=name)
    if len(results) == 0:
        return None
    return results.rows[0].value

def update(doc, newcontent):
    doc['updated'] = datetime.today().ctime()
    doc['content'] = newcontent
    id = doc['_id']
    db[id] = doc

def delete(name):
    pass


class AboutPage:
    def GET(self):
        return render.about()

class WikiEditor:
    def GET(self, name):
        doc = read(name)
        if doc:
            return render.editor(doc['title'], doc['content'])
        else:
            return render.editor(name, '')

    def POST(self, name):
        input = web.input()
        if input.action == 'Cancel':
            raise web.seeother('/w')

        doc = read(name)
        if doc:
            update(doc, input.page)
        else:
            create(name, input.page)

        raise web.seeother('/w/%s' % name)


class WikiPage:
    def GET(self, name):
        if not name:
            raise web.seeother('/w')

        if name[0].islower():
            name = name[0].upper() + name[1:]

        doc = read(name)
        if not doc:
            return render.not_found(name)
        else:
            content = markdown(doc['content'])
            return render.article(doc['title'], content)


class StartPage:
    def GET(self):
        raise web.seeother('/w/Welcome')

if __name__ == '__main__':
    app.run()
