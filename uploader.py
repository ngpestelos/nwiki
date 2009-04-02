'''Upload contents from an older database (pre 0.4)'''

from couchdb import Server
from datetime import datetime
from markdown import markdown

SRC_ADDRESS = 'http://192.168.1.200:5984'
SRC_DB = 'nwiki_20090217'

srcdb = Server(SRC_ADDRESS)[SRC_DB]
destdb = Server()['nwiki']


map_fun = '''function(doc) { emit(doc._id, doc); }'''
results = [r.value for r in srcdb.query(map_fun)]

for doc in results:
    print doc['_id']
    today = datetime.today().ctime()
    newdoc = {'slug' : doc['_id'], 'posted' : doc.get('posted', today), \
      'format' : 'markdown', 'body' : doc['content'], \
      'html' : markdown(doc['content']), 'type' : 'post'}
    destdb.create(newdoc)
