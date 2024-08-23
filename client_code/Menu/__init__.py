from ._anvil_designer import MenuTemplate
from ..ItemModello import ItemModello
from ..Cart import Cart
from anvil import *
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Menu(MenuTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.load_menu_items() # Loads menu items

    def load_menu_items(self):
        try:
            menu_items = anvil.server.call('get_menu_items') # Get menu items from server
            self.flow_panel_1.clear() # Clear those items!!!
            for item in menu_items:
                item_form = ItemModello()
                item_form.set_item(
                    name=item['Name'],
                    description=item['Description'],
                    price=item['Price'],
                    image=item['Image']
                )
                self.flow_panel_1.add_component(item_form)
        except Exception as e:
            pass

    def ViewCartButton_click(self, **event_args):
      pass

    

