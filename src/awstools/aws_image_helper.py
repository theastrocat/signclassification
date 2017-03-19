import numpy as np
from PIL import Image
import os
import pandas as pd
import json
import boto3
import argparse


"""
Provides a method for moving all LISA traffic images out of a file system and into an s3 bucket.


Arguments
---------

indir   :   str
            The base directory for unchanged LISA file system.

outdir  :   str
            The output bucket name

"""


class Move_Images(object):
    def __init__(self, indir, outdir):
        self.s3 = boto3.resource('s3')
        self.bucket = outdir
        self.indir = indir

        self.image_dict = {}

        self.sub_dirs = []
        for directory in os.listdir(self.indir):
            cnt_dir = os.path.join(self.indir,directory)
            if os.path.splitext(cnt_dir)[1] == '' and directory[0] != '.':
                self.sub_dirs.append(cnt_dir)

        self.image_dirs = []
        for directory in self.sub_dirs:
            for subdir in os.listdir(directory):
                if subdir[0] == 'f':
                    self.image_dirs.append(os.path.join(self.indir,directory,subdir))

        self.build_image_dict()
        self.save_images()
        self.save_image_dictionary()

    def save_images(self):
        """
        Saves the images to the bucket.
        """
        x = 1
        for image in self.image_dict.items():
            self.s3.meta.client.upload_file(image[1]['path'], self.bucket,image[0])
            print "Upload {} image(s).".format(x)
            x += 1

    def build_image_dict(self):
        """
        Pulls builds a directory of images and the bounding boxes.
        """
        print "Building image dictionary"
        for directory in self.image_dirs:
            images = [x for x in os.listdir(directory) if x[-4:] == '.png']
            for image in images:
                self.image_dict[image] = {}
                self.image_dict[image]['path'] = os.path.join(directory,image)
            image_annot = pd.read_csv(os.path.join(directory,'frameAnnotations.csv'), delimiter=';')
            for row in range(len(image_annot)):
                self.image_dict[image_annot.loc[row][0]]['bounds'] = [float(x) for x in str(image_annot.loc[row][2:6]).split() if x.isdigit()]
                self.image_dict[image_annot.loc[row][0]]['type'] = image_annot.loc[row][1]

    def save_image_dictionary(self):
        with open('image_dict_full.json', 'w') as f:
            json.dump(self.image_dict, f)
        self.s3.meta.client.upload_file('image_dict_full.json' self.bucket, 'image_dict_full.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Moves images to s3 bucket.')
    parser.add_argument('--indir', help='Input directory ')
    parser.add_argument('--bucket', help='Output to bucket')
    args = parser.parse_args()
    image_maker = Move_Images(args.indir, args.bucket)
