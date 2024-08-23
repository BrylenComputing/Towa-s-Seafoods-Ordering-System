from ._anvil_designer import ItemModelloTemplate
from ..AlertModello import AlertModello
from ..Cart import Cart
from anvil import *
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemModello(ItemModelloTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.MenuCartButton.set_event_handler('click', self.add_button_click)

    def set_item(self, name, description, price, image):
        self.MenuName.text = name
        self.MenuDescription.text = description
        self.MenuPrice.text = f"${price:.2f}"
        if isinstance(image, LazyMedia):
            self.MenuFoto.source = image.url 
        self.MenuFoto.width = '500px'
        self.MenuFoto.height = '500px'
        self.MenuDescription.width = 500

    def menu_cart_button_click(self, **event_args):
        pass    

    def add_button_click(self, **event_args):
      alert_form = AlertModello()
      alert_form.set_details(self.MenuName.text,
                             float(self.MenuPrice.text.replace('$', '')),
                             self.MenuFoto.source)
      alert(alert_form, large=True)

    def ViewCartButton_click(self, **event_args):
      open_form('Cart')  # Redirect to Cart

    def LoginButton_click(self, **event_args):
      open_form('EmployeeLoginPage') # Redirect to Employee Login



