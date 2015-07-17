Lesson 1 Note
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