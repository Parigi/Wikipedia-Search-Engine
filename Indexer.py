import os
from Parser import getParsedPage
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.index import create_in

# Create the Schema
schema = Schema(id=NUMERIC, title=TEXT, body=TEXT, category=TEXT, infobox=TEXT, links=TEXT, URL=ID(stored=True))

# Create index
if not os.path.exists("index"):
  os.mkdir("index")
index = create_in("index", schema)

# Add parsed documents
writer = index.writer()
pages = getParsedPage()
for i in pages:
    writer.add_document(id=i[0], title=i[1], body=i[2], category=i[3], infobox=i[4], links=i[5], URL=i[6])
writer.commit()