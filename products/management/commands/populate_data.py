import random
from django.core.management.base import BaseCommand
from accounts.models import User
from products.models import Category, Product, Review
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with dummy data"

    def handle(self, *args, **kwargs):
        # Create categories
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                name=fake.unique.word().capitalize(),
                description=fake.text()
            )
            categories.append(category)
        
        self.stdout.write(self.style.SUCCESS("5 categories created successfully"))
        
        # Create products
        products = []
        for category in categories:
            for _ in range(10):
                product = Product.objects.create(
                    category=category,
                    name=fake.unique.word().capitalize(),
                    description=fake.text(),
                    price=round(random.uniform(10, 500), 2),
                    stock=random.randint(1, 100),
                )
                products.append(product)
        
        self.stdout.write(self.style.SUCCESS("50 products created successfully"))
        
        # Fetch some users
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("No users found! Please create some users first."))
            return
        
        # Create reviews
        for product in products:
            for _ in range(15):
                user = random.choice(users)
                Review.objects.create(
                    product=product,
                    user=user,
                    comment=fake.text(),
                )
        
        self.stdout.write(self.style.SUCCESS("750 reviews created successfully"))
