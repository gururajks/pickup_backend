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

Run the setup.sh to get the local server running. 
Please make sure you have ran the database setup before running the setup script
```bash
chmod +x setup.sh
./setup.sh
```

## AUTH0:
Customer: "create:orders", "read:orders" 

A customer can create and read orders

AUTH0 role: pickup_customer 

Merchant: "read:orders"

A merchant can only read orders 

AUTH0 role: pickup_merchant

Authorization is required for creating and reading orders
There is no authorization required for fetching/updating/deleting customer or merchant information.  

```
CUSTOMER_TOKEN = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4ZzltZTNhR1RZZ1RwNEFVb3ktTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmR1ZGFjaXR5Z3VydS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMjRiZDhkNDRlZDgwMDE5NDY3MGIxIiwiYXVkIjoicGlja3VwYXV0aCIsImlhdCI6MTU5NDA1MDA1NCwiZXhwIjoxNTk0MTM2NDU0LCJhenAiOiJjSUVGWlpBc3dVUXRhcVdkVlpvOFpIU0pKcVg4TnF4eiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOm9yZGVycyIsInJlYWQ6b3JkZXJzIl19.Qwo8d7bGfoJg6bf1ufnx5bpUM8jZz09fi4bAZBwIvLpZ1Sg55uWgmUCDsA2LtSIl03xi_P4_3hwr3Tz8TCMSvN7gV_SN3KK0jq8323AF9PW3xp0ZRRXzyn_z-PdbmdX5mSJSRLTQLQrcOqciZmRg_SwQTqmOwreuzKlN597gKFeh26OAox17JTyZr1nZvnLe16Dpg3IKQXw87MRd4IDg0nb707B9qH6RB4KurUCpH1JySEcJB0wZAXokH4JE6UndtlXhyyFV8GrM4ePhxjIHdeEUdWRWJ5gQdoa4XYu119GHjJ2TuHg2Zno0alEZVVY0svZM2N4wt1oHmcEKDY8hZQ

MERCHANT_TOKEN = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4ZzltZTNhR1RZZ1RwNEFVb3ktTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmR1ZGFjaXR5Z3VydS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMjRiNzg5Mjg4MmMwMDEzNWQ4ZDYxIiwiYXVkIjoicGlja3VwYXV0aCIsImlhdCI6MTU5NDA1MDEyOCwiZXhwIjoxNTk0MTM2NTI4LCJhenAiOiJjSUVGWlpBc3dVUXRhcVdkVlpvOFpIU0pKcVg4TnF4eiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDpvcmRlcnMiXX0.GyQOtvmdEYxiAh8eH-jcP0EPek33ePDekc1TThd2dLtKXfU6m_lG8YdFH04bqcbGlhX041DBocWAkeD_v7Z3FvI4Ic776FfIlBP1gdR4Cxu5kNK71GrbMYmUOIH_nWOmtOaBeO6VJSB2CKM_fWe5jqESEd7WD4btmf66r3KAxjTPU9r6E_3KU4pmYbsE0vH3mnthMg6ig83F9-FKpj-9375qRZ8FC1YBJPW5UmLxyAJLw4itdqwSeC7lC1exPFBGNCt8Fd0rIgVb7aBSEBfqWGa2oCDQ5o8ZOi9BaRD8NFllVnV6Zkii4-4R42Q3fp5rR9NY-CRv2TS1jFWgllqaAg
```

`CLIENT_ID = cIEFZZAswUQtaqWdVZo8ZHSJJqX8Nqxz`

`AUTH0 Domain = fsndudacityguru.auth0.com`


## Hosted App

The pickup app is hosted in Heroku
URL: https://pickup-project.herokuapp.com/

There is a postman collection in the repo: [POSTMAN Collection](https://github.com/gururajks/pickup_backend/blob/master/Capstone%20.postman_collection.json) that is provided to try all the API endpoints.
Please make sure you add the `CUSTOMER_TOKEN` and `MERCHANT_TOKEN` as part of an environment in POSTMAN before trying it out. 


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

### `GET /`

Returns a string "Healthy!"

##### Request
Eg: `curl http://localhost:5000/`

##### Response
```
Healthy!
```

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

Permissions Required:
`create:orders`


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

Permissions required:
`read:orders`

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

Permissions required:
`read:orders`

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
