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
Eg: `curl http://localhost:3000/customers/1`

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

### `GET /questions`
Gets all the questions that are available and is paginated. It is restricted to 10 questions per page
Use page parameter for the page
##### Request

Parameters: `page`

Eg: `curl -v http://localhost:3000/questions?page=1`

##### Response
```
{
    "categories": [
        {
        "id": 1,
        "type": "Science"
        }
    ],
    "current_category": "Sports",
    "questions": [
        {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```


### `DELETE /questions/<int:question_id>`

Delete a specific question given its question id

##### Request

Eg: `curl -X DELETE http://localhost:3000/questions`

##### Response
```
{
    "message": "Deleted"
    "success": True
}
```

### `POST /questions`

Create a new question with the given details as part of the body
##### Request

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| answer |  string |
| category |    integer   |
| difficulty | integer |
| question | string |

```
{
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
}
```

##### Response
Eg:
```
{
    "id": 1,
    "message" : "Added",
    "success": True
}
```

### `POST /search`

It searches and displays all the questions that have a substring equal to the given string
##### Request

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| searchTerm |  string |

```
{
    "searchTerm" : "country"
}
```

##### Response
Eg:
```
{
  "current_category": "Sports", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }
  ], 
  "total_questions": 1
}

```
Errors:
400 for bad request


### `GET /categories/<int:category_id>/questions`
Get all the questions for a particular category
##### Request

Eg: `curl http://localhost:3000/categories/1/questions`

##### Response
```
{
  "currentCategory": 1, 
  "questions": [
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "totalQuestions": 1
}

```

### `POST /quizzes`

This is the trivia quiz which gives the next question for a particular category. The next question is randomized and does not repeat. 
##### Request

Provide the previous question id so that we know which questions were asked and they are not repeated. 
`quiz_category` is a category object. 

Required Fields:
| Fields   |      Type      |
|----------|:-------------:|
| previous_questions |  List |
| quiz_category |  object |
```
{
    "previous_questions":[],
    "quiz_category":{
        "type":"Science",
        "id":1
    }
}
```

##### Response
Eg:
```
{
    "question": {
        "answer": "Mona Lisa", 
        "category": 2, 
        "difficulty": 3, 
        "id": 17, 
        "question": "La Giaconda is better known as what?"
  }
}
``` 


### Errors

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
    "message": "Server Error"
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
