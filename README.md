# Auction-service
Simple API for an auction service using Django Rest Framework

test cases are in **api/tests.py** 

## Getting started
1. Install docker and Docker-compose for easy setup. 

2. Run `docker-compose build && docker-compose up -d`. You should get this output 
   **Recreating auction-server ... done**
   
   **NOTE**: To run the testcases execute `docker exec -it auction-server  python manage.py test`.
   Server should be up and running and visiting http://127.0.0.1:8000/api/v1/ should return a page with a list of some of the    endpoints. 

3. Create user(s). See sample request below
```
POST /api/v1/users HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
    "username": "user_1",
    "email": "user_1@gmail.com"
}

```

4. Add item(s)
```
POST /api/v1/items HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
    "name": "item_1",
    "product_code": "ITEM/QWERTY/1",
    "description": "this is a placeholder description",
    "sold": false
}

```

5. Place bid(s) by sending item id, user id and amount
```
POST /api/v1/bids HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
    "item": 1,
    "user": 1,
    "bid_amount": 5000
}
```

6. Get the current winning bid for an item
  - first get list of items
  ```
  GET /api/v1/items HTTP/1.1
  Host: 127.0.0.1:8000

  ```
  - Use a returned item id in step a to get current winning bid. For example for item with ID 1 
  ```
  GET /api/v1/item/<item_id>/winner HTTP/1.1
   Host: 127.0.0.1:8000
   Content-Type: application/json
  ```
  ```
  SAMPLE RESPONSE:
  {
    "id": 1,
    "item": 1,
    "user": {
        "id": 1,
        "username": "patrickcmd",
        "email": "patrick@gmail.com"
    },
    "bid_time": "2019-12-22T21:30:23.564362Z",
    "bid_amount": "5000.00"
  }
  ```
 
  7. Get all the bids for an item
  ```
  GET /api/v1/item/<item_id>/bids HTTP/1.1
  Host: 127.0.0.1:8000
  Content-Type: application/json
  ```
  
  8. Get all the items on which a user has bid
  ```
  GET /api/v1/user/<user_id>/bids/items HTTP/1.1
  Host: 127.0.0.1:8000
  Content-Type: application/json
  ```
  ```
  SAMPLE RESPONSE:
[
    {
        "id": 1,
        "name": "item_1",
        "product_code": "ITEM/QWERTY/1",
        "description": "this is a placeholder description",
        "sold": false
    }
]
  ```
  
## Data Structures Used
The Django ORM was used to create classes for **Items Table**, **Users Table**  and **Bids Tables**. The database engine used for this project is Postgres which is an RDBMS. One object worthy of note is the Bid class.
```
class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_time = models.DateTimeField(auto_now_add=True) 
    bid_amount =  models.DecimalField(decimal_places=2, max_digits=10)

```

**Note**: Complete implementation can be found in `api/models.py` 

## Concurrency approach
When this application is started, a docker container spins up two services.
1. *auction-db* :  this is a postgres database server. Postgres is a SQL database with ACID properties that will place a lock on resources during writes. Therefore, only one write can happen a time to maintain integrity. The timestamp on a bid is determined by the write time and this helps to prevent ties.

2. *auction-server*: a gunicorn webserver with 4 workers. Each of the workers is a UNIX process that loads an instance of the Python application. This makes it possible for concurrent requests to be handled by any of the 4 workers 

