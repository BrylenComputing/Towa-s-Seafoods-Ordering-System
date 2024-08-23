from ._anvil_designer import MenuEditingTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media

class MenuEditing(MenuEditingTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.update_menu_items() # Updates list of menu items
    
  def update_menu_items(self):
      try:
        menu_items = anvil.server.call('get_menu_items')
        self.repeating_panel_1.items = [
            {
                'Name': item['Name'],
                'Price': item['Price'],
                'Description': item['Description'],
                'Image': item['Image']
            }
            for item in menu_items
        ]
      except Exception as e:
        Notification(f"Error fetching menu items: {e}").show()

  def NewItemButton_click(self, **event_args):
    name = self.NewNameText.text
    price = float(self.NewPriceText.text) if self.NewPriceText.text else 0.0
    description = self.NewDescriptionText.text
    image_file = self.NewImageUpload.file

    if not name or not description or not image_file: # Checks for empty fields
        Notification("Please fill in all fields and upload an image.").show()
        return

    try:
        response = anvil.server.call('add_menu_item', name, price, description, image_file)
        Notification(response).show()

        self.NewNameText.text = ""
        self.NewPriceText.text = ""
        self.NewDescriptionText.text = ""

        open_form('MenuEditing')  
    except Exception as e:
        Notification(f"Failed to add item: {e}").show()

  def MMenuButton_click(self, **event_args):
    open_form('Menu') # Redirect to Menu

  def MTSButton_click(self, **event_args):
    open_form('TicketingSystem') # Redirect to Ticketing System





