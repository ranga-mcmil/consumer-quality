import random
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from accounts.models import User
from products.models import Category, Product, Review
from faker import Faker

fake = Faker()

# Tech-focused categories
CATEGORIES = [
    "Smartphones", "Laptops", "Audio & Accessories", "Gaming", "Wearables"
]

# Tech-focused product names per category
PRODUCTS = {
    "Smartphones": ["iPhone 14", "Samsung Galaxy S23", "Google Pixel 7", "OnePlus 11", "Xiaomi Mi 13"],
    "Laptops": ["MacBook Pro", "Dell XPS 15", "Razer Blade 16", "Lenovo ThinkPad X1", "Asus ROG Zephyrus"],
    "Audio & Accessories": ["Sony WH-1000XM5", "AirPods Pro", "Bose QuietComfort 45", "JBL Charge 5", "Logitech MX Master 3"],
    "Gaming": ["PlayStation 5", "Xbox Series X", "Nintendo Switch OLED", "Alienware Aurora R15", "Steam Deck"],
    "Wearables": ["Apple Watch Ultra", "Samsung Galaxy Watch 5", "Garmin Fenix 7", "Fitbit Charge 6", "Oura Ring Gen3"]
}

# Sample reviews
GOOD_REVIEWS = [
    "Amazing product! Works perfectly and exceeded my expectations.",
    "Highly recommended! The performance is outstanding.",
    "Very satisfied with my purchase. Great value for money.",
    "Top-notch quality! Will definitely buy from here again.",
    "Incredible battery life and features. Best in the market!"
]

MODERATE_REVIEWS = [
    "It's decent but has some minor issues.",
    "Works fine but not as great as advertised.",
    "Good, but I feel like there are better alternatives.",
    "Gets the job done but could be improved.",
    "It's okay. Nothing special, but not terrible."
]

BAD_REVIEWS = [
    "Terrible experience. Overpriced and underwhelming.",
    "Not worth the price. Wouldn’t buy again.",
    "Broke after a few days of use. Really disappointed.",
    "Worst purchase ever. Poor performance and quality.",
    "Battery life is awful, and customer support is useless."
]

class Command(BaseCommand):
    help = "Populate the database with tech-focused dummy data"

    def handle(self, *args, **kwargs):
        # Create categories
        categories = {}
        for cat_name in CATEGORIES:
            category, _ = Category.objects.get_or_create(
                name=cat_name, defaults={"description": f"Latest and best {cat_name.lower()} in the market."}
            )
            categories[cat_name] = category
        
        self.stdout.write(self.style.SUCCESS(f"{len(CATEGORIES)} tech categories created successfully"))

        # Create products
        products = []
        image_path = os.path.join(os.path.dirname(__file__), "product_image.png")
        
        for category_name, product_names in PRODUCTS.items():
            category = categories[category_name]
            for product_name in product_names:
                product = Product.objects.create(
                    category=category,
                    name=product_name,
                    description=f"Premium {product_name} with cutting-edge technology and design.",
                    price=round(random.uniform(300, 3000), 2),
                    stock=random.randint(5, 50),
                )
                if os.path.exists(image_path):
                    with open(image_path, "rb") as img_file:
                        product.image.save(f"{product_name.lower().replace(' ', '_')}.png", File(img_file), save=True)
                
                products.append(product)
        
        self.stdout.write(self.style.SUCCESS(f"{len(products)} tech products created successfully"))

        # Fetch or create users
        users = list(User.objects.all())
        if not users:
            users = []
            for _ in range(20):  # Creating 20 users
                user = User.objects.create_user(
                    email=fake.unique.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    password="password123"  # Default password for testing
                )
                users.append(user)
            self.stdout.write(self.style.SUCCESS("20 test users created successfully"))

        # Create reviews with varying distributions
        for product in products:
            num_reviews = random.randint(5, 15)
            review_distribution = random.choice(["all_positive", "all_negative", "balanced", "more_negative"])

            for _ in range(num_reviews):
                if review_distribution == "all_positive":
                    review_type = GOOD_REVIEWS
                elif review_distribution == "all_negative":
                    review_type = BAD_REVIEWS
                elif review_distribution == "balanced":
                    review_type = random.choices(
                        [GOOD_REVIEWS, MODERATE_REVIEWS, BAD_REVIEWS], weights=[33, 34, 33], k=1
                    )[0]
                else:  # more_negative
                    review_type = random.choices(
                        [GOOD_REVIEWS, MODERATE_REVIEWS, BAD_REVIEWS], weights=[20, 30, 50], k=1
                    )[0]

                comment = random.choice(review_type)
                Review.objects.create(
                    product=product,
                    reviewer=f'{fake.first_name()} {fake.last_name()}',
                    comment=comment,
                    email=fake.unique.email()
                )

        self.stdout.write(self.style.SUCCESS("Reviews added with varied distributions successfully"))