import numpy as np
import pandas as pd
import os as os



coupon_list_train = pd.read_csv('coupon_list_train_translated2.csv')
coupon_list_test = pd.read_csv('coupon_list_test_translated2.csv')
user_list = pd.read_csv('user_list_translated.csv')
coupon_detail_train = pd.read_csv("coupon_detail_train_translated.csv")

coupon_list_train = coupon_list_train[['COUPON_ID_hash', 'PREF_LATITUDE','PREF_LONGITUDE']]
coupon_list_test = coupon_list_test[['COUPON_ID_hash', 'PREF_LATITUDE','PREF_LONGITUDE']]
user_list = user_list[['USER_ID_hash', 'USER_lat','USER_lng']]


location_coupon_detail_train = pd.merge(coupon_detail_train, coupon_list_train, on="COUPON_ID_hash", how="inner")
location_coupon_detail_train = pd.merge(location_coupon_detail_train, user_list, on="USER_ID_hash", how="inner")

location_coupon_detail_train["USER_lat"] = location_coupon_detail_train["USER_lat"].fillna(0)
location_coupon_detail_train["USER_lng"] = location_coupon_detail_train["USER_lng"].fillna(0)

location_coupon_detail_train["Distance"] = 0

print(location_coupon_detail_train.columns.values)

from geopy.distance import vincenty
for b in location_coupon_detail_train.index :
  pointLOL = (location_coupon_detail_train.values[b][9], location_coupon_detail_train.values[b][10])
  pointLOLOL = (location_coupon_detail_train.values[b][11], location_coupon_detail_train.values[b][12])
  print(vincenty(pointLOL, pointLOLOL).miles)
  location_coupon_detail_train.values[b][13] = vincenty(pointLOL, pointLOLOL).miles

location_coupon_detail_train = location_coupon_detail_train.to_csv("coupon_detail_train_v1_location.csv")






#location_user_coupon_test = location_user_coupon_test.to_csv("location_user_coupon_test.csv")
#location_user_coupon_train = location_user_coupon_train.to_csv("location_user_coupon_train.csv")

while True:
    os.system('afplay /System/Library/Sounds/Sosumi.aiff')

