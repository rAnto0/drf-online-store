import json
from faker import Faker
from django.core.management.base import BaseCommand
from random import randint, choice
from datetime import datetime

fake = Faker()

class Command(BaseCommand):
    help = 'Generate product fixtures (JSON)'

    def handle(self, *args, **kwargs):
        categories = [
            {"model": "products.category", "pk": 1, "fields": {"name": "Electronics", "slug": "electronics", "description": "Electronic devices"}},
            {"model": "products.category", "pk": 2, "fields": {"name": "Home Appliances", "slug": "home-appliances", "description": "Appliances for home"}},
            {"model": "products.category", "pk": 3, "fields": {"name": "Books", "slug": "books", "description": "Books and novels"}},
        ]

        products = []
        product_id = 1
        now = datetime.utcnow().isoformat() + "Z"

        for i in range(50):
            category_id = choice([1, 2, 3])
            name = fake.unique.word().capitalize() + " " + fake.word().capitalize()
            description = fake.sentence()
            price = round(randint(100, 1500) + fake.random.random(), 2)
            stock = randint(10, 100)

            products.append({
                "model": "products.product",
                "pk": product_id,
                "fields": {
                    "category": category_id,
                    "name": name,
                    "description": description,
                    "price": str(price),
                    "stock": stock,
                    "created_at": now,
                    "updated_at": now
                }
            })
            product_id += 1

        data = categories + products

        with open("products/fixtures/generated_products.json", "w") as f:
            json.dump(data, f, indent=4)

        self.stdout.write(self.style.SUCCESS("✔ 50+ продуктов сгенерированы в fixtures/generated_products.json"))
