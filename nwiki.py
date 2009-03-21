#!/usr/bin/env python

import web, os

urls = (
  '/w/(.*)', 'WikiPage',
  '/w', 'StartPage'
)

startPage = 'Welcome'

render = web.template.render('static/', base='site')

renderBare = web.template.render('static/')

# don't create docs for these pages
#watch = ['browse', 'edit', 'about', 'home']

app = web.application(urls, globals())

class WikiPage:
    def GET(self, name):
        if not name:
            raise web.seeother('/w')

        editUrl = os.path.join('/w/edit', name)
        msg = '<h3 id="notfound">%s does not exist. <a href="%s">Create?</a></h3>'
        return renderBare.site(name, msg % (name, editUrl))

class StartPage:
    def GET(self):
        raise web.seeother('/w/Welcome')

if __name__ == '__main__':
    app.run()
