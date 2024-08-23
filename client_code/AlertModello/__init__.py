from ._anvil_designer import AlertModelloTemplate
from ..CartItemsModule import add_to_cart
from anvil import *
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AlertModello(AlertModelloTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.ATCCartButton.set_event_handler('click', self.add_button_click)
        self.added_button.visible = False # Hides the 'added' button first.
    
    def set_details(self, name, price, image):
        self.item_name = name
        self.item_price = price
        self.item_image = image
        self.MenuName.text = name
        self.MenuPrice.text = f"${price:.2f}"
        self.MenuFoto.source = image

    def add_button_click(self, **event_args):
      quantity = int(self.QuantityBox.text or 1) # Quantity defaults to 1, if left blank
      item = {
        'name': self.item_name,
        'price': self.item_price,
        'image': self.item_image,
        'quantity': quantity
      }
      add_to_cart(item)
      self.added_button.visible = True # Shows the 'added' button now.
      alert("Item added to cart!", title="Success") # Confirmation message!
      self.raise_event('x-close-alert')
