from django.core.management.base import BaseCommand

from analysis import analysis as a
from products.models import Product, Review


class Command(BaseCommand):
    help = "Analyse Sentiments of Products"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        
        # Create categories
        for product in products:
            reviews = [review.comment for review in product.reviews.all()]
            result = a.yelp(reviews)

            chart, reviews, sentiments, _rating_ = result

            print("") 
            print("")
            print("")
            print("")
            print("Product : ", product.name)
            print("Reviews Count : ", len(reviews))
            print("Sentiments Count : ", len(sentiments))
            print("Rating : ", _rating_)
            print("Rating Len: ", len(_rating_))
            print("")
            print("")
            print("")
            print("")
            
            product.modelling_data = result
            product.save()

        self.stdout.write(self.style.SUCCESS("Successfully analysed reviews"))