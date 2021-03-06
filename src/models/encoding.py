import pandas as pd
from sklearn.base import TransformerMixin
import numpy as np


class Aggregation(TransformerMixin):
    def __init__(self, num_cols,  static_cat_cols, dynamic_cat_cols, one_hot_static=True,
                 case_id_col="case:concept:name", activity_col="concept:name",
                 timestamp_col="time:timestamp"):

        self.num_cols = num_cols
        self.static_cat_cols = static_cat_cols
        self.dynamic_cat_cols = dynamic_cat_cols
        self.one_hot_static = one_hot_static
        self.id = case_id_col
        self.trace = activity_col
        self.timestamp_col = timestamp_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.num_cols] = X[self.num_cols].fillna(0)
        X_num = X.groupby(self.id)[self.num_cols].agg(
            {np.mean,np.max,np.min,np.sum,np.std}).fillna(0)
        self.X_num_cols = X_num.columns.tolist()
        X_cat_dyn = pd.concat([X[self.id],
                               pd.get_dummies(X[self.dynamic_cat_cols],
                                              dummy_na=True)], axis=1)
        X_cat_dyn = X_cat_dyn.groupby(self.id).agg(np.sum)
        self.X_cat_dyn_cols = X_cat_dyn.columns.tolist()

        if self.one_hot_static:
            X_cat_stat = pd.concat([X[self.id],
                                    pd.get_dummies(X[self.static_cat_cols],
                                                   dummy_na=True)], axis=1)
            X_cat_stat = X_cat_stat.groupby(self.id).first()
        else:
            X_cat_stat = X.groupby(self.id)[self.static_cat_cols].first()
        self.X_cat_stat_cols = X_cat_stat.columns.tolist()
        y = X.groupby(self.id)['y'].first()
        X = X_num.join(X_cat_dyn).join(X_cat_stat)
        del X_cat_dyn, X_num
        self.cat_indeces = list([i for i in range(len(X.columns)-len(self.static_cat_cols), len(X.columns))])
        self.X_cols = X.columns.tolist()
        return X, y