#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from numpy.random import normal

# We can use the pandas library in python to read in the csv file.
# This creates a pandas dataframe and assigns it to the coupon_detail_train variable.
coupon_detail_train = pd.read_csv("coupon_detail_train.csv")

# Print the first 5 rows of the dataframe.
print("coupon_detail_train.csv : ")
print(coupon_detail_train.head(5))
print(coupon_detail_train.describe())

# We can use the pandas library in python to read in the csv file.
# This creates a pandas dataframe and assigns it to the coupon_list_train variable.
coupon_list_train = pd.read_csv("coupon_list_train.csv")

# Print the first 5 rows of the dataframe.
print("coupon_list_train.csv : ")
print(coupon_list_train.head(5))
print(coupon_list_train.describe())

# We can use the pandas library in python to read in the csv file.
# This creates a pandas dataframe and assigns it to the coupon_visit_train variable.
coupon_visit_train = pd.read_csv("coupon_visit_train.csv")

# Print the first 5 rows of the dataframe.
print("coupon_visit_train.csv : ")
print(coupon_visit_train.head(5))
print(coupon_visit_train.describe())

# We can use the pandas library in python to read in the csv file.
# This creates a pandas dataframe and assigns it to the prefecture_locations variable.
prefecture_locations = pd.read_csv("prefecture_locations.csv")

# Print the first 5 rows of the dataframe.
print("prefecture_locations.csv : ")
print(prefecture_locations.head(5))
print(prefecture_locations.describe())


# We can use the pandas library in python to read in the csv file.
# This creates a pandas dataframe and assigns it to the user_list variable.
user_list = pd.read_csv("user_list.csv")

# Print the first 5 rows of the dataframe.
print("user_list.csv : ")
print(user_list.head(5))
print(user_list.describe())




