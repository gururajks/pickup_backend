import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Customer, Merchant, Order
from app import create_app

CUSTOMER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4ZzltZTNhR1RZZ1RwNEFVb3ktTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmR1ZGFjaXR5Z3VydS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMjRiZDhkNDRlZDgwMDE5NDY3MGIxIiwiYXVkIjoicGlja3VwYXV0aCIsImlhdCI6MTU5Mzk5NzM2OCwiZXhwIjoxNTk0MDgzNzY4LCJhenAiOiJjSUVGWlpBc3dVUXRhcVdkVlpvOFpIU0pKcVg4TnF4eiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOm9yZGVycyIsInJlYWQ6b3JkZXJzIl19.oCIWAOZ0FHfV_SqocXZ34TFOWjuk3zecVdyNWh640pi2vdVVYqhl-Z4R4P5LbA6J3vEW7INJ34heoUZqAzyDRsvClq05ci1iQyZbvrmLq_cw8jgwMvioPzUEt0QKnPBMT-H90KjGyvFbNwAivMrlQNSmkoo_tMKLMymApOpOKHV3QSNO9f3GxRTz6wKZX-qXybXUm0yaDEsGEzLx4OTrHEgKroWoZoP1qNw8dV7ELf1SCTbUeFqFBNvSH571Cncubibg7iu3kWelgiMKdSsZu0tKgvznje4iBINWzDovxwUbVmojCLRT7UuD62B4pCRfnDUvuOiu5VvScwdFgGwj4g"
MERCHANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4ZzltZTNhR1RZZ1RwNEFVb3ktTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmR1ZGFjaXR5Z3VydS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMjRiNzg5Mjg4MmMwMDEzNWQ4ZDYxIiwiYXVkIjoicGlja3VwYXV0aCIsImlhdCI6MTU5Mzk5NzQyOSwiZXhwIjoxNTk0MDgzODI5LCJhenAiOiJjSUVGWlpBc3dVUXRhcVdkVlpvOFpIU0pKcVg4TnF4eiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDpvcmRlcnMiXX0.qTYxUnYTdTD3S9ydWWGL1TaLwXYqZPj2LaRsWP0YRNQ9YY8J_AI3kwXiBa9Rhq7K90eIw8xbustELhK4u7Ba68UsbVI8Rmw-ycMN2kJ9UMhDZC7URZM9yTzAuyTwRPf-rQK5Lyy2FkkiQ2vR8IuvgMVw5pH1_EOFITzifY3Vsj4a8Fxp-eKFkyvb5DDbB1JhaX2W1_r1vnARzhIqZey0Y0F7Djc-MrqKn9jNvPQiwr2okAOx6NfS6TFL0WmXCiTpCRarmIFWuKqmQg9k8SSHxIPliflzNqZudtzwPb0fHgdB43wJeGs5XAHtYm_Nd5cF6Kc2tdpfDz1XfrVQoYpCoQ"


class PickupTest(unittest.TestCase):

    def setUp(self) -> None:
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.mock_customer = {
            "name": "DoofuTest",
            "email": "Doofu@gmail.com",
            "city": "AustinIsHot"
        }
        inserted_customer = self.insert_customer(self.mock_customer)
        self.parsed_inserted_customer = json.loads(inserted_customer)
        self.inserted_customer_id = self.parsed_inserted_customer.get('customer').get('id')

    def tearDown(self) -> None:
        self.delete_customer(self.parsed_inserted_customer)

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

    def create_merchant(self):
        mock_merchant = {
            "name": "DoofuBossTest",
            "email": "DoofuBoss@gmail.com",
            "city": "AustinUS"
        }
        headers = {
            "Content-Type": "application/json"
        }
        res = self.client.post('/merchants', data=json.dumps(mock_merchant), headers=headers)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        return body.get('merchant').get('id')

    def delete_merchant(self, merchant_id):
        headers = {
            "Content-Type": "application/json"
        }
        res = self.client.delete('/merchants/{}'.format(merchant_id), headers=headers)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(True, body.get('success'))

    def test_get_customer(self):
        res = self.client.get('/customers/{}'.format(self.inserted_customer_id))
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data).get('customer')
        self.assertEqual(body.get('name'), self.mock_customer.get('name'))
        self.assertEqual(body.get('city'), self.mock_customer.get('city'))
        self.assertEqual(body.get('email'), self.mock_customer.get('email'))

    def test_patched_customer(self):
        mock_customer = {
            "name": "DoofuTest_patch",
            "email": "Doofuss@gmail.com",
            "city": "AustinIsHot"
        }
        headers = {
            "Content-Type": "application/json"
        }
        res = self.client.patch('/customers/{}'.format(self.inserted_customer_id), data=json.dumps(mock_customer),
                                headers=headers)
        self.assertEqual(res.status_code, 200)
        res = self.client.get('/customers/{}'.format(self.inserted_customer_id))
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data).get('customer')
        self.assertEqual(body.get('name'), mock_customer.get('name'))
        self.assertEqual(body.get('city'), mock_customer.get('city'))
        self.assertEqual(body.get('email'), mock_customer.get('email'))

    def test_create_order(self):
        merchant_id = self.create_merchant()
        body = {
            "name": "First Order",
            "customer_id": self.inserted_customer_id,
            "merchant_id": merchant_id
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CUSTOMER_TOKEN)
        }
        res = self.client.post('/orders', data=json.dumps(body), headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), {"success": True})
        self.delete_merchant(merchant_id)

    def test_read_order(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(MERCHANT_TOKEN)
        }
        res = self.client.get('/merchants/{}/orders'.format(self.inserted_customer_id), headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), {"orders": []})

    def test_no_auth_order(self):
        headers = {
            "Content-Type": "application/json"
        }
        res = self.client.get('/merchants/{}/orders'.format(self.inserted_customer_id), headers=headers)
        self.assertEqual(res.status_code, 401)

    def test_fail_create_order(self):
        merchant_id = self.create_merchant()
        body = {
            "name": "First Order",
            "customer_id": self.inserted_customer_id,
            "merchant_id": merchant_id
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(MERCHANT_TOKEN)
        }
        res = self.client.post('/orders', data=json.dumps(body), headers=headers)
        self.assertEqual(res.status_code, 401)
        self.delete_merchant(merchant_id)


if __name__ == '__main__':
    unittest.main()
