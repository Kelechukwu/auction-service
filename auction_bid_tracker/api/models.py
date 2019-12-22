from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.EmailField()

    def __str__(self):
        return f"{self.username}({self.email})"

class Item(models.Model):
    name = models.CharField(max_length=50)
    product_code = models.CharField(max_length=255)
    description = models.TextField(null=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}({self.product_code})"

class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_time = models.DateTimeField(auto_now_add=True)
    bid_amount =  models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
       unique_together = ["item", "user"]

    def __str__(self):
        return f"{self.item}({self.bid_amount}) @ {self.bid_time}"
