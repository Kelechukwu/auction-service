from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bids', views.BidView)
router.register(r'items', views.ItemView)
router.register(r'users', views.UserView)


urlpatterns = [
    path('', include(router.urls)),
    path('item/<int:pk>/winner', views.WinningBid.as_view()),
    path('item/<int:pk>/bids', views.ItemBids.as_view()),
    path('user/<int:pk>/bids/items', views.UserItemsBids.as_view()),
]