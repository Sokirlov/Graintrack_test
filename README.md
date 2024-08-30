# Test work for https://graintrack.com/
Demo api for shop.

## Firs start
```shell
python manage.py makemigrations && python manage.py migrate && \
python manage.py createsuperuser && \
python manage.py loaddata shop
```
 
## About API

### Categorys
This endpoint support methods 
- GET

List of categories according to nesting hierarchy 

___

### Products
This endpoint support methods

_Anyone_
- GET

_Authenticate_
- POST
- PUT
- PATCH
- DELETE

___

### Orders
This endpoint support methods:

_The **USER** sees only his orders_
- GET
- POST
- PUT

_The **STAFF** sees only his orders_
- GET
- POST
- PUT
