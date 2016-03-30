from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.types import Date, DateTime
from sqlalchemy.orm import relationship

from flask_app.database import Base, db_session

class Feature(Base):
	__tablename__ = 'features'
	id = Column(Integer, primary_key=True)
	title = Column(String(50))
	description = Column(Text)
	client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
	client = relationship("Client", foreign_keys=[client_id])
	client_priority = Column(Integer)
	target_date = Column(Date)
	ticket_url = Column(String(300))
	product_area_id = Column(Integer, ForeignKey('products.id'), nullable=False)
	product_area = relationship("Product", foreign_keys=[product_area_id])
	
	def __init__(self, title=None, description=None, client_id=None, client_priority=None, target_date=None, ticket_url=None, product_area_id=None):
		#typically check for values here, but as SQL has a conecpt of nullable fields
		#I tend to leave that validation to that layer, to keep responsibilities in line and code clean
		self.title = title
		self.description = description
		self.client_id = client_id
		priorities = Feature.query.filter(Feature.client_id == client_id) #To save lookups, this value is saved as it's called repeatedly
		if client_priority == None or client_priority < 1: #consideration: -1 for denoting "doesn't need to be done, but would be nice"
			client_priority = len(priorities.all()) + 1
		else:
			for f in prorities.filter(Feature.client_priority >= client_priority).all():
				f.client_priority += 1
			client_priority = min(len(priorities) + 1, client_priority) #To keep the priorities list only consequetive integers
			db_session.commit()
		self.client_priority = client_priority
		self.target_date = target_date
		self.ticket_url = ticket_url
		self.product_area_id = product_area_id
    
	def __repr__(self):
		return '<feature %r - from %r>' % (self.title, self.client.name)
		
class Client(Base):
	__tablename__ = 'clients'
	id = Column(Integer, primary_key=True) #Almost certainly a uuid in a production environment
	name = Column(String(50), unique=True)
	#Other pertainent info here:
	#Probably things like contact info
	
	def __init__(self, name=None):
		self.name = name
		
	def __repr__(self):
		return '<Client %s>' % (self.name)
		
class Product(Base):
	__tablename__ = 'products'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True)
	
	def __init__(self, name=None):
		self.name = name