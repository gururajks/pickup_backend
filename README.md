# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Please use a virtual environment. Use this `virtualenv venv` 

#### PIP Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- Flask
- Flask CORS
- Flask SQLAlchemy

## Database Setup
You need to run migration commands.
Make sure psql is installed. 
```bash
createdb pickup
flask db migrate
flask db upgrade
```

## Running the server

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Motivation

Given the current situation with Covid-19, pickup, deliveries and online purchasing has increased. I wanted to create the backend for a customer-merchant delivery system.
This project reflects the start of that project. 
Here in this project the customer is able to make orders to a merchant. The merchant is able to view the details of the order created. 
Along with that, the customer and merchant are able to make changes to their profile information.


## Testing
To run the tests, run this
using the same database you created before.
Make sure you have run the app before running the tests as the databases and tables needs to be created
```
python test_app.py
```


## API Documentation

### `GET /customers/<int:customer_id>`

Get the information of a particular customer
##### Request
Eg: `curl http://localhost:5000/customers/1`

##### Response
```
{
    "customer": {
        "city": "Austin",
        "email": "doofu@gmail.com",
        "id": 1,
        "name": "Doofu"
    }
}
```

### `GET /merchants/<int:merchant_id>`

Get the information of a particular merchant
##### Request
Eg: `curl http://localhost:5000/merchants/1`

##### Response
```
{
    "merchant": {
        "city": "Austin",
        "email": "doofu@gmail.com",
        "id": 1,
        "name": "Doofu"
    }
}
```

### `POST /customers`

Create a new Customer

##### Request

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| name |  string |
| city | string   |
| email | string |


##### Response
```
{
    "customer": {
        "city": "Boston",
        "email": "doofuBos@gmail.com",
        "id": 2,
        "name": "DoofuBoston"
    },
    "success": true
}
```

### `PATCH /customers/<int:customer_id>`

Update customer information

##### Request

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| name |  string |
| city | string   |
| email | string |

Payload
```
{
    "name" : "Doofu",
    "city" : "Boston",
    "email" : "doofuBos@gmail.com"
}
```

##### Response
```
{
    "customer": {
        "city": "Boston",
        "email": "doofuBos@gmail.com",
        "id": 2,
        "name": "DoofuBoston"
    },
    "success": true
}
```


### `DELETE /customers/<int:customer_id>`

Delete a Customer

##### Request


Eg: `curl -X DELETE http://localhost:5000/customers/1`

##### Response
```
{
    "success": True
}
```

### `POST /merchants`

Create a new Merchant

##### Request

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| name |  string |
| city | string   |
| email | string |

Payload
```
{
    "name" : "Doofu",
    "city" : "Boston",
    "email" : "doofuBos@gmail.com"
}
```

##### Response
```
{
    "merchant": {
        "city": "Boston",
        "email": "doofuBos@gmail.com",
        "id": 1,
        "name": "DoofuBoston"
    },
    "success": true
}
```

### `DELETE /merchants/<int:merchant_id>`

Delete a merchant

##### Request


Eg: `curl -X DELETE http://localhost:5000/merchants/1`

##### Response
```
{
    "success": True
}
```



### `POST /orders`

Create a new order
Authorized endpoint and will need permissions to create a new order

##### Request

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| customer_id |    integer   |
| merchant_id | integer |

```
{
    "customer_id" : 1,
    "merchant_id" : 2
}
```

Headers
```
{
    Content-Type: application/json,
    Authorization: Bearer <TOKEN>
}
```


##### Response
Eg:
```
{
    "success": true
}
```

### `GET /merchants/<int:merchant_id>/orders`

Get the orders for a particular merchant
Authorized Endpoint and will need permissions to read orders

##### Request
Eg: `curl http://localhost:5000/merchant/1`

Headers
```
{
    Content-Type: application/json,
    Authorization: Bearer <TOKEN>
}
```

##### Response
```
{
    "orders": [
        {
            "customer_city": "Austin",
            "customer_email": "doofu@gmail.com",
            "customer_id": 1,
            "customer_name": "Doofu",
            "order_id": 2
        }
    ]
}
```

### `GET /customers/<int:customer_id>/orders`

Get the orders for a particular customer
Authorized Endpoint and will need permissions to read orders

##### Request
Eg: `curl http://localhost:5000/customer/1`

Headers
```
{
    Content-Type: application/json,
    Authorization: Bearer <TOKEN>
}
```

##### Response
```
{
    "orders": [
        {
            "merchant_city": "Austin",
            "merchant_email": "doofuBoss@gmail.com",
            "merchant_id": 1,
            "merchant_name": "DoofuBoss",
            "order_id": 1
        },
        {
            "merchant_city": "Boston",
            "merchant_email": "doofuBos@gmail.com",
            "merchant_id": 2,
            "merchant_name": "DoofuActonVeryBossy",
            "order_id": 2
        }
    ]
}
```


### Errors

##### `401 - Not Authorized`

Response
```
{
    "error": 401,
    "message": "<Customer Error message>",
    "success": false
}
```


##### `400 - Bad Request`

Response
```
{
    "error": 400,
    "message": "Bad Request, please check the body and the url",
    "success": false
}
```

##### `500 - Server Error`

Response
```
{
    "success": False,
    "error": 500,
    "message": "Server Error, something went wrong"
}
```


##### `404 - Resource not found`

Response
```
{
    "error": 404,
    "message": "Resouce not Found!"
    "success": false
}
```

##### `405 - Method Not Allowed`

Response
```
{
    "success": False,
    "error": 405,
    "message": "Method not allowed. Please check documentation"
}
```


##### `422 - Unprocessable`

Response
```
{
    "success": False,
    "error": 422,
    "message": "unprocessable"
}
```
