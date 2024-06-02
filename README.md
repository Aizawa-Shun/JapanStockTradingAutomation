# JapanStockTradingAutomation

This project automates the process of logging into a trading platform, retrieving stock information, and placing orders for Japanese stocks based on data from an Excel file. It ensures that orders are placed only on business days and handles all necessary parameters for trading.

## Features
- **Automated Login**: Automatically logs into the trading platform using credentials stored in a configuration file.
- **Order Placement**: Places stock orders based on the information provided in an Excel file.
- **Business Day Validation**: Ensures orders are placed only on valid business days.
- **Configurable Parameters**: Uses a configuration file to manage login credentials and trading parameters.

## Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/JapanStockTradingAutomation.git
    cd JapanStockTradingAutomation
    ```

2. **Install the required libraries**
    ```sh
    pip install -r requirements.txt
    ```

3. **Configure the `config.ini` file**

    Update the `config.ini` file with your trading credentials and parameters:
    ```ini
    [login]
    branch=Branch_Number
    account=Account_Number
    login_pass=Login_Password
    spHyojiMode=0
    syokiGamen=0
    ntt=""
    logIn.x=82
    logIn.y=22

    [trading]
    password=Trading_Password
    ```

## Usage

1. **Prepare your Excel file**

    Ensure your Excel file (`Order_Stock_List.xlsx`) is formatted correctly with columns for Stock Code, Order Shares, Stock Name, and Trigger Time.

2. **Run the automation script**

    Execute the main script to start the automation process:
    ```sh
    python main.py
    ```

## Code Overview

### main.py
Handles the overall order processing flow, including initializing managers, logging in, and placing orders based on the Excel file.

### order_manager.py
Manages the details of order placement, including setting parameters and submitting orders.

### web_scraping.py
Handles the login process and retrieving necessary URLs and cookies using web scraping techniques.

### excel_reader.py
Reads and processes the order information and trigger times from the Excel file.

### dates.py
Includes functions to determine if a date is a business day and to find the next business day.

## Dependencies
- `pandas`
- `openpyxl`
- `schedule`
- `jpholiday`

Install all dependencies using `pip install -r requirements.txt`.

## Contributing
Contributions are welcome! Please create an issue or pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.
