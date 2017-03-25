import numpy as np
import requests
from cStringIO import StringIO

"""
Module for getting a random image and its features from the test set to post
to the website.
"""

baseurl = "https://s3-us-west-2.amazonaws.com/croppedandcleanedlisaimages/"

r_labels = requests.get("{}test.npy".format(baseurl))
r_features = requests.get("{}test_features.npy".format(baseurl))


class RandImage(object):
    def __init__(self):
        self.test_features = np.load(StringIO(r_features.content))
        self.test_paths = np.load(StringIO(r_labels.content))
        self.test_set = np.concatenate((self.test_features, self.test_paths[:,1].reshape(-1,1)), axis = 1)
        self.getrandomimage()
    def getrandomimage(self):
        current_index = np.random.choice(range(len(self.test_set)))
        self.current_image = baseurl + self.test_set[current_index][-1]
        self.current_label = self.test_paths[current_index,-2]
        return self.current_image, current_index
    def getimagefeatures(self, indx):
        return self.test_set[indx][:-1]
