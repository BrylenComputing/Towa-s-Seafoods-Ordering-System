import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

cart_items = [] 

def add_to_cart(item):
    cart_items.append(item) # Adds item to the cart

def remove_from_cart(item_name):
    global cart_items
    cart_items = [item for item in cart_items if item['name'] != item_name]

def get_cart_items():
    return cart_items

def calculate_subtotal():
    return sum(item['price'] * item['quantity'] for item in cart_items) # Calculates subtotal of cart items
