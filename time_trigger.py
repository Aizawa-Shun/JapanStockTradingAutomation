import schedule
import time
import excel_reader as er

# Get trigger time from Excel
trigger_time = er.get_trigger_time()

def work():
   print(f'Executing main.py. (Execution time: {trigger_time})')
   import main
   print(f'Waiting until {trigger_time}.')

# On execution
print('Starting the time trigger.')
print(f'Waiting until {trigger_time}.')

# Execute code every day at the specified time
schedule.every().day.at(trigger_time).do(work)

while True:
   schedule.run_pending()
   time.sleep(40)