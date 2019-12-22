from api.models import Bid, Item, User
from .serializers import BidSerializer, ItemSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from django.db.models import Max


def get_item(id):
    """
     Args:
       id: the unique identifier of an item.
     Returns: 
       Item object or raises Http404
    """
    try:
        return Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404

def get_user(user_id):
    """
     Args:
       id: the unique identifier of a User.
     Returns: 
       User object or raises Http404
    """
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

class BidView(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class ItemView(viewsets.ModelViewSet):
    """
        Retrieve all available items
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class WinningBid(APIView):
    """
    Retrieve current winning bid for an item.
    GET item/<item_id>/winner
    """

    def get(self, request, pk, format=None):
        item = get_item(pk)
        max_bid = Bid.objects.filter(item=item.id).aggregate(Max('bid_amount'))
        winning_bid= Bid.objects.filter(bid_amount=max_bid["bid_amount__max"]).order_by('bid_time')[0]

        serializer = BidSerializer(winning_bid)
        winning_bid = serializer.data

        winning_user = get_user(winning_bid.get("user"))
        winning_bid["user"] = UserSerializer(winning_user).data
        return Response(winning_bid)


class ItemBids(APIView):
    """
    Retrieve all the bids for an item;
    GET item/<item_id>/bids
    """

    def get(self, request, pk, format=None):
        item = get_item(pk)
        bids = Bid.objects.filter(item=item.id)

        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

class UserItemsBids(APIView):
    """
    Retrieve all the items on which a user has bid;
    GET user/<user_id>/bids/items
    """

    def get(self, request, pk, format=None):
        # check if the user exists
        user = get_user(pk) 

        items_id_dict = Bid.objects.filter(user=user.id).values('item_id')
        item_ids = [val['item_id'] for val in items_id_dict]

        item_objects = Item.objects.filter(pk__in=item_ids)
        serializer = ItemSerializer(item_objects, many=True)
        return Response(serializer.data)