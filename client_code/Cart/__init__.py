from ._anvil_designer import CartTemplate
from ..CartItemsModule import add_to_cart, remove_from_cart, get_cart_items, calculate_subtotal
from anvil import *
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import DatePicker
from datetime import datetime
import uuid

class Cart(CartTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.update_cart() # Updates the cart
        self.TYOrderButton.visible = False # Hides confirmation
        self.shop_button.set_event_handler('click', self.shop_button_click)
        self.ViewMenuButton.set_event_handler('click', self.ViewCartButton_click)
        self.checkout_button.set_event_handler('click', self.checkout_button_click)
        self.repeating_panel_1.set_event_handler('x-remove-item', self.handle_remove_item)
        try:
            if hasattr(self, 'pickup_time_input'):
                self.pickup_time_input.set_event_handler('change', self.validate_pickup_time)
            else:
                raise AttributeError("pickup_time_input is not defined.")
            
            if hasattr(self, 'tip_input'):
                self.tip_input.set_event_handler('change', self.update_order_summary)
            else:
                raise AttributeError("tip_input is not defined.")
        except Exception as e:
            Notification(f"Error figuring out inputs: {e}").show() # Shows error message

    def shop_button_click(self, **event_args):
        open_form('Menu') # Redirects to Menu if clicked

    def update_cart(self):
        cart_items = get_cart_items() # Gets items from cart
        if cart_items:
            self.empty_cart_panel.visible = False  # Hides empty cart panel if there are items in cart.
            self.column_panel_1.visible = True  # Shows column panel with cart items
            self.repeating_panel_1.items = [
                {'name': item['name'], 'price': item['price'], 'image': item['image'], 'quantity': item['quantity']}
                for item in cart_items
            ] # Puts cart items in repeating panel.
            self.update_order_summary() # Updates the order summary
        else:
            self.empty_cart_panel.visible = True  # Shows the empty cart panel if there are no items
            self.column_panel_1.visible = False  # Hides column panel with cart items

    def update_order_summary(self, **event_args):
        subtotal = calculate_subtotal() # Calculates subtotal of cart items
        tip_input = self.tip_input.text # Gets tip input from customer
        default_tip = 0.00 # Default tip amount
        try:
          if tip_input.strip() == "":
            tip = default_tip # Uses default tip if no tip inputted 
          else:
            tip = float(tip_input)
            if isinstance(tip, (int, float)):
                if tip < 0:
                    raise ValueError("Tip cannot be negative.")
        except ValueError:
          tip = default_tip
          self.tip_input.text = str(default_tip) 
          Notification("Tip must be a positive number. It has been reset to $0.00.").show()
        total = subtotal + tip # Calculates the total amount
        self.subtotal_label.text = f"${subtotal:.2f}" # Updates subtotal label
        self.total_label.text = f"${total:.2f}" # Updates the total label

    def handle_remove_item(self, **event_args):
        item_name = event_args['name'] # Gets the name of the item to remove
        remove_from_cart(item_name) # Removes cart item
        self.update_cart() # Updates the cart after removed item

    def ViewCartButton_click(self, **event_args):
        open_form('Menu') # Redirects to Menu

    def checkout_button_click(self, **event_args):
        order_name = self.order_name_input.text
        pickup_time = self.pickup_time_input.date
        tip = float(self.tip_input.text or "0.00")

        if not order_name.strip():
          Notification("Order Name is required to proceed with checkout.").show()
          return
       
        if not self.is_valid_pickup_time(pickup_time):
            Notification("Pickup time must be on a weekday and between 6am and 3pm.").show()
            return
        
        cart_items = get_cart_items() # Gets items from the cart
        order_details = {
            'order_name': order_name,
            'pickup_time': pickup_time.strftime('%Y-%m-%d %H:%M'), 
            'items': [{'name': item['name'], 'quantity': item['quantity'], 'price': item['price']} for item in cart_items],
            'tip': tip
        }
        
        try:
            total_amount = (calculate_subtotal() + tip) * 100
            stripe.checkout.charge(amount=total_amount, # stripe payment
                            currency="AUD",
                            title="Towa's Seafood",
                            icon_url="_/theme/Towa's%20Logo%20-%20Transparent.png")
            charge_id = str(uuid.uuid4())
            anvil.server.call('add_order', charge_id, order_details)
            self.clear_cart_items()
            self.clear_order_details()
            self.TYOrderButton.visible = True
        except Exception as e:
            Notification(f"Error during checkout: {e}").show()

    def validate_pickup_time(self, **event_args):
        pickup_time = self.pickup_time_input.date
        if not self.is_valid_pickup_time(pickup_time):
            Notification("Pickup time must be on a weekday and between 6am and 3pm.").show() # error notification
            self.pickup_time_input.date = None  

    def is_valid_pickup_time(self, pickup_time):
        if pickup_time is None:
            return False
        weekday = pickup_time.weekday()
        hour = pickup_time.hour
        return weekday < 5 and 6 <= hour < 15 

    def clear_cart_items(self):
        self.repeating_panel_1.items = []
        self.update_order_summary()

    def clear_order_details(self):
        self.order_name_input.text = ""
        self.pickup_time_input.date = None
        self.subtotal_label.text = "$0.00"
        self.total_label.text = "$0.00"
        self.tip_input.text = "0.00"
    

