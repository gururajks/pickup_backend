from flask import Flask, jsonify, request, abort
from models import Customer, Merchant, setup_db, Order
from auth import requires_auth, AuthError


def create_app():
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
    def get_customer(customer_id):
        customer = Customer.query.filter_by(id=customer_id).one_or_none()
        if not customer:
            abort(404)

        return jsonify({
            "customer": customer.format(),
        })

    @app.route('/customers/<int:customer_id>/orders')
    @requires_auth('read:orders')
    def get_customer_orders(customer_id):
        orders = db.session.query(Order.id,
                                  Merchant.id.label('merchant_id'),
                                  Merchant.name.label('merchant_name'),
                                  Merchant.city.label('merchant_city'),
                                  Merchant.email.label('merchant_email')) \
            .join(Merchant, Order.merchant_id == Merchant.id) \
            .join(Customer, Order.customer_id == Customer.id) \
            .filter(Customer.id == customer_id).all()
        return jsonify({
            "orders": [{
                "order_id": order.id,
                "merchant_id": order.merchant_id,
                "merchant_name": order.merchant_name,
                "merchant_city": order.merchant_city,
                "merchant_email": order.merchant_email,
            } for order in orders]
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

    @app.route('/customers/<int:customer_id>', methods=['DELETE'])
    def delete_customer(customer_id):
        try:
            customer = Customer.query.filter_by(id=customer_id).one_or_none()
            customer.delete()
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify({
            "success": True
        })

    @app.route('/customers/<int:customer_id>', methods=['PATCH'])
    def update_customer(customer_id):
        body = request.get_json()
        try:
            customer = Customer.query.filter_by(id=customer_id).one_or_none()
            if 'name' not in body or 'city' not in body or 'email' not in body:
                raise ValueError('Bad request')
            customer.name = body['name']
            customer.email = body['email']
            customer.city = body['city']
            customer.update()
        except ValueError as e:
            abort(400)
        return jsonify({
            'success': True,
            'customer': customer.format()
        })

    @app.route('/merchants/<int:merchant_id>', methods=['GET'])
    def get_merchant(merchant_id):
        merchant = Merchant.query.filter_by(id=merchant_id).one_or_none()
        return jsonify({
            "customer": merchant.format(),
        })

    @app.route('/merchants/<int:merchant_id>/orders', methods=['GET'])
    @requires_auth("read:orders")
    def get_merchant_orders(merchant_id):
        orders = db.session.query(Order.id,
                                  Customer.id.label('customer_id'),
                                  Customer.name.label('customer_name'),
                                  Customer.city.label('customer_city'),
                                  Customer.email.label('customer_email')) \
            .join(Merchant, Order.merchant_id == Merchant.id) \
            .join(Customer, Order.customer_id == Customer.id) \
            .filter(Merchant.id == merchant_id).all()
        return jsonify({
            "orders": [{
                "order_id": order.id,
                "customer_id": order.customer_id,
                "customer_name": order.customer_name,
                "customer_city": order.customer_city,
                "customer_email": order.customer_email,
            } for order in orders]
        })

    @app.route('/merchants', methods=['POST'])
    def create_merchant():
        try:
            body = request.get_json()
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

    @app.route('/merchants/<int:merchant_id>', methods=['DELETE'])
    def delete_merchant(merchant_id):
        try:
            merchant = Merchant.query.filter_by(id=merchant_id).one_or_none()
            merchant.delete()
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify({
            "success": True
        })

    '''
    Create a new order, will require permissions
    '''
    @app.route('/orders', methods=['POST'])
    @requires_auth("create:orders")
    def create_orders():
        body = request.get_json()
        try:
            if 'customer_id' not in body or 'merchant_id' not in body:
                raise ValueError('Bad Request. data incorrect')
            customer = Customer.query.filter_by(id=body['customer_id']).first()
            merchant = Merchant.query.filter_by(id=body['merchant_id']).first()
            if not customer or not merchant:
                abort(400)
            order = Order()
            order.customer = customer
            order.merchant = merchant
            order.insert()
        except (KeyError, ValueError) as e:
            abort(400)
        return jsonify({
            "success": True
        })

    @app.route('/')
    def healthy():
        return 'Healthy!'

    '''
    Errors
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request, please check the body and the url"
        }), 400

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed. Please check documentation"
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
            "message": "Resouce not Found!"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error, something went wrong"
        }), 500

    @app.errorhandler(AuthError)
    def not_authorized(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error.get('description')
        }), error.status_code

    return app


app = create_app()
if __name__ == '__main__':
    app.run()
