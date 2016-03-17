import pandas as pd
import matplotlib.pyplot as plt
from numpy.random import normal

# We can use the pandas library in python to read in the csv file.
# This creates a pandas dataframe and assigns it to the user_list variable.
user_list = pd.read_csv("user_list_translated.csv")

# Find all the unique genders -- the column appears to contain only male and female.
print(user_list["SEX_ID"].unique())

# Replace all the occurences of male with the number 0.
user_list.loc[user_list["SEX_ID"] == "m", "SEX_ID"] = 0
user_list.loc[user_list["SEX_ID"] == "f", "SEX_ID"] = 1

user_list.to_csv("user_list_translated.csv", header=True,
                               index=False, columns=['USER_ID_hash', 'REG_DATE', 'SEX_ID', 'AGE', 'WITHDRAW_DATE', 'PREF_NAME', "PREF_LONGITUDE", "PREF_LATITUDE"])
