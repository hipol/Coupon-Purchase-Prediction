import pandas as pd
import numpy as np
from datetime import datetime

coupon_purchases_train = pd.read_csv("coupon_detail_train_translated.csv")

coupon_purchases_train["I_DATE"] = coupon_purchases_train["I_DATE"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
coupon_purchases_train["I_Month"] = coupon_purchases_train["I_DATE"].apply(lambda x: x.month)

coupon_purchases_train.to_csv("coupon_detail_train_translated.csv")

coupon_visit_train = pd.read_csv("coupon_visit_train.csv")

coupon_visit_train["I_DATE"] = coupon_visit_train["I_DATE"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
coupon_visit_train["I_Month"] = coupon_visit_train["I_DATE"].apply(lambda x: x.month)

coupon_visit_train.to_csv("coupon_visit_train.csv")

