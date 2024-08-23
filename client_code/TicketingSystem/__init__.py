from ._anvil_designer import TicketingSystemTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TicketingSystem(TicketingSystemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_orders()

  def TMenuButton_click(self, **event_args):
    open_form('Menu') # Redirects to Menu

  def load_orders(self):
    orders = anvil.server.call('get_orders') # Yoinks the orders from the server
    self.repeating_panel_1.items = orders # Displays them bad boys

  def TItemEditButton_click(self, **event_args):
    open_form('MenuEditing') # Redirects to Menu Editing
