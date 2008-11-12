# A simple CMS running on CouchDB and web.py

import web
from couchdb import Server
from couchdb import ResourceNotFound
import os

urls = (
    '/edit/(.*)', 'WikiEditor',
    '/(.*)', 'WikiPage'
)

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
              <li><a href="#">Home</a></li>
              <li><a href="#">Edit</a></li>
              <li><a href="#">Browse</a></li>
              <li><a href="#">About</a></li>
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
  return page % (title, title, content)

class WikiEditor:
    def __init__(self):
        self.db = Server('http://localhost:5984')['nwiki']

    def form(self, name, document=''):
        doc = '''
        <h2>You are editing %s</h2>
        <form method="post" accept-charset="utf-8" action="%s">
          <input name="fname" type="hidden" value="%s" />
          <textarea name="page" cols="100" rows="20">%s</textarea>
          <br /><br />
          <input name="action" type="submit" value="Update" />&nbsp;
          <input name="action" type="submit" value="Preview" />&nbsp;
          <input name="action" type="submit" value="Discard" />
        </form>
        '''
        return doc % (name, name, name, document)

    def GET(self, name):
        wiki = ''
        doc = self.form(name, wiki)
        print skeleton(name, doc)

class WikiPage:
    def __init__(self):
        self.db = Server('http://localhost:5984')['nwiki']

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
            doc = self.db[name]
            print skeleton(name, doc['content'])
        except ResourceNotFound:
            print skeleton(name, self.info(name, 'dne'))

if __name__ == "__main__":
    web.run(urls, globals())
