# A simple CMS running on CouchDB and web.py

import web
from couchdb import Server
from couchdb import ResourceNotFound
import os
from datetime import datetime

urls = (
    '/edit/(.*)', 'WikiEditor',
    '/browse', 'WikiBrowser',
    '/(.*)', 'WikiPage'
)

server = Server('http://localhost:5984')
db = server['nwiki']

def skeleton(title, content):
  page = '''
    <!DOCTYPE html PUBLIC "-//W3C/DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
      <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <title>%s - nwiki</title>
      <link rel="stylesheet" media="screen" type="text/css" href="/static/css/style.css" />
      </head>
      <body>
        <div id="masthead">
          <div id="logo">
            <img src="/static/images/jolly.jpeg" />
          </div>
          <h1>%s</h1>
          <div id="mainCol">
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/edit/%s">Edit</a></li>
              <li><a href="/browse">Browse</a></li>
              <li><a href="/About">About</a></li>
            </ul>
          </div>
        </div>
        <div id="content">
          %s
        </div>
        <div id="sidebar">
        </div>
        <div id="footer">
          &copy; 2008 Nestor G Pestelos Jr (ngpestelos@gmail.com)
        </div>
      </body>
    </html>
  '''
  return page % (title, title, title, content)

class WikiBrowser:
    def GET(self, dir='.'):
        doc = "<ul>"
        rows = ''
        for document in db:
          rows += """
          <li><a href="/%s">%s</a></li>
          """ % (document, document)
        doc += rows
        doc += "</ul>"
        print skeleton("Browse", doc)

class WikiEditor:
    def form(self, name, document=''):
        doc = '''
        <h2>You are editing %s</h2>
        <form method="post" accept-charset="utf-8" action="/edit/%s">
          <input name="fname" type="hidden" value="%s" />
          <textarea name="page" cols="100" rows="20">%s</textarea>
          <br /><br />
          <input name="action" type="submit" value="Update" />&nbsp;
          <input name="action" type="submit" value="Discard" />
        </form>
        '''
        return doc % (name, name, name, document)

    def GET(self, name):
        try:
            doc = db[name]
            editor = self.form(name, doc['content'])
            print skeleton(name, editor)
        except ResourceNotFound:
            editor = self.form(name, '')
            print skeleton(name, editor)

    def POST(self, name):
        inparms = web.input()
        if inparms.action == 'Update':
            try:
                updated = datetime.now().isoformat()
                doc = db[name]
                doc['content'] = inparms.page 
                doc['updated'] = updated
                db[name] = doc
                web.redirect('/%s' % (name))
            except ResourceNotFound:
                posted = datetime.now().isoformat()
                db[name] = {'content' : inparms.page, 'posted' : posted}
                web.redirect('/%s' % (name))
        elif inparms.action == 'Discard':
            web.redirect('/%s' % (name))

class WikiPage:
    def info(self, name, type):
        if type == 'dne':
            msg = '''
            <p>
              %s does not exist. <a href="%s">Create?</a>
            </p>
            '''
            return msg % (name, os.path.join('/edit', name))
        else:
            return ''

    def GET(self, name):
        if name == '/' or name == '' or not name:
            name='GoAway'
        try:
            doc = db[name]
            print skeleton(name, doc['content'])
        except ResourceNotFound:
            print skeleton(name, self.info(name, 'dne'))

if __name__ == "__main__":
    web.run(urls, globals())
