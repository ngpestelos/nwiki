'''Design docs go here'''

from couchdb import Server

db = Server()['nwiki']

articles = {
  "language" : "javascript",
  "views" : {
    "slugs" : {
      "map" : "function(doc) { if (doc.type == 'post') emit(doc.slug, doc); }"
    }
  }
}

if not db.get('_design/articles', None):
    db['_design/articles'] = articles
