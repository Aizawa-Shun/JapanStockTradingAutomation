import datetime
import jpholiday

# Function to determine if the specified date is a business day
def is_business_day(date):
    if date.weekday() >= 5 or jpholiday.is_holiday(date):
        return False
    else:
        return True

# Function to find the next business day from the specified start date
def find_next_biz_day(start_date):
    current_date = datetime.datetime.strptime(start_date, "%Y%m%d").date()

    while not is_business_day(current_date):
        current_date += datetime.timedelta(days=1)

    return current_date.strftime("%Y%m%d")

# Function to return the next business day
def get_next_business_day():
    current_time = datetime.datetime.now(datetime.timezone.utc)      # Get current UTC time
    japan_timezone = datetime.timezone(datetime.timedelta(hours=9))  # Japan timezone
   
    current_time_jp = current_time.astimezone(japan_timezone)        # Convert UTC to Japan time
    next_biz_day = None

    if current_time_jp.time() >= datetime.time(15, 0):
      tomorrow_jp = current_time_jp + datetime.timedelta(days=1)
      tomorrow_str = tomorrow_jp.strftime("%Y%m%d")
      next_biz_day = find_next_biz_day(tomorrow_str)
      print("Next business day:", next_biz_day)
    else:
      today_str = current_time_jp.strftime("%Y%m%d")
      next_biz_day = find_next_biz_day(today_str)
      print("Next business day:", next_biz_day)
    
    return next_biz_day