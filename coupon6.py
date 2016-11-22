#cosine
import pandas as pd
import numpy as np

import os as os

print(1)

coupon_list_train = pd.read_csv('coupon_list_train_translated2.csv')
coupon_list_test = pd.read_csv('coupon_list_test_translated2.csv')
# note that this file has some NA values for ken for user
user_list = pd.read_csv('user_list_translated.csv')
coupon_purchases_train = pd.read_csv("coupon_detail_train_translated.csv")

coupon_purchases_train["Weight"] = 1.0
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 1, "Weight"] = coupon_purchases_train["Weight"]*0.5
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 2, "Weight"] = coupon_purchases_train["Weight"]*0.5
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 3, "Weight"] = coupon_purchases_train["Weight"]*0.5
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 4, "Weight"] = coupon_purchases_train["Weight"]*0.5
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 5, "Weight"] = coupon_purchases_train["Weight"]*1.75
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 6, "Weight"] = coupon_purchases_train["Weight"]*1.75
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 7, "Weight"] = coupon_purchases_train["Weight"]*1.75
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 8, "Weight"] = coupon_purchases_train["Weight"]*0.25
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 9, "Weight"] = coupon_purchases_train["Weight"]*0.25
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 10, "Weight"] = coupon_purchases_train["Weight"]*0.25
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 11, "Weight"] = coupon_purchases_train["Weight"]*0.25
coupon_purchases_train.loc[coupon_purchases_train["I_Month"] == 12, "Weight"] = coupon_purchases_train["Weight"]*0.25


############## VISIT
purchased_coupons_train = coupon_purchases_train.merge(coupon_list_train,
                                                 on='COUPON_ID_hash',
                                                 how='inner')

### filter redundant features
features = ['GENRE_NAME', 'COUPON_ID_hash', 'USER_ID_hash','DISCOUNT_PRICE',
            'large_area_name', 'ken_name', 'small_area_name', 'Weight']

purchased_coupons_train = purchased_coupons_train[features]

# because coupon_list_test doesn't have USER_ID_hash, since there is no purchase / view file, hence nothing to merge with
### create 'dummyuser' records in order to merge training and testing sets in one
coupon_list_test['USER_ID_hash'] = 'dummyuser'

### actually a dummmy weight
coupon_list_test['Weight'] = 1.00

### filter testing set consistently with training set
coupon_list_test = coupon_list_test[features]

### merge sets together
## note that this is on axis 0, on the X axis
combined = pd.concat([purchased_coupons_train, coupon_list_test], axis=0)

print(2)

### create two new features
combined['DISCOUNT_PRICE'] = 1 / np.log10(combined['DISCOUNT_PRICE'])

### convert categoricals to OneHotEncoder form
categoricals = ['GENRE_NAME', 'large_area_name', 'ken_name', 'small_area_name']
combined_categoricals = combined[categoricals]

## this basically goes and represents everything by 1's (gives each possible value a separate column)
combined_categoricals = pd.get_dummies(combined_categoricals,
                                    dummy_na=False)

### leaving continuous features as is, obtain transformed dataset
continuous = list(set(features) - set(categoricals))
#note that this is on axis 1 !!!! the y axis
combined = pd.concat([combined[continuous], combined_categoricals], axis=1)

### remove NaN values
NAN_SUBSTITUTION_VALUE = 1
combined = combined.fillna(NAN_SUBSTITUTION_VALUE)

print(3)

### split back into training and testing sets
train = combined[combined['USER_ID_hash'] != 'dummyuser']
test = combined[combined['USER_ID_hash'] == 'dummyuser']
test.drop('USER_ID_hash', inplace=True, axis=1)

### find most appropriate coupon for every user (mean of all purchased coupons), in other words, user profile
train_dropped_coupons = train.drop('COUPON_ID_hash', axis=1)

########### VISIT
def wavg(group):
  li = list(group.columns.values)
  li.remove('USER_ID_hash')

  value_array = []

  for i in li :
    d = group[i]
    w = group['Weight']
    if w.sum() == 0 :
        d = 0
    else :
        d = (d * w).sum() / w.sum()
    value_array.append(d)

  return pd.Series(value_array, index=li)

user_profiles = train_dropped_coupons.groupby(by='USER_ID_hash').apply(wavg)

############## VISIT

FEATURE_WEIGHTS = {
    'GENRE_NAME': 2.7,
    'DISCOUNT_PRICE': 4, 
    'large_area_name': 0,
    'ken_name': 0,
    'small_area_name': 5,
    'Weight': 1
}

# dict lookup helper
def find_appropriate_weight(weights_dict, colname):
    for col, weight in weights_dict.items():
        if col in colname:
            return weight
    raise ValueError

#searches through all the columns in user_profiles.csv
W_values = [find_appropriate_weight(FEATURE_WEIGHTS, colname)
            for colname in user_profiles.columns]

#essentially puts weighted values in a diagonal
W = np.diag(W_values)

print(4)

### find weighted dot product(modified cosine similarity) between each test coupon and user profiles
test_only_features = test.drop('COUPON_ID_hash', axis=1)

for x in test_only_features.columns:
  test_only_features[x] = test_only_features[x].fillna(test_only_features[x].median())

##.T means transpose
similarity_scores = np.dot(np.dot(user_profiles, W),
                           test_only_features.T)

print(5)

### create (USED_ID)x(COUPON_ID) dataframe, similarity scores as values
coupons_ids = test['COUPON_ID_hash']
index = user_profiles.index
columns = [coupons_ids[i] for i in range(0, similarity_scores.shape[1])]
result_df = pd.DataFrame(index=index, columns=columns,
                      data=similarity_scores)

### obtain string of top10 hashes according to similarity scores for every user
def get_top10_coupon_hashes_string(row):
    row.sort()
    return ' '.join(row.index[-10:][::-1].tolist())

print(6)

output = result_df.apply(get_top10_coupon_hashes_string, axis=1)

output_df = pd.DataFrame(data={'USER_ID_hash': output.index,
                               'PURCHASED_COUPONS': output.values})
output_df_all_users = pd.merge(user_list, output_df, how='left', on='USER_ID_hash')

output_df_all_users.to_csv('FINAL_SUBMISSION.csv', header=True,
                           index=False, columns=['USER_ID_hash', 'PURCHASED_COUPONS'])

while True:
    os.system('afplay /System/Library/Sounds/Sosumi.aiff')






