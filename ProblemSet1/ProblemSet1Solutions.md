Problem Set 1 

### Query all of the puppies and return the results in ascending alphabetical order

```
from sqlalchemy import asc
>>> for puppy in session.query(Puppy).order_by(Puppy.name):
...     print puppy.name
...     print "\n"
...
```

### Query all of the puppies that are less than 6 months old organized by the youngest first

```
>>> for puppy in session.query(Puppy).order_by(Puppy.dateOfBirth):
...     print puppy.name
...     print puppy.dateOfBirth
...     print "\n"
```

### Query all puppies by ascending weight

```
>>> for puppy in session.query(Puppy).order_by(asc(Puppy.weight)):... 
...     print puppy.name
...     print puppy.weight
...     print "\n"
```

### Query all puppies grouped by the shelter in which they are staying

```
>>> for puppy in session.query(Puppy).order_by(asc(Puppy.shelter_id)):
...     print puppy.shelter_id
...     print "\n"
```