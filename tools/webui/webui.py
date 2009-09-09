
import web

from pymongo.connection import Connection
from pymongo import ASCENDING, DESCENDING

import settings

urls = (
    '/(.*)', 'index'
)

def get_mongo_collection(db, collection, host, port):
    return Connection(host, port)[db][collection]

app = web.application(urls, globals())
render = web.template.render('templates/', base='base')
db = get_mongo_collection(**settings.MONGO)

class index:
    def GET(self, level):
        args = {}
        if level and level in ['info', 'debug', 'warning', 'error', 'critical']:
            args = {'level':level}

        def fill_missing(el):
            if not 'host' in el:
                el['host'] = '(unknow)'
            return el            
        logs = map(fill_missing, db.find(args, limit=100).sort('$natural', DESCENDING))

        return render.index(logs)

if __name__ == '__main__':
    app.run()

