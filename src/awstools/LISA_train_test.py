import numpy as np
import json
import boto3
import os
import argparse
import pandas as pd
"""
Method for creating a train-test split of the availaible LISA images.

Input:
--------

bucket:
    The name of the bucket where the image dictionary is stored.

output:
    csv of of image dict keys for train and test, saved back to the bucket.
"""

class Make_Split(object):
    def __init__(self,bucket):
        self.s3 = boto3.resource("s3")
        self.bucket = bucket
        self.df = None
        self.signs_count_df = None
        self.top = None
        self.s3.meta.client.download_file(self.bucket, 'cropped_image_dict.json', 'cropped_image_dict.json')

        with open('cropped_image_dict.json') as data:
            self.image_dict = json.load(data)

        self.cropped_images = []
        for item in self.image_dict.items():
            if 'cropped' in item[1].keys():
                self.cropped_images.append([item[1]['type'],item[1]['cropped']])
        self.cropped_images = np.array(self.cropped_images)

    def build_dataframe(self):
        index = ['Row'+str(i) for i in range(1, len(self.cropped_images)+1)]
        self.df = pd.DataFrame(self.cropped_images, index=index)
        self.signs_count_df = self.df.groupby(0).agg('count')
        self.top = self.signs_count_df.sort_values(1, ascending=False).index[:15]
        self.df['gt_100'] = self.df[0].map(lambda x: self.highest_counts(x))
        self.df = self.df[self.df['gt_100'] == True].drop('gt_100', axis=1)

    def highest_counts(self, item):
        if item in self.top:
            return True
        else:
            return False

    def get_splits(self):
        first = 0
        for sign in self.df[0].unique():
            sign_type = self.df[self.df[0] == sign].values
            np.random.shuffle(sign_type)
            if first == 0:
                train, test = sign_type[:int(.8*len(sign_type))], sign_type[int(.8*len(sign_type)):]
                first += 1
            else:
                train = np.concatenate((train, sign_type[:int(.8*len(sign_type))]), axis = 0)
                test = np.concatenate((test, sign_type[int(.8*len(sign_type)):]), axis = 0)
        np.random.shuffle(train)
        np.random.shuffle(test)
        full = self.df.values
        np.random.shuffle(full)
        np.save('full',full)
        np.save('train',train)
        np.save('test',test)
        self.s3.meta.client.upload_file('full.npy',self.bucket,'full.npy')
        self.s3.meta.client.upload_file('train.npy',self.bucket,'train.npy')
        self.s3.meta.client.upload_file('test.npy',self.bucket,'test.npy')
        os.remove('full.npy')
        os.remove('train.npy')
        os.remove('test.npy')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Method for parsing LISA sign data into cropped images.')
    parser.add_argument('--bucket', help='Input bucket name with cropped images')
    args = parser.parse_args()
    split_maker = Make_Split(args.bucket)
    split_maker.build_dataframe()
    split_maker.get_splits()
