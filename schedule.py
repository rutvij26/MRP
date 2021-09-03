#!/usr/bin/env python
# coding: utf-8

# In[15]:


from pandas import DataFrame
import pandas as pd
import random
import datetime


# In[16]:


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


# In[17]:



class Dummy_Requirement_spawner():
    
    def __init__(self, size) -> None:
        self.size = size
        self.requirements_df = self.dataframe_generate()
    
    def __random_requirement_generator(self) -> dict:
        for i in range(self.size):
            yield {
                "part_id": i+1,
                "dye":random.choice(dye_names),
                "cust": random.choice(["Autoliv","KSS","TRW"]),
                "safety_stock":0,
                "cards":random.randint(0,5),
                "cards_quantity":random.randint(0,14401),
            }
            
    def dataframe_generate(self):
        requirments = list(req for req in self.__random_requirement_generator())
        
        self.requirements_df = pd.DataFrame.from_records(data=requirments)

        self.requirements_df["build_quantity"] = list(
            row["cards"]*row["cards_quantity"] for index, row in self.requirements_df.iterrows() 
        )
        self.requirements_df["dye_capacity"] = list (
            capacity_per_day[row["dye"]]*work_days for index, row in self.requirements_df.iterrows()
        )
        return self.requirements_df
    
    def total_build_quantity(self):
        return self.requirements_df.groupby(by=self.requirements_df["dye"])                         .sum()                         .reset_index()                         .drop(
                            columns=["part_id","safety_stock","cards","cards_quantity","dye_capacity"]
                        ) \
                        .rename({
                            "build_quantity":"total_build_qty"
                        })
                        
    def dataframe_filter_dye(self,dye: str)-> DataFrame:
        return self.requirements_df.loc[self.requirements_df['dye'] == dye]
        
        
    
    


# In[18]:


requirements = Dummy_Requirement_spawner(size = 150)
end = requirements.dataframe_filter_dye('8E')
princess = requirements.dataframe_filter_dye('P')
maggie = requirements.dataframe_filter_dye('M')
dyeHard = requirements.dataframe_filter_dye('D')
high5 = requirements.dataframe_filter_dye('H')     


# In[19]:




class Production_Schedule():
    
    def __init__(self, df: DataFrame) -> None:
        self.df = df
    
    
    def __scheduler(self) -> list[dict]:
        return pd.DataFrame.from_records(data=list(record for record in self.__date_record_generator()))
    
    
    def __dict_merger(self,index:int, i:int, rows:int, qty:int, skip_days:int=0) -> dict:
        return {
                "index":index,
                "Date": week_days[i] + datetime.timedelta(days=skip_days),
                "part_id" : rows["part_id"],
                "dye": rows["dye"],
                "cards": rows["cards"],
                "cards_quantity": rows["cards_quantity"],
                "build_quantity": qty
        }
    
    
    def __due_product_dict(self,index:int, rows:int, qty:int) -> dict:
        return {
                "index":index,
                "part_id" : rows["part_id"],
                "dye": rows["dye"],
                "cards": rows["cards"],
                "cards_quantity": rows["cards_quantity"],
                "build_quantity": qty
        }
    
    
    def __date_record_generator(self) -> dict:
        i=0
        sum=0
        for index, rows in self.df.iterrows():
            if i <len(week_days):
                sum += rows["build_quantity"]
                if sum > capacity_per_day[rows["dye"]]:
                    difference = sum-capacity_per_day[rows["dye"]]
                    split = rows["build_quantity"] - difference
                    yield self.__dict_merger(index, i, rows, split)
                    i += 1
                    sum = difference
                    if i >= len(week_days):
                        due_product_list.append(self.__due_product_dict(index, rows, difference))
                    else:
                        yield self.__dict_merger(index, i, rows, difference)
                elif i < len(week_days):
                    yield self.__dict_merger(index, i, rows, rows["build_quantity"])
                
                else:
                    due_product_list.append(self.__due_product_dict(index, rows, difference))
            else:
                due_product_list.append(self.__due_product_dict(index, rows, rows["build_quantity"]))
    
                
    def csv_generation(self, csv_name):
        pd.DataFrame.from_records(data=self.__scheduler()).to_csv(csv_name + '.csv')
    
    
    def dataframe_generation(self) -> DataFrame:
        return pd.DataFrame.from_records(data=self.__scheduler())
    
    
    def records_generation(self) -> list[str]:
        return self.__scheduler()
                
            


# In[20]:


e =  Production_Schedule(end)
p =  Production_Schedule(princess)
m =  Production_Schedule(maggie)
d =  Production_Schedule(dyeHard)
h =  Production_Schedule(high5)


# In[21]:


e.csv_generation('./8End')
p.csv_generation('./Princess')
m.csv_generation('./Maggie')
d.csv_generation('./DyeHard')
h.csv_generation('./High5')
pd.DataFrame.from_records(data=due_product_list).to_csv('./Due_products.csv')


# In[22]:


end


# In[ ]:




