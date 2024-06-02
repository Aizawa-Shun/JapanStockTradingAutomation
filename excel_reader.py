import pandas as pd

# Read order information from Excel
def get_order_infos():
    # Set the path to the Excel file
    file_path = 'Order_Stock_List.xlsx'

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Get data from each column until a blank is encountered
    data_until_blank = {}
    for col in df.columns:
        data_until_blank[col] = df[col].dropna().tolist()
    
    # Store order data  
    order_infos = {}
    for i in range(len(data_until_blank['Stock_Code'])):
        order_infos[data_until_blank['Stock_Code'][i]] = {
            'Order_Shares': data_until_blank['Order_Shares'][i],
            'Stock_Name': data_until_blank['Stock_Name'][i]
        }
    
    return order_infos

def get_trigger_time():
    # Set the path to the Excel file
    file_path = 'Order_Stock_List.xlsx'

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Get data from each column until a blank is encountered
    data_until_blank = {}
    for col in df.columns:
        data_until_blank[col] = df[col].dropna().tolist()

    # Get the trigger time
    trigger_time = data_until_blank['Trigger_Time'][0].strftime('%H:%M')

    return trigger_time