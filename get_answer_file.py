import pandas as pd
import numpy as np

import ml_metrics as metrics


#prediction data from previous
output_df_all_users = pd.read_csv("TRIAL.csv")
output_df_all_users["PURCHASED_COUPONS"] = output_df_all_users["PURCHASED_COUPONS"].fillna("")

#answer data
coupon_purchases_train = pd.read_csv("coupon_detail_train_translated.csv")
user_coupon_purchase = coupon_purchases_train[["USER_ID_hash", "COUPON_ID_hash"]]

answer_file = pd.DataFrame()
answer_file["USER_ID_hash"] = output_df_all_users["USER_ID_hash"]
answer_file["PURCHASED_COUPONS"] = "1st"
answer_file["PREDICTION"] = "2nd"

#sort both files by userid
user_coupon_purchase = user_coupon_purchase.sort(['USER_ID_hash'])
answer_file = answer_file.sort(['USER_ID_hash'])

user_coupon_purchase = user_coupon_purchase.reset_index()
answer_file = answer_file.reset_index()

user_coupon_purchase.drop('index', inplace=True, axis=1)
answer_file.drop('index', inplace=True, axis=1)

x = 0
count = 0

#print(user_coupon_purchase['USER_ID_hash'])
#print(answer_file['USER_ID_hash'])

print("step 1")
for i in answer_file.index:
  while x <= user_coupon_purchase.index[-1] :
    print("i and x")
    print(i, x)

    if user_coupon_purchase.values[x][0] == answer_file.values[i][0]:
      #print("user")
      #print(user_coupon_purchase.values[x][0])

      #print("coupon")
      #print(user_coupon_purchase.values[x][1])

      answer_file.values[i][1] = user_coupon_purchase.values[x][1]

      if x == user_coupon_purchase.index[-1]:
        break

      count = x + 1

      while user_coupon_purchase.values[count][0] == answer_file.values[i][0]:
        #print("coupon CONTINUE")
        #print(user_coupon_purchase.values[count][1])

        answer_file.values[i][1] = answer_file.values[i][1] + ' ' + user_coupon_purchase.values[count][1]

        #print("stored")
        #print(answer_file.values[i][1])
        count = count + 1
        x = x + 1

        if user_coupon_purchase.values[x][0] != answer_file.values[i][0]:
          break

        if count > user_coupon_purchase.index[-1]:
          break

    else:
      break
    x = x + 1

#print("fuck")
#print(answer_file.values[3][1])

answer_file.to_csv('answer_file.csv', header=True,
                       index=False, columns=['USER_ID_hash', 'PURCHASED_COUPONS'])
