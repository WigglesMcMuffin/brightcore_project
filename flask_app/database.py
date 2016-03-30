from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////code/tmp/test.db', convert_unicode=True) #Typically I use postgres, but sqlalchemy is db agnostic
db_session = scoped_session(sessionmaker(autocommit=False,					#For convenience I switched to sqlite
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import flask_app.models
    Base.metadata.create_all(bind=engine)