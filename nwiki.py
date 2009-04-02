#!/usr/bin/env python

import web, os
from couchdb import Server
from datetime import datetime
from markdown import markdown

urls = (
  '/w/[a|A]bout', 'About',
  '/w/[h|H]ome', 'Start',
  '/w/[e|E]dit/(.*)', 'Editor',
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
      'html' : markdown(content), \
      'posted' : datetime.today().ctime(), 'type' : post}
    return db.create(doc)

def read(slug):
    fun = '''
    function(doc) {
      if (doc.type == 'post' && doc.slug == '%s')
        emit([doc.slug, doc.posted], doc);
    }''' % slug
    res = [r for r in db.query(fun)]
    if len(res) == 0:
        return None
    else:
        return res[-1].value

def update(doc, newcontent):
    newdoc = {'slug' : doc['slug'], 'body' : newcontent, \
      'format' : 'markdown', 'html' : markdown(newcontent), \
      'posted' : datetime.today().ctime(), 'type' : 'post'}
    return db.create(newdoc)

class AboutPage:
    def GET(self):
        return render.about()

class Editor:
    def GET(self, slug):
        doc = read(slug)
        if doc:
            return render.editor(doc['slug'], doc['body'])
        else:
            return render.editor(slug, '')

    def POST(self, slug):
        input = web.input()
        if input.action == 'Cancel':
            raise web.seeother('/w')

        doc = read(slug)
        if doc:
            update(doc, input.content)
        else:
            create(slug, input.content)

        raise web.seeother('/w/%s' % slug)

class Page:
    def GET(self, slug):
        if not slug:
            raise web.seeother('/w')

        if slug[0].islower():
            slug = slug[0].upper() + slug[1:]

        doc = read(slug)
        if not doc:
            return render.not_found(slug)
        else:
            return render.page(doc['slug'], doc['html'])

class Start:
    def GET(self):
        return render_bare.welcome()

class About:
    def GET(self):
        return render_bare.about()

if __name__ == '__main__':
    app.run()
