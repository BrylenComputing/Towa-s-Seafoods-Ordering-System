from ._anvil_designer import TSModelloTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from anvil import Notification

class TSModello(TSModelloTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        try:
            if not isinstance(self.item, dict):
                raise ValueError("Item data should be a dictionary.")
            
            order_details = self.item.get('order', {}) # get order details
            # set labels with order info
            self.charge_id_label.text = f"{self.item.get('charge_id', 'N/A')}"
            self.order_name_label.text = f"{order_details.get('order_name', 'N/A')}"
            self.pickup_time_label.text = f"{order_details.get('pickup_time', 'N/A')}"
            self.items_label.text = self.format_order_items(order_details.get('items', []))
            self.tip_label.text = f"${order_details.get('tip', 0.00):.2f}"
            
        except Exception as e:
            Notification(f"Error initializing ticket details: {e}").show()
        
        self.trash_button.set_event_handler('click', self.trash_button_click)

    def format_order_items(self, order_items): # Converts list of items into a cleaner string to display
        formatted_lines = []
        for item in order_items:
            quantity = item.get('quantity', 0)
            name = item.get('name', 'Unknown')
            price = item.get('price', 0.00)
            line = f"{quantity} x {name} - ${price:.2f}"
            formatted_lines.append(line)
        return "\n".join(formatted_lines)

    def trash_button_click(self, **event_args): # Delete the order using the charge ID
        try:
            anvil.server.call('delete_order', self.item.get('charge_id', ''))
            self.remove_from_parent()
        except Exception as e:
            Notification(f"Error deleting order: {e}").show()



