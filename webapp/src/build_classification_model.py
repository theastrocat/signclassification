"""
Module containing model fitting code for a web application that implements a
logistic regression on features obtained from a neural network.

When run as a module, this will load in features, train a classification
model, and then pickle the resulting model object to disk.

USE:

python build_model.py --features <pathtofeatures.npy> --labels <pathtolabels.npy> --out <pathtosave.pkl>

"""

import argparse
import cPickle as pickle
from sklearn.linear_model import LogisticRegression
import numpy as np
from cStringIO import StringIO
import requests

print "Loading labels... "
r_labels = requests.get("https://s3-us-west-2.amazonaws.com/croppedandcleanedlisaimages/train.npy")
print "Loading features..."
r_features = requests.get("https://s3-us-west-2.amazonaws.com/croppedandcleanedlisaimages/train_features.npy")
train_features = np.load(StringIO(r_features.content))
train_labels = np.load(StringIO(r_labels.content))


class ProbabiltyFinder(object):
    """
    A model for finding probabilties of what type of street sign is in an image.
    """
    def __init__(self):
        self._lr = LogisticRegression()


    def fit(self):
        print "Fitting model..."
        X = train_features
        y = train_labels[:,0]
        self._lr.fit(X,y)
        return self

    def predict_proba(self,features):
        return self._lr.predict_proba(features)

    def classes_(self):
        return self._lr.classes_


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Fit a logistic regression model and save the results.")
    parser.add_argument('--out', help='A file location to save the model.')
    args = parser.parse_args()
    pf = ProbabiltyFinder()
    pf.fit()
    print "Pickling model..."
    with open(args.out, 'w') as f:
        pickle.dump(pf, f)
