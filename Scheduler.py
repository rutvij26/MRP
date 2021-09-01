# INPUTS ->  Work days, Requirements (Build Quantity), Quantity per Day per Die , Safety Stock, Previous Due for a part , Cards, Card Quantity
#           Due Date, 
# Dye names -> 
# 8 End     (8E)
# Princess  (P)
# Maggie    (M)
# Dye Hard  (D)
# High 5    (H) 
# ["8E",
# "P",
# "M",
# "D",
# "H"]
import datetime
import pandas as pd
work_days = 5

capacity_per_day = {
"8E":1000,
"P":1000,
"M":1000,
"D":1000,
"H":1000,
}

requirement_for_week = {
"8E":3200,
"P":4000,
"M":400,
"D":800,
"H":1200,
}

days = [
    datetime.datetime(2021, 8, 23),
    datetime.datetime(2021, 8, 24),
    datetime.datetime(2021, 8, 25),
    datetime.datetime(2021, 8, 26),
    datetime.datetime(2021, 8, 27),
]

df = pd.DataFrame(columns=[
"8E",
"P",
"M",
"D",
"H",   
])

print(df)