import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Customer, Merchant, Order
from app import create_app


class PickupTest(unittest.TestCase):

    def setUp(self) -> None:
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        pass

    def insert_customer(self, mock_customer):
        headers = {
            "Content-Type": "application/json"
        }
        res = self.client.post('/customers', data=json.dumps(mock_customer), headers=headers)
        self.assertEqual(res.status_code, 200)
        return res.data

    def delete_customer(self, customer):
        headers = {
            "Content-Type": "application/json"
        }
        mock_customer = customer.get('customer')
        res = self.client.delete('/customers/{}'.format(mock_customer.get('id')), headers=headers)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(True, body.get('success'))

    def test_get_customer(self):
        mock_customer = {
            "name": "DoofuTest",
            "email": "DoofuBaidlu@gmail.com",
            "city": "AustinIsHot"
        }
        inserted_customer = self.insert_customer(mock_customer)
        parsed_inserted_customer = json.loads(inserted_customer)
        res = self.client.get('/customers/{}'.format(parsed_inserted_customer.get('customer').get('id')))
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data).get('customer')
        self.assertEqual(body.get('name'), mock_customer.get('name'))
        self.assertEqual(body.get('city'), mock_customer.get('city'))
        self.assertEqual(body.get('email'), mock_customer.get('email'))
        self.delete_customer(parsed_inserted_customer)

    def test_insert_delete_customer(self):
        mock_customer = {
            "name": "DoofuTest_insert_delete",
            "email": "DoofuBaidlu@gmail.com",
            "city": "AustinIsHot"
        }
        inserted_customer = self.insert_customer(mock_customer)
        parsed_inserted_customer = json.loads(inserted_customer)
        # delete the added customer
        self.delete_customer(parsed_inserted_customer)
        res = self.client.get('/customers/{}'.format(parsed_inserted_customer.get('customer').get('id')))
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
