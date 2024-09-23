import datetime
from num2words import num2words


#{num2words('day', 'ordinal_num)}
day = datetime.datetime.now().strftime('%d')


print(f"{datetime.datetime.now().strftime('%A')} the {num2words(day, 'ordinal_num')} of {datetime.datetime.now().strftime('%B')} the year of our lord {num2words(datetime.datetime.now().strftime('%C'))} {num2words(datetime.datetime.now().strftime('%y'))}")