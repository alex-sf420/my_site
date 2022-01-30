import time, json
from datetime import datetime as dt
your_date = dt.now()
print(your_date)
data = json.dumps(time.mktime(your_date.timetuple())*1000)
print(type(your_date))
print(data)
