from ._anvil_designer import RPModelloTemplate
from ...CartItemsModule import add_to_cart, remove_from_cart, get_cart_items, calculate_subtotal
from anvil import *
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RPModello(RPModelloTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.delete_button.set_event_handler('click', self.delete_button_click)

  def set_item(self, name, price, image, quantity):
        self.MenuName.text = name
        self.MenuPrice.text = f"${price:.2f}"
        self.MenuFoto.source = image
        self.label_3.text = f"Quantity: {quantity}"

  def delete_button_click(self, **event_args):
        item_name = self.MenuName.text  # Get item name to be removed
        remove_from_cart(item_name)
        self.remove_from_parent()
        get_open_form().update_order_summary()
