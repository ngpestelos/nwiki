import web

urls = (
  '/w/(.*)', 'StartPage'
)

startPage = 'Welcome'

# don't create docs for these pages
#watch = ['browse', 'edit', 'about', 'home']

app = web.application(urls, globals())

class StartPage:
    def GET(self, name):
        return "here we go again! All Hail Britannia!"
