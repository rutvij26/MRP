#!/usr/bin/env python
# coding: utf-8

# In[397]:



from pandas import DataFrame
import pandas as pd
import random
import datetime


# In[398]:


due_product_list = list()
dye_names = [ "8E","P","M","D","H"]
work_days = 5
week_start_date = datetime.datetime(2021, 8, 30)
capacity_per_day = {
"8E":288000,
"P":57600,
"M":100800,
"D":72000,
"H":86400,
}
week_days = list(
    week_start_date + datetime.timedelta(days=i) for i in range(work_days)
)
week_days


# In[399]:


def random_requirement_generator(size: int) -> dict:
    for i in range(size):
        yield {
            "part_id": i+1,
            "dye":random.choice(dye_names),
            "cust": random.choice(["Autoliv","KSS","TRW"]),
            "safety_stock":0,
            "cards":random.randint(0,5),
            "cards_quantity":random.randint(0,14401),
        }
        
requirments = list(req for req in random_requirement_generator(10000))


# In[400]:


requirements_df = pd.DataFrame.from_records(data=requirments)

requirements_df["build_quantity"] = list(
    row["cards"]*row["cards_quantity"] for index, row in requirements_df.iterrows() 
)
requirements_df["dye_capacity"] = list (
    capacity_per_day[row["dye"]]*work_days for index, row in requirements_df.iterrows()
)

total_build_quantity = requirements_df.groupby(by=requirements_df["dye"])                         .sum()                         .reset_index()                         .drop(
                            columns=["part_id","safety_stock","cards","cards_quantity","dye_capacity"]
                        ) \
                        .rename({
                            "build_quantity":"total_build_qty"
                        })


# In[401]:



total_build_quantity['capacity_per_day'] = list(capacity_per_day[row["dye"]] for index, row in total_build_quantity.iterrows())
total_build_quantity['capacity_per_week'] = list(capacity_per_day[row["dye"]]*work_days for index, row in total_build_quantity.iterrows())
total_build_quantity


# In[402]:


end = requirements_df.loc[requirements_df['dye'] == '8E']
princess = requirements_df.loc[requirements_df['dye'] == 'P']
maggie = requirements_df.loc[requirements_df['dye'] == 'M']
dyeHard = requirements_df.loc[requirements_df['dye'] == 'D']
high5 = requirements_df.loc[requirements_df['dye'] == 'H']


# In[403]:




def scheduler(df: DataFrame) -> list[dict]:
    return pd.DataFrame.from_records(data=list(record for record in date_record_generator(df)))

def dict_merger(index:int, i:int, rows:int, qty:int, skip_days:int=0) -> dict:
    return {
            "index":index,
            "Date": week_days[i] + datetime.timedelta(days=skip_days),
            "part_id" : rows["part_id"],
            "dye": rows["dye"],
            "cards": rows["cards"],
            "cards_quantity": rows["cards_quantity"],
            "build_quantity": qty
    }

def due_product_dict(index:int, i:int, rows:int, qty:int):
    return {
            "index":index,
            "part_id" : rows["part_id"],
            "dye": rows["dye"],
            "cards": rows["cards"],
            "cards_quantity": rows["cards_quantity"],
            "build_quantity": qty
    }

def date_record_generator(df: DataFrame) -> dict:
    i=0
    sum=0
    for index, rows in df.iterrows():
        if i <=len(week_days):
            sum += rows["build_quantity"]
            if sum > capacity_per_day[rows["dye"]]:
                difference = sum-capacity_per_day[rows["dye"]]
                split = rows["build_quantity"] - difference
                yield dict_merger(index, i, rows, split)
                i += 1
                sum = difference
                if i >= len(week_days):
                    # yield dict_merger(index, i-1, rows, difference, skip_days=7-work_days)
                    due_product_list.append(due_product_dict(index, i, rows, difference))
                    break
                else:
                    yield dict_merger(index, i, rows, difference)
            else:
                yield dict_merger(index, i, rows, rows["build_quantity"])
        else:
            due_product_list.append(due_product_dict(index, i, rows, rows["build_quantity"]))
            
            


# In[404]:


e_scheduled = pd.DataFrame.from_records(data=scheduler(end))
p_scheduled = pd.DataFrame.from_records(data=scheduler(princess))
m_scheduled = pd.DataFrame.from_records(data=scheduler(maggie))
d_scheduled = pd.DataFrame.from_records(data=scheduler(dyeHard))
h_scheduled = pd.DataFrame.from_records(data=scheduler(high5))


# In[ ]:




