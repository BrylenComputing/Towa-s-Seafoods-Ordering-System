from ._anvil_designer import MenuModelloTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media


class MenuModello(MenuModelloTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def NameChangeButton_click(self, **event_args):
    new_name = self.NameChangeText.text.strip() # Gets new name
    
    if new_name:
        try:
            anvil.server.call('update_menu_item_name', self.item['Name'], new_name)
            self.item['Name'] = new_name # updates local name
            self.MenuName.text = new_name  # updates displayed name
            Notification("Name updated successfully!").show()
        except Exception as e:
            Notification(f"Failed to update name: {e}").show()
    else:
        Notification("Please enter a valid name.").show()

  def PriceChangeButton_click(self, **event_args):
    try:
        new_price = float(self.PriceChangeText.text) # converts new price
        anvil.server.call('update_menu_item_price', self.item['Name'], new_price)
        self.MenuPrice.text = f"${new_price:.2f}"  # updates price
        Notification("Price updated successfully!").show()
    except ValueError:
        Notification("Invalid price. Please enter a valid number.").show()
    except Exception as e:
        Notification(f"Failed to update price: {e}").show()

  def DescChangeButton_click(self, **event_args):
    try:
        new_description = self.DescChangeText.text # get new description
        
        result = anvil.server.call('update_menu_item_description', self.item['Name'], new_description) # update item description
        Notification(result).show()
        
        self.MenuDescription.text = new_description  # updates displayed description
    except Exception as e:
        Notification(f"Failed to update description: {e}").show()

  def DeleteButton_click(self, **event_args):
    try:
        item_name = self.item['Name'] # Gets item name
        anvil.server.call('delete_menu_item', item_name) # Delete item from the server
        self.remove_from_parent() # Removes item from the repeating panel
        
    except Exception as e:
        print(f"Error while deleting item: {e}")
        Notification(f"Failed to delete item: {e}").show()

  def update_item(self, item): # updates all the items
        self.MenuName.text = item['Name'] 
        self.MenuPrice.text = str(item['Price']) 
        self.MenuDescription.text = item['Description'] 
        self.MenuFoto.file = item['Image']

  def ImageChangeUploader_change(self, file, **event_args): # changes image item
    if file is not None:
        try:
            response = anvil.server.call('update_item_image', self.item, file)
            Notification(response).show()
            self.item['Image'] = file  
            self.refresh_data_bindings()  
        except Exception as e:
            Notification(f"Failed to update image: {e}").show()
    else:
        Notification("No file selected.").show()
