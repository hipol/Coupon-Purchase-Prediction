import pandas as pd
import numpy as np

import os as os

#############

user_list = pd.read_csv('user_list_translated.csv')
pref_translation = pd.read_csv('prefecture_locations_translated.csv')

print(user_list.head())
print(user_list.describe())

print(pref_translation.columns.values)
pref_translation = pref_translation[["\xef\xbb\xbfPREF_NAME", "LATITUDE", "LONGITUDE"]]
pref_translation["PREF_NAME"] = pref_translation["\xef\xbb\xbfPREF_NAME"]
pref_translation = pref_translation.drop("\xef\xbb\xbfPREF_NAME", axis=1)

user_list = pd.merge(user_list, pref_translation,
                                                 on='PREF_NAME',
                                                 how='left')
print(user_list.describe())

user_list["PREF_LONGITUDE"] = user_list["LONGITUDE"]
user_list["PREF_LATITUDE"] = user_list["LATITUDE"]

user_list = user_list.drop("LONGITUDE", axis=1)
user_list = user_list.drop("LATITUDE", axis=1)

user_list.to_csv('user_list_translated.csv')

########

coupon_list_train = pd.read_csv("coupon_list_train_translated2.csv")
coupon_list_test = pd.read_csv("coupon_list_test_translated2.csv")

pref_translation["ken_name"] = pref_translation["PREF_NAME"]
pref_translation = pref_translation.drop("PREF_NAME", axis=1)

coupon_list_train = pd.merge(coupon_list_train, pref_translation,
                                                 on='ken_name',
                                                 how='left')
coupon_list_test = pd.merge(coupon_list_test, pref_translation,
                                                 on='ken_name',
                                                 how='left')


coupon_list_train["PREF_LONGITUDE"] = coupon_list_train["LONGITUDE"]
coupon_list_test["PREF_LATITUDE"] = coupon_list_test["LATITUDE"]
coupon_list_test["PREF_LONGITUDE"] = coupon_list_test["LONGITUDE"]
coupon_list_train["PREF_LATITUDE"] = coupon_list_train["LATITUDE"]

coupon_list_test = coupon_list_test.drop("LATITUDE", axis=1)
coupon_list_train = coupon_list_train.drop("LATITUDE", axis=1)
coupon_list_test = coupon_list_test.drop("LONGITUDE", axis=1)
coupon_list_train = coupon_list_train.drop("LONGITUDE", axis=1)

coupon_list_train.to_csv("coupon_list_train_translated2.csv")
coupon_list_test.to_csv("coupon_list_test_translated2.csv")





while True:
    os.system('afplay /System/Library/Sounds/Sosumi.aiff')
