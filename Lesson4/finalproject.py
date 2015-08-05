# Set up
from flask import Flask,render_template, request, redirect, jsonify, url_for,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
 
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# # Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# # Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


# API Endpoint

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(Menu_Item=Menu_Item.serialize)

# list all restaurants
@app.route('/restaurant/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurants = [r.serialize for r in restaurants])



# Routing
@app.route("/")
@app.route("/restaurant/")
def showRestaurants():
	# this page will show all the restaurants
	restaurants = session.query(Restaurant).all()
	return render_template("restaurants.html",restaurants=restaurants)

# create a new restaurant
@app.route("/restaurant/new/",methods = ['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template("newRestaurant.html")

# edit a restaurant
@app.route("/restaurant/<int:restaurant_id>/edit/", methods = ['GET','POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
			return redirect(url_for('showRestaurants'))
	else:
		return render_template("editRestaurant.html",restaurant=editedRestaurant)

# delete a restaurant
@app.route("/restaurant/<int:restaurant_id>/delete/", methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		return redirect(url_for('showRestaurants',restaurant_id = restaurant_id))
	else:
		return render_template("deleteRestaurant.html",restaurant = restaurantToDelete)

# show restaurant menu
@app.route("/restaurant/<int:restaurant_id>/")
@app.route("/restaurant/<int:restaurant_id>/menu/")
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template("showMenu.html",restaurant=restaurant)

# create a new menu item
@app.route("/restaurant/<int:restaurant_id>/menu/new/", methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'],description = request.form['description'],price = request.form['price'],course = request.form['course'],restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for("showMenu",restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html',restaurant_id = restaurant_id)


@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/", methods = ['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
	editItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editItem.name = request.form['name']
		if request.form['description']:
			editItem.description = request.form['description']
		if request.form['price']:
			editItem.price = request.form['price']
		if request.form['course']:
			editItem.course = request.form['course']
		session.add(editMenuItem)
		session.commit()
		return redirect(url_for('showMenu',restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html',restaurant_id = restaurant_id, menu_id = menu_id, item = editItem)

# delete a menu item

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/", methods = ['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('showMenu',restaurant_id = restaurant_id))
	else:
		return render_template('deleteMenuItem.html', item = itemToDelete)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
