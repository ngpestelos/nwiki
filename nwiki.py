# A simple CMS running on CouchDB and web.py

import web
from couchdb import Server
from couchdb import ResourceNotFound
import os
from datetime import datetime

render = web.template.render('static/')

urls = (
    '/edit/(.*)', 'WikiEditor',
    '/browse', 'WikiBrowser',
    '/(.*)', 'WikiPage'
)

startPage = 'GoAway'

# don't create docs for these pages
#watch = ['browse', 'edit', 'about', 'home']

server = Server('http://localhost:5984')
db = server['nwiki']

class WikiBrowser:
    def GET(self, dir='.'):
        doc = "<ul>"
        rows = ''
        for d in db:
            rows += '''<li><a href="%s">%s</a></li>''' % (d, d)
        doc += rows
        doc += '''</ul>'''
        print render.browser(doc)

class WikiEditor:
    def GET(self, name):
        try:
            doc = db[name]
            print render.editor(name, doc['content'])
        except ResourceNotFound:
            print render.editor(name, '')
    def POST(self, name):
        input = web.input()
        if input.action == 'Save':
            try:
                doc = db[name]
                doc['content'] = input.page
                doc['updated'] = datetime.today().ctime()
                db[name] = doc
                web.redirect('/%s' % name)
            except ResourceNotFound:
                posted = datetime.today().ctime()
                db[name] = {'content' : input.page, 'posted' : posted}
                web.redirect('/%s' % name)
        elif input.action == 'Cancel':
            web.redirect('/%s' % name)

class WikiPage:
    def GET(self, name):
        if not name:
            name = startPage
        try:
            doc = db[name]
            print render.default(name, doc['content'])
        except ResourceNotFound:
            edit = os.path.join('/edit', name)
            msg = '''<p>%s does not exist. <a href="%s">Create?</a></p>'''
            print render.default(name, msg % (name, edit))

if __name__ == "__main__":
    web.run(urls, globals())
