import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	id = Column(Integer,primary_key=True)
	name = Column(String(250),nullable=False)

	# for API to jsonify data
	@property
	def serialize(self):
		# return object data in easily serializeable format
	    return {
	    	'name':self.name,
	    	'id': self.id,
	    }

class MenuItem(Base):
	__tablename__ = 'menu_item'
	id = Column(Integer,primary_key=True)
	name = Column(String(250),nullable=False)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(250))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
	    return {
	    	'name': self.name,
	    	'price': self.price,
	    	'id': self.id,
	    	'price': self.price,
	    	'course':self.course,
	    }
	
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)