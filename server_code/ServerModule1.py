import anvil.stripe
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

@anvil.server.callable
def get_menu_items(): # retrieves all items from database
    try:
        menu_items = app_tables.menuitems.search()
        menu_items_list = [
            {
                'Name': item['Name'],
                'Description': item['Description'],
                'Price': item['Price'],
                'Image': item['Image']
            }
            for item in menu_items
        ]
        return menu_items_list
    except Exception as e:
        return []

@anvil.server.callable
def add_order(charge_id, order_details): # add new row to database
    try:
        app_tables.orders.add_row(
            charge_id=charge_id,
            order=order_details
        )
    except Exception as e:
        raise Exception(f"An error occurred while adding the order: {e}")

@anvil.server.callable
def login_employee(employee_id, password): # validates login info
    employee = app_tables.employees.get(employee_id=employee_id)
    if employee and employee['password'] == password:
        return True
    return False

@anvil.server.callable
def get_orders(): # retrieves orders from database 
    orders = app_tables.orders.search()
    order_list = [{'charge_id': order['charge_id'], 'order': order['order']} for order in orders]
    return order_list

@anvil.server.callable
def delete_order(charge_id): # deletes order from database
    order_row = app_tables.orders.get(charge_id=charge_id)
    if order_row:
        order_row.delete()

@anvil.server.callable
def upload_image(image_file): # upload image and get url
    try:
        image_media = anvil.media.from_file(image_file)
        return image_media.url
    except Exception as e:
      raise Exception(f"Error uploading image: {e}")

@anvil.server.callable
def add_menu_item(name, price, description, image_url): # add new row to menu database
    try:
        app_tables.menuitems.add_row(
            Name=name,
            Price=price,
            Description=description,
            Image=image_url
        )
    except Exception as e:
        raise Exception(f"Error adding menu item: {e}")

@anvil.server.callable
def update_menu_item(item): # update item with new details
    try:
        app_tables.menuitems.get(item['id']).update(
            Name=item['Name'],
            Price=item['Price'],
            Description=item['Description'],
            Image=item['Image']
        )
    except Exception as e:
        raise Exception(f"Error updating menu item: {e}")

@anvil.server.callable
def delete_menu_item(item_name): # deletes menu item
    try:
        row = app_tables.menuitems.get(Name=item_name)
        if row:
            row.delete()
        else:
            raise Exception(f"No item found with name '{item_name}'")
            
    except Exception as e:
        raise Exception(f"Error deleting menu item: {e}")

@anvil.server.callable
def update_menu_item_name(old_name, new_name): # updates menu name
    try:
        item = app_tables.menuitems.get(Name=old_name)
        if item:
            item['Name'] = new_name
        else:
            raise Exception("Item not found")
    except Exception as e:
        raise Exception(f"Failed to update name: {e}")

@anvil.server.callable
def update_menu_item_price(item_name, new_price): # updates menu price
    try:
        item = app_tables.menuitems.get(Name=item_name)
        if item:
            item['Price'] = new_price
            return "Price updated successfully"
        else:
            return "Item not found"
    except Exception as e:
        raise Exception(f"Error updating price: {e}")

@anvil.server.callable
def update_menu_item_description(item_name, new_description): # updates menu description
    try:
        item = app_tables.menuitems.get(Name=item_name)
        if item:
            item['Description'] = new_description
            return "Description updated successfully"
        else:
            return "Item not found"
    except Exception as e:
        raise Exception(f"Error updating description: {e}")

@anvil.server.callable
def update_item_image(item, image_file): # update menu image
    try:
        item['Image'] = image_file
        return "Image updated successfully"
    except Exception as e:
        raise Exception(f"Error updating image: {e}")


