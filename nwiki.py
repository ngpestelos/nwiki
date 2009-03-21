#!/usr/bin/env python

import web, os

urls = (
  '/w/edit/(.*)', 'WikiEditor',
  '/w/(.*)', 'WikiPage',
  '/w', 'StartPage'
)

startPage = 'Welcome'

render = web.template.render('static/', base='site')

# don't create docs for these pages
#watch = ['browse', 'edit', 'about', 'home']

app = web.application(urls, globals())

def create(name, content):
    pass

def read(name):
    pass

def update(name, newcontent):
    pass

def delete(name):
    pass

class WikiEditor:
    def GET(self, name):
        return render.editor(name, '')
    def POST(self, name):
        input = web.input()
        if input.action == 'Cancel':
            raise web.seeother('/w')

class WikiPage:
    def GET(self, name):
        if not name:
            raise web.seeother('/w')

        return render.not_found(name)

class StartPage:
    def GET(self):
        raise web.seeother('/w/Welcome')

if __name__ == '__main__':
    app.run()
