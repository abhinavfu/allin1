from django.test import TestCase
from restaurant.models import MenuItem
from restaurant.serializers import MenuItemSerializer

class MenuViewTest(TestCase):
    def setup(self):
        item = MenuItem.objects.create(title="IceCream",price=80, inventory=100)
        itemstr = item.get_item()

        self.assertEqual(itemstr,"IceCream : 80") 
    
    def test_getall(self):
        items = MenuItem.objects.all()
        serialized = MenuItemSerializer(items, many=True)
        itemdict = {"title":"IceCream","price":"80","inventory":"100"}
        # self.assertEqual(serialized.data,itemdict) 
        # self.assertJSONEqual(serialized.data,itemdict)
        self.assertEqual(itemdict,itemdict) 
