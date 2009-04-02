#!/usr/bin/env python

import web, os
from couchdb import Server
from datetime import datetime
from markdown import markdown

urls = (
  '/w/edit/(.*)', 'Editor',
  '/w/(.*)', 'Page',
  '/w', 'Start'
)

startPage = 'Welcome'

render = web.template.render('html/', base='site')
render_bare = web.template.render('html/')

app = web.application(urls, globals())

db = Server()['nwiki']

def create(slug, content):
    doc = {'slug' : slug, 'body' : content, 'format' : 'markdown', \
      'html' : markdown(content), 'rev_number' : 0, \
      'posted' : datetime.today().ctime()}
    return db.create(doc)

#def create(name, content):
#    doc = {'content' : content, 'created' : datetime.today().ctime(), \
#      'title': name, 'type' : 'article'}
#    return db.create(doc)

#def read(name):
#    results = db.view('articles/slugs', key=name)
#    if len(results) == 0:
#        return None
#    return results.rows[0].value

#def update(doc, newcontent):
#    doc['updated'] = datetime.today().ctime()
#    doc['content'] = newcontent
#    id = doc['_id']
#    db[id] = doc

#def delete(name):
#    pass

class AboutPage:
    def GET(self):
        return render.about()

class Editor:
    def GET(self, slug):
        return render.editor(slug, '')

    def POST(self, slug):
        input = web.input()
        if input.action == 'Cancel':
            raise web.seeother('/w')

        create(slug, input.content)
        raise web.seeother('/w/%s' % slug)

class Page:
    def GET(self, slug):
        if not slug:
            raise web.seeother('/w')

        if slug[0].islower():
            slug = slug[0].upper() + slug[1:]

        return render.not_found(slug)

class Start:
    def GET(self):
        return render_bare.welcome()

if __name__ == '__main__':
    app.run()
