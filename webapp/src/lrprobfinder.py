from sklearn.linear_model import LogisticRegression
import numpy as np

class ProbabilityFinder(object):
    """
    A model for finding probabilties of what type of street sign is in an image.
    """
    def __init__(self):
        self._lr = LogisticRegression()

    def fit(self,X,y):
        print "Fitting model..."
        y = y[:,0]
        self._lr.fit(X,y)
        return self

    def predict_proba(self,features):
        return self._lr.predict_proba(features)

    def classes_(self):
        return self._lr.classes_
