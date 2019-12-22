from api.models import Item, User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient


def create_dummy_items(quantity=2):
    items = []
    for x in range(2):
        b = Item(name=f'item_{x}', product_code=f'QQ-{x}-{x*3}')
        b.save()
        items.append(b)
    return items

def create_dummy_users(quantity=2):
    users = []
    for x in range(2):
        b = User(username=f'user_{x}', email=f'user{x}@email.com')
        b.save()
        users.append(b)
    return users


class BidTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.items = create_dummy_items()
        self.users = create_dummy_users()

    def test_user_can_bid_for_item(self):

        bid = {'item': 1, 'user':1, 'bid_amount': 3000}
        response = self.client.post('/api/v1/bids', bid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_get_all_bids_and_winning_bid_for_an_item(self):
        item_id = 1

        # first bid
        bid_1 = {'item': item_id, 'user':1, 'bid_amount': 3000}
        response = self.client.post('/api/v1/bids', bid_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # second bid
        bid_2 = {'item': item_id, 'user':2, 'bid_amount': 4000}
        response = self.client.post('/api/v1/bids', bid_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #  get all bids
        response = self.client.get(f'/api/v1/item/{item_id}/bids')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        bids = response.json()
        self.assertEqual(len(bids), 2)

        #  get winning bid
        response = self.client.get(f'/api/v1/item/{item_id}/winner')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        winning_bid = response.json()
        self.assertEqual(float(winning_bid.get('bid_amount')), 4000.00)
    

    def test_get_all_items_a_user_has_bid(self):
        user_id = 1
        
        # first bid
        bid_1 = {'item': 1, 'user':user_id, 'bid_amount': 3000}
        response = self.client.post('/api/v1/bids', bid_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # second bid
        bid_2 = {'item': 2, 'user':user_id, 'bid_amount': 4000}
        response = self.client.post('/api/v1/bids', bid_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f'/api/v1/user/{user_id}/bids/items')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = response.json()
        self.assertEqual(len(items), 2)
    

    def test_user_cannot_bid_on_item_multiple_times(self):
        user_id = 1
        
        # first bid
        bid_1 = {'item': 1, 'user':user_id, 'bid_amount': 3000}
        response = self.client.post('/api/v1/bids', bid_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # second bid
        bid_2 = {'item': 1, 'user':user_id, 'bid_amount': 4000}
        response = self.client.post('/api/v1/bids', bid_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

