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
        orders = db.session.query(Order.id).join(Customer, Order.customer_id == Customer.id) \
            .filter(Customer.id == customer_id).all()

        return jsonify({
            "customer": customer.format(),
            "orders": [order.id for order in orders]
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
            customer = Customer.query.filter_by(id=customer_id)
            if 'name' not in body or 'city' not in body or 'email' not in body:
                raise ValueError('Bad request')
            customer.name = body['name']
            customer.email = body['email']
            customer.city = body['city']
            customer.update()
        except ValueError as e:
            abort(400)
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()

        return jsonify({
            'success': True,
            'customer': customer.format()
        })

    @app.route('/merchants/<int:merchant_id>', methods=['GET'])
    def get_merchant(merchant_id):
        merchant = Merchant.query.filter_by(id=merchant_id).one_or_none()
        orders = db.session.query(Order.id).join(Merchant, Order.merchant_id == Merchant.id) \
            .filter(Merchant.id == merchant_id).all()
        return jsonify({
            "customer": merchant.format(),
            "orders": [order.id for order in orders]
        })

    @app.route('/merchants', methods=['POST'])
    def create_merchants():
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

    @app.route('/orders', methods=['POST'])
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

    @app.route('/orders/<int:order_id>')
    def get_order(order_id):
        order = Order.query.filter_by(id=order_id).one_or_none()
        return jsonify({
            "success": True,
            "order": order.format()
        })

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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
