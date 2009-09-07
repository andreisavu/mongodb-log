
import web

from pymongo.connection import Connection

import settings

urls = (
    '/', 'index'
)

app = web.application(urls, globals())
render = web.template.render('templates/', base='base')

class index:
    def GET(self):
        return render.index()

if __name__ == '__main__':
    app.run()

