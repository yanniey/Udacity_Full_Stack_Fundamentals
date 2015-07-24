# UD088 - Udacity's Full Stack Fundamentals course
[Course Link](https://www.udacity.com/course/full-stack-foundations--ud088)

Python + SQLAlchemy + MySql+ Flask

Lesson 1, completed 07/16/2015

Lesson 2, completed 07/21/2015

## Syllabus

+ Lesson 1 - Working with the CRUD

In the first lesson, you will learn about CRUD; Create, Read, Update, and Delete. You will learn why this acronym is important in web development and implement CRUD operations on a database. You will also learn to use an ORM (Object-Relational Mapping) as an alternative to SQL.

+ Lesson 2 - Making a Web Server

In the second lesson, you will build a web server from scratch using Python and some of the pre-installed libraries it includes. You will learn what GET and POST requests are and how we use them to retrieve and modify information on a web site. We will then use the concepts learned in Lesson 1 to add CRUD functionality to our website.

+ Lesson 3 - Developing with Frameworks

In the third lesson, we will discuss web frameworks like Django and Ruby on Rails. You will see how web frameworks simplify the development process and allow us to create web applications faster. We will use the Flask web framework to develop our own web application. We will also discuss API's (Application Programming Interfaces) and add JSON (JavaScript Object Notation) endpoints to our application to allow data to be sent in a format alternative to HTML.

+ Lesson 4 - Iterative Development

In the last lesson, you will build an entire web application on your own. You will learn about the iterative development process and how developing iteratively allows you to have a working prototype throughout all stages of the development process.

---

Lesson 3 Notes

Using Flask: views are under the `templates` folder, call with `render_template(template,variable)`

Flask functions: 
+ `@app.route('/',method=['GET','POST'])`
+ `render_template`
+ `url_for()`
+ `redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))`

---

Lesson 1 Notes

## Setup

```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
```
OR

```
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> from database_setup import Base,Restaurant, MenuItem
>>> engine = create_engine('sqlite:///restaurantmenu.db')
>>> Base.metadata.bind=engine
>>> DBSession=sessionmaker(bind=engine)
>>> session=DBSession()
>>> AnyiFirstRestaurant = Restaurant(name="Bamboo Palace")
>>> session.add(AnyiFirstRestaurant)
>>> session.commit()
>>> session.query(Restaurant).all()
[<database_setup.Restaurant object at 0xb6b485ac>]
```





## add MenuItem

```
>>> ramen = MenuItem(name="Ramen",description = "Anyi's favorite comfort food", course="Entree",price="$10.99",restaurant=AnyiFirstRestaurant)
>>> session.add(ramen)
>>> session.commit()
>>> session.query(MenuItem).all()
[<database_setup.MenuItem object at 0xb6b485ec>]
```

## First Result

```
>>> firstResult = session.query(Restaurant).first()
>>> firstResult
<database_setup.Restaurant object at 0xb6b485ac>
>>> firstResult.name
u'Bamboo Palace'
```

## Update an item

```
>>>veggieBurgers = session.query(MenuItem).filter_by(name="Veggie Burger")

>>> for veggieBurger in veggieBurgers:
...     print veggieBurger.id
...     print veggieBurger.price
...     print veggieBurger.restaurant.name
...     print "\n"

2
$7.50
Urban Burger


10
$5.99
Urban Burger


21
$9.50
Panda Garden


27
$6.80
Thyme for That Vegetarian Cuisine


37
$7.00
Andala's


43
$9.50
Auntie Ann's Diner'


>>> UrbanVeggieBurger = session.query(MenuItem).filter_by(id=2).one()
>>> print UrbanVeggieBurger.price
$7.50

>>> UrbanVeggieBurger.price = '$2.99'
>>> session.add(UrbanVeggieBurger)
>>> session.commit()
```

## Update multiple items

```
>>> for veggieBurger in veggieBurgers:
...     if veggieBurger.price !="$2.99":
...             veggieBurger.price = "$2.99"
...             session.add(veggieBurger)
...             session.commit()
```

## Delete an item

```
>>> spinach = session.query(MenuItem).filter_by(name="Spinach Ice Cream").one()
>>> print spinach.name
Spinach Ice Cream
>>> print spinach.restaurant.name
Auntie Ann's Diner'
>>> session.delete(spinach)
>>> session.commit()
```