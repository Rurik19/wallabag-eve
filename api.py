# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import column_property
# from sqlalchemy import (
#     Column,
#     String,
#     Integer,
#     )

# Base = declarative_base()

# class Authors(Base):
#     __tablename__ = 'authors'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(120))
#     sort = Column(String(120))
#     link = Column(String(120))
#-------------------------------------------------------------------------------------------
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, backref

# engine = create_engine('sqlite:///C:\\Users\\yevdokimov\\Books\\calibre\\metadata.db1', convert_unicode=True, echo=False)
# Base = declarative_base()
# Base.metadata.reflect(engine)

# class Authors(Base):
#     __table__ = Base.metadata.tables['authors'] 
#     def _id(self):
#         return self.id
#-----------------------------------------------------------------------------------
DATA_URL='mysql://wallabag2:********@10.8.1.90:3306/wallabag2'
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
Base = automap_base()
engine = create_engine(DATA_URL, convert_unicode=True, echo=False)
Base.prepare(engine, reflect=True)

from eve_sqlalchemy import SQL 
from eve_sqlalchemy.validation import ValidatorSQL
from eve_sqlalchemy.decorators import registerSchema

Entries=Base.classes.wallabag_entry
#Books=Base.classes.books
#BALink=Base.classes.books_authors_link
#Comments=Base.classes.comments

from eve.utils import config

ID_FIELD = 'id'
ITEM_LOOKUP_FIELD = ID_FIELD
config.ID_FIELD = ID_FIELD
config.ITEM_LOOKUP_FIELD = ID_FIELD


registerSchema('entries')(Entries)
#registerSchema('books')(Books)
#//registerSchema('ba_link')(BALink)
#registerSchema('comments')(Comments)

SETTINGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': DATA_URL,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'DOMAIN': {
      'entries': Authors._eve_schema['entries'],
#      'books': Books._eve_schema['books'],
#      'ba_link': BALink._eve_schema['ba_link'],
#      'comments': Comments._eve_schema['comments'],
    },
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'ITEM_METHODS': ['GET', 'PATCH', 'PUT', 'DELETE']        
}

from eve import Eve
app = Eve(auth=None, settings=SETTINGS, validator=ValidatorSQL, data=SQL)

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base

app.run(debug=True, use_reloader=False)
