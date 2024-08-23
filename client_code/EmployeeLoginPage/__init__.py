from ._anvil_designer import EmployeeLoginPageTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EmployeeLoginPage(EmployeeLoginPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def ELoginButton_click(self, **event_args):
    employee_id = self.EIDText.text
    password = self.EPasswordText.text
    try:
        if anvil.server.call('login_employee', employee_id, password):
            Notification("Login successful!").show() # Success Notification
            open_form('TicketingSystem')  # Redirects to Ticketing System
        else:
            Notification("Invalid Employee ID or Password!").show() # Error Notification
    except Exception as e:
        Notification(f"An error occurred: {e}").show() # Error Notification 2.0

  def LMenuButton_click(self, **event_args):
    open_form('Menu') # Redirects to Menu

  def EViewCartButton_click(self, **event_args):
    open_form('Cart') # Redirects to Cart
    

