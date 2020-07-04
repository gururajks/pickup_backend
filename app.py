from flask import Flask, jsonify, request, abort
from models import Customer, Merchant, setup_db
from auth import requires_auth, AuthError

app = Flask(__name__)
db = setup_db(app)


@app.after_request
def after_request_response(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Authorization,Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    return response


@app.route('/customers/<int:customer_id>', methods=['GET'])
def customers(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    return jsonify({
        "customer": customer.format()
    })


@app.route('/customers', methods=['POST'])
def create_customer():
    body = request.get_json()
    try:
        customer = Customer(name=body['name'],
                            city=body['city'],
                            email=body['email'])
        customer.insert()
    except KeyError:
        abort(500)
    return jsonify({
        "success": True,
        "customer": customer.format()
    })


@app.route('/merchants/<int:merchant_id>', methods=['GET'])
def merchants(merchant_id):
    merchant = Merchant.query.filter_by(id=merchant_id).first()
    return jsonify({
        "customer": merchant.format()
    })


@app.route('/merchants', methods=['POST'])
def create_merchants():
    try:
        body = request.get_json()
        print(body)
        merchant = Merchant(name=body['name'],
                            city=body['city'],
                            email=body['email'])
        merchant.insert()
    except KeyError:
        abort(500)
    return jsonify({
        "success": True,
        "merchant": merchant.format()
    })


@app.route('/orders', methods=['POST'])
def orders():
    pass


@app.route('/')
def healthy():
    return 'Healthy!'


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request, could be a bad formed json"
    }), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "something went wrong"
    }), 500


@app.errorhandler(AuthError)
def not_authorized(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error.get('description')
    }), error.status_code


if __name__ == '__main__':
    app.run()
