'''Design docs go here'''

from couchdb import Server

db = Server()['nwiki']

articles = {
  "language" : "javascript",
  "views" : {
    "by_title" : {
      "map" : """function(doc) {
                   if (doc.type == 'article') emit(doc.title, doc);
                 }"""
    }
  }
}

if not db.get('_design/articles', None):
    db['_design/articles'] = articles
