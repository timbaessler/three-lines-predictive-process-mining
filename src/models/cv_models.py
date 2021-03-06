from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sys import platform

class CrossValidation:

    def __init__(self, classifier: str, param_dict: dict, cvs=3, random_state=42):
        self.classifier = classifier
        self.param_dict = param_dict
        if platform == "linux":
            self.gpu = True
        else:
            self.gpu = False
        self.random_state = random_state
        self.cvs = cvs

    def get_classifier(self):
        if self.classifier == "XGBoost":
            if self.gpu:
                clf = GridSearchCV(XGBClassifier(random_state=self.random_state,
                                             eval_metric="auc",
                                             tree_method="gpu_hist"),
                                   param_grid=self.param_dict,
                                   scoring='roc_auc',
                                   refit=True,
                                   n_jobs=-1,
                                   cv=self.cvs,
                                   verbose=10)
            else:
                clf = GridSearchCV(XGBClassifier(random_state=self.random_state,
                                                 eval_metric="auc"),
                                   param_grid=self.param_dict,
                                   scoring='roc_auc',
                                   refit=True,
                                   cv=self.cvs,
                                   verbose=10)

        elif self.classifier == "RandomForest":
            clf = GridSearchCV(RandomForestClassifier(random_state=42),
                       param_grid=self.param_dict,
                       refit=True,
                       cv=self.cvs,
                       verbose=10,
                       n_jobs=-1,
                       scoring='roc_auc')
        else:
            raise RuntimeError
        return clf