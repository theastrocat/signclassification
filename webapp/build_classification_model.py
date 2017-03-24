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
from src.lrprobfinder import ProbabilityFinder
from cStringIO import StringIO
import requests
import numpy as np

r_labels = requests.get("https://s3-us-west-2.amazonaws.com/croppedandcleanedlisaimages/train.npy")
r_features = requests.get("https://s3-us-west-2.amazonaws.com/croppedandcleanedlisaimages/train_features.npy")
train_features = np.load(StringIO(r_features.content))
train_labels = np.load(StringIO(r_labels.content))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Fit a logistic regression model and save the results.")
    parser.add_argument('--out', help='A file location to save the model.')
    args = parser.parse_args()
    pf = ProbabilityFinder()
    pf.fit(train_features,train_labels)
    print "Pickling model..."
    with open(args.out, 'w') as f:
        pickle.dump(pf, f)
