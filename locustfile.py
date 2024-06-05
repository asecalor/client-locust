import random

from locust import HttpUser, task, between
from faker import Faker
import json

fake = Faker()


class MyUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between each task execution
    client_data = None

    def on_start(self):
        client_data = {
            "name": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "address": fake.address()
        }
        response = self.client.post("/client", json=client_data)
        self.client_data = response.json()
        if response.status_code == 201:
            print("Client created successfully")
        try:
            self.client_data = response.json()
        except json.JSONDecodeError:
            print("Response body is not in valid JSON format")
        else:
            print(f"Failed to create client: {response.status_code}")

    @task(3)
    def get_products(self):
        products = self.client.get("/product").json()

    @task(1)
    def buy_product(self):
        random_product_id = random.randint(1, 5)
        product_request = self.client.get(f"/product/{random_product_id}")
        product = product_request.json()
        client_id = self.client_data["id"]
        provider_id = 1
        print(random_product_id)
        print(provider_id)
        body = {
                "clientId": client_id,
                "providerId": provider_id,
                "products": [
                    {
                        "productId": product["id"],
                        "quantity": random.randint(1, 5)
                    }
                ]
            }
        if product_request.status_code == 200:
            order_request = self.client.post("/order", json=body)
            order = order_request.json()
            print(order_request.status_code)


