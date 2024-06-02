import time
import configparser

import order_manager as om
import web_scraping as ws
import excel_reader as er

# Order processing
def request_order(stock_code, order_quantity, stock_name):
      
    # Instantiate the manager to store information
    manager = om.Manager()

    # Instantiate the manager to execute login via web scraping
    login_manager = ws.LoginManager(manager.login_url, manager.headers)

    # Send login POST request
    login_manager.login()

    # Get cookies
    cookies = login_manager.get_cookies()

    # Get and set new sell URL
    new_sell_url = login_manager.get_new_sell_url()  # Get new sell URL
    manager.set_order_url(new_sell_url)              # Set new_sell_url to manager
    
    # Store the information of the stock to be traded
    manager.set_stock_infos(stock_code, order_quantity)

    # Instantiate the manager to execute order operation
    order_manager = ws.OrderManager(manager.order_url, manager.submit_params, manager.headers, cookies, stock_code, stock_name, order_quantity)
    
    # Send POST request for order information input
    order_manager.submit_order()

    # Wait
    time.sleep(5)

    # Set action_url and price to manager
    manager.set_action_url(order_manager.get_action_url_parts())
    manager.set_price(order_manager.get_price())

    # Set necessary information to the manager for order operation
    order_manager.set_order_params(manager.order_params)  # Set order_params to the manager for order operation
    order_manager.set_action_url(manager.action_url)      # Set action_url to the manager for order operation

    # Confirm order information
    order_manager.confirm_order()                         # Send POST request to confirm order
    token_id_value = order_manager.get_token_id_values()  # Get token ID

    # If token_id can be obtained
    if token_id_value is not None:
      manager.set_token_id(token_id_value)  # Set id to manager
      manager.set_commit_params()           # Set commit_params to manager
      manager.set_commit_url(order_manager.get_commit_url_parts())  # Set commit_url to manager
    else:
      return

    # Set commit_url from manager
    order_manager.set_commit_url(manager.commit_url)

    # Set commit_params to the manager for order operation
    order_manager.set_commit_params(manager.commit_params)

    # URL and header information Order confirmation and password input
    order = order_manager.commit_order()

    return order

# Stock code and order quantity for each trading stock
order_infos = er.get_order_infos()

# Initialize click counts
request_counts = {}  
for key in order_infos:
  request_counts[key] = 0

click_time = 1  # Click waiting time [s]

# Get account information from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
info = {
    'branch_number': config['login']['branch'],
    'account_number': config['login']['account'],
}
account = info['branch_number'] + ' ' + info['account_number']  # Account information

# Execute order processing
print('Starting the program.')
while True:
    # If there are no order stocks, end the program
    if len(order_infos) == 0:
      print('There are no stocks to order. Ending the program.')
      break

    # Copy dictionary keys as a list
    keys = list(order_infos.keys())
      
    # Loop the order processing for the number of stocks
    for key in keys:
      print(f'Account information {account}')

      # Order information
      ord_qty = order_infos[key]['Order_Shares']
      stock_name = order_infos[key]['Stock_Name']

      # Order processing
      order = request_order(key, ord_qty, stock_name)

      try:
        if 'Receipt No.' in order:
          print(f'[{key} {stock_name}] {ord_qty} shares {order}')  # Display stock, shares, price

          # Delete the ordered stock
          del order_infos[key]
        else:
          print(f'[{key} {stock_name}] Cannot order.')
      except TypeError:
          print(f'[{key} {stock_name}] Cannot order.')

      # Wait
      time.sleep(click_time)

      # Increment click count
      request_counts[key] += 1

      # Total: click count
      print(f'[{key} {stock_name}] Total requests: {request_counts[key]} times\n')