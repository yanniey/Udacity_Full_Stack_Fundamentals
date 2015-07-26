# Set up
from flask import Flask,render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}



# Routing


@app.route("/")
@app.route("/restaurant/")
def showRestaurants():
	# this page will show all the restaurants
	return render_template("restaurants.html",restaurants=restaurants)

@app.route("/restaurant/new/")
def newRestaurant():
	return "create new restaurant"

@app.route("/restaurant/<int:restaurant_id>/edit/")
def editRestaurant(restaurant_id):
	return "edit restaurant %s" %restaurant_id

@app.route("/restaurant/<int:restaurant_id>/delete/")
def deleteRestaurant(restaurant_id):
	return "delete restaurant %s" %restaurant_id

@app.route("/restaurant/<int:restaurant_id>/")
@app.route("/restaurant/<int:restaurant_id>/menu/")
def showMenu(restaurant_id):
	return "restaurant menu page %s" %restaurant_id

@app.route("/restaurant/<int:restaurant_id>/menu/new/")
def newMenuItem(restaurant_id):
	return "new menu item %s " %restaurant_id

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/")
def editMenuItem(restaurant_id,menu_id):
	return render_template("editMenuItem.html",item_id = menu_id)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/")
def deleteMenuItem(restaurant_id,menu_id):
	return "delete menu item %s" %menu_id



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
