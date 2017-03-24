import os
import tensorflow as tf
import tensorflow.python.platform
from tensorflow.python.platform import gfile
import numpy as np
import json
import boto3
import argparse

"""
Method for feature extraction from numpy array files that are saved on aws.

When run as a module, this will load in arrays of image strings, pull them in
from a designated bucket, run feature extraction on them and then export the
features back to the same bucket as a numpy array.

USE:

python aws_feature_extraction --bucket <nameofbucket> --type <(train/test/full)>
"""



class FeatureExtraction(object):
    def __init__(self,bucket):
        self.s3 = boto3.resource("s3")
        self.bucket = bucket
        self.s3.meta.client.download_file(self.bucket, 'train.npy', 'train.npy')
        self.s3.meta.client.download_file(self.bucket, 'test.npy', 'test.npy')
        self.s3.meta.client.download_file(self.bucket, 'full.npy', 'full.npy')

        self.train = self.load_data('train')
        self.test = self.load_data('test')
        self.full = self.load_data('full')

    def load_data(self,typ):
        with open('{}.npy'.format(typ)) as data:
            return np.load(data)

    def extract_features(self,typ):
        img_list = self.get_list(typ)
        nb_features = 2048
        features = np.empty((len(img_list), nb_features))

        self.create_graph()

        with tf.Session() as sess:

            next_to_last_tensor = sess.graph.get_tensor_by_name('pool_3:0')

            for ind, image in enumerate(img_list):
                self.s3.meta.client.download_file(self.bucket, image, image)
                if (ind % 100 == 0):
                    print 'Processing {}th image...'.format(ind)
                    # Save periodically
                    np.save('{}_features'.format(typ), features)
                if not gfile.Exists(image):
                    tf.logging.fatal('File does not exist %s', image)

                image_data = gfile.FastGFile(image, 'rb').read()

                predictions = sess.run(next_to_last_tensor,
                                        {'DecodeJpeg/contents:0': image_data})
                features[ind, :] = np.squeeze(predictions)
                os.remove(image)
        print "Final Save: {} images processed".format(ind)
        np.save('{}_features'.format(typ), features)
        self.s3.meta.client.upload_file('{}_features.npy'.format(typ), self.bucket, '{}_features.npy'.format(typ))
        #return features

    def get_list(self,typ):
        if typ == 'train':
            return self.train[:,1]
        if typ == 'test':
            return self.test[:,1]
        if typ == 'full':
            return self.full[:,1]


    def create_graph(self):
        model_dir = 'imagenet'
        with gfile.FastGFile(os.path.join(
                model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Method for getting features out of images saved on AWS bucket')
    parser.add_argument('--bucket', help='Input bucket name with cropped images and image files')
    parser.add_argument('--type', help='Input type of features you want (train,test,full)')
    args = parser.parse_args()
    feature_extractor = FeatureExtraction(args.bucket)
    feature_extractor.extract_features(args.type)
