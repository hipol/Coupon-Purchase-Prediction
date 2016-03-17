#add geolocation data to coupon_list_train_translated.csv and coupon_list_test_translated.csv
#follow instructions here https://pypi.python.org/pypi/geolocation-python/0.2.0
#make sure you use your own API key, and enable the GEOCODING API

import pandas as pd
import matplotlib.pyplot as plt
from numpy.random import normal
import numpy as np

# We can use the pandas library in python to read in the csv file.
# This creates a pandas dataframe and assigns it to the coupon_list_train variable.
coupon_list_train = pd.read_csv("coupon_list_train_translated2.csv")
coupon_list_test = pd.read_csv("coupon_list_test_translated2.csv")

coupon_list_train = coupon_list_train[['CAPSULE_TEXT', 'GENRE_NAME',
 'PRICE_RATE', 'CATALOG_PRICE', 'DISCOUNT_PRICE', 'DISPFROM', 'DISPEND',
 'DISPPERIOD', 'VALIDFROM', 'VALIDEND', 'VALIDPERIOD', 'USABLE_DATE_MON',
 'USABLE_DATE_TUE', 'USABLE_DATE_WED', 'USABLE_DATE_THU', 'USABLE_DATE_FRI',
 'USABLE_DATE_SAT', 'USABLE_DATE_SUN', 'USABLE_DATE_HOLIDAY',
 'USABLE_DATE_BEFORE_HOLIDAY', 'large_area_name', 'ken_name',
 'small_area_name', 'COUPON_ID_hash', 'PREF_LATITUDE', 'PREF_LONGITUDE']]

coupon_list_test = coupon_list_test[['CAPSULE_TEXT', 'GENRE_NAME',
 'PRICE_RATE', 'CATALOG_PRICE', 'DISCOUNT_PRICE', 'DISPFROM', 'DISPEND',
 'DISPPERIOD', 'VALIDFROM', 'VALIDEND', 'VALIDPERIOD', 'USABLE_DATE_MON',
 'USABLE_DATE_TUE', 'USABLE_DATE_WED', 'USABLE_DATE_THU', 'USABLE_DATE_FRI',
 'USABLE_DATE_SAT', 'USABLE_DATE_SUN', 'USABLE_DATE_HOLIDAY',
 'USABLE_DATE_BEFORE_HOLIDAY', 'large_area_name', 'ken_name',
 'small_area_name', 'COUPON_ID_hash', 'PREF_LATITUDE', 'PREF_LONGITUDE']]

from geolocation.google_maps import GoogleMaps
google_maps = GoogleMaps(api_key='')


#if Google maps can't find a small area location, go to prefecture data provided in CSV file
def getGeopoint( address ):

  location = google_maps.search(location=address) # sends search to Google Maps.
  my_location = location.first() # returns only first location.

  geopoint = [my_location.lat, my_location.lng]

  return geopoint


# Find all the unique genders -- don't know why there is a 2 .... ignore for now. but we can convert it to 1 if that yields better results
unique_small_area_name = coupon_list_train["small_area_name"].unique()
unique_small_area_name_test = coupon_list_test["small_area_name"].unique()

dictionary_of_geopoints = {}

coupon_list_train["Lat_SMALL"] = coupon_list_train["small_area_name"]
coupon_list_train["Lng_SMALL"] = coupon_list_train["small_area_name"]

coupon_list_test["Lat_SMALL"] = coupon_list_test["small_area_name"]
coupon_list_test["Lng_SMALL"] = coupon_list_test["small_area_name"]

for x in unique_small_area_name:
  geopoint = getGeopoint(x)
  dictionary_of_geopoints[x] = geopoint

for x in unique_small_area_name_test:
  geopoint = getGeopoint(x)
  dictionary_of_geopoints[x] = geopoint

i_array = ['test']
b_array_lat = [123]
b_array_lng = [123]

df = pd.DataFrame(data=dictionary_of_geopoints)
df = df.T
df = df.reset_index()

df["small_area_name"] = df['index']
df = df.drop("index", axis=1)
df["Lat_SMALL"] = df[0]
df = df.drop(0, axis=1)
df["Lng_SMALL"] = df[1]
df = df.drop(1, axis=1)
#df = pd.DataFrame([i,b[0],b[1] in dictionary_of_geopoints.items()], columns=['small_area_name', 'Lat_SMALL', "Lng_SMALL"])

coupon_list_train = pd.merge(coupon_list_train, df, on="small_area_name", how='left')
coupon_list_test = pd.merge(coupon_list_test, df, on="small_area_name", how='left')

coupon_list_train.to_csv("coupon_list_train_translated2.csv")
coupon_list_test.to_csv("coupon_list_test_translated2.csv")


####################

print("SUDSUFIOSDJFOIJSDFOISDJFOISDJFOSDIJFOSDIJFOSDIFJOSDIFJSDOIFJSDOFJSDOIFJDSOIJFOSDIFJSDOIFJSODIFJOSDIFJSDOIFJSDOIFJSDOIFJSD")
coupon_purchases_train = pd.read_csv("coupon_detail_train_translated.csv")
coupon_purchases_train = coupon_purchases_train[["SMALL_AREA_NAME", "USER_ID_hash"]]

coupon_purchases_train = coupon_purchases_train.drop_duplicates()
coupon_purchases_train = coupon_purchases_train.sort(["USER_ID_hash"])
coupon_purchases_train.to_csv("fuck.csv")

unqie = coupon_purchases_train["USER_ID_hash"].unique()
print("0")
print(unqie.shape)

print(coupon_purchases_train.head(100))

user_list = pd.read_csv('user_list_translated.csv')

print("1")
print(user_list.shape)

user_list = pd.merge(user_list, coupon_purchases_train,
                                                 on="USER_ID_hash",
                                                 how='left')

print("2")
print(user_list.shape)

user_list["SMALL_AREA_NAME"] = user_list["SMALL_AREA_NAME"].fillna("")

user_list["Lat_SMALL"] = user_list["SMALL_AREA_NAME"]
user_list["Lng_SMALL"] = user_list["SMALL_AREA_NAME"]

unique_small_area_name_user_list = user_list["SMALL_AREA_NAME"].unique()
print(unique_small_area_name_user_list)

for x in unique_small_area_name_user_list:
  geopoint = getGeopoint(x)
  dictionary_of_geopoints[x] = geopoint

df = pd.DataFrame(data=dictionary_of_geopoints)
df = df.T
df = df.reset_index()

df["SMALL_AREA_NAME"] = df['index']
df = df.drop("index", axis=1)
df["Lat_SMALL"] = df[0]
df = df.drop(0, axis=1)
df["Lng_SMALL"] = df[1]
df = df.drop(1, axis=1)
#df = pd.DataFrame([i,b[0],b[1] in dictionary_of_geopoints.items()], columns=['small_area_name', 'Lat_SMALL', "Lng_SMALL"])
print(df.head())
print(df.columns.values)


print("3")
print(user_list.shape)

user_list = pd.merge(user_list, df, on="SMALL_AREA_NAME", how='left')


print("4")
print(user_list.shape)

user_list.to_csv("user_list_translated2.csv")










