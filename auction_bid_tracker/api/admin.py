from django.contrib import admin
from .models import Bid, Item, User

admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(User)