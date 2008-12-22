# A simple CMS running on CouchDB and web.py

import web
from couchdb import Server
from couchdb import ResourceNotFound
import os
from datetime import datetime
from markdown import markdown

render = web.template.render('static/')

urls = (
    '/rename', 'Rename',
    '/edit/(.*)', 'WikiEditor',
    '/browse', 'WikiBrowser',
    '/(.*)', 'WikiPage'
)

startPage = 'GoAway'

# don't create docs for these pages
#watch = ['browse', 'edit', 'about', 'home']

server = Server('http://localhost:5984')
db = server['nwiki']

app = web.application(urls, globals(), autoreload=True)

class Rename:
    def POST(self):
        input = web.input()
        if input.action == 'Save':
            doc = db[input.d]
            posted = ''
            if 'posted' in doc:
                posted = doc['posted']
            db[input.new_name] = {'content' : doc['content'], \
              'posted' : posted, 'updated' : datetime.today().ctime()}
            del db[input.d]
            web.redirect("/browse")
        elif input.action == 'Cancel':
            web.redirect("/browse")
    def GET(self):
        input = web.input()
        return render.rename(input.d)

class WikiBrowser:
    def GET(self):
        return render.browser([doc for doc in db])

class WikiEditor:
    def GET(self, name):
        try:
            doc = db[name]
            return render.editor(name, doc['content'])
        except ResourceNotFound:
            return render.editor(name, '')
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
            #content = web.utils.safemarkdown(doc['content'])
            content = markdown(doc['content'])
            return render.site(name, content)
        except ResourceNotFound:
            edit = os.path.join('/edit', name)
            msg = '''<p>%s does not exist. <a href="%s">Create?</a></p>'''
            return render.site(name, msg % (name, edit))

if __name__ == "__main__":
    app.run()
