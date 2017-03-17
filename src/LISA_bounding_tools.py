import numpy as np
from PIL import Image
import argparse
import os
import pandas as pd
import json


"""
Provides a method for pulling sign images out of the LISA traffic sign dataset.
Outputs cropped images of signs to square. Unsquare images will be padded with black.


Arguments
---------

indir   :   str
            The base directory for unchanged LISA file system.

outdir  :   str
            The ouput directory for the sets of cropped images

"""


class Make_Images(object):
    def __init__(self, indir = os.getcwd(), outdir = os.getcwd()):
        self.inder = indir
        self.outdir = outdir

        self.image_dict = {}
        self.saved_images = []
        self.sub_dirs = []
        for directory in os.listdir(self.inder):
            cnt_dir = os.path.join(self.inder,directory)
            if os.path.splitext(cnt_dir)[1] == '' and directory[0] != '.':
                self.sub_dirs.append(cnt_dir)

        self.image_dirs = []
        for directory in self.sub_dirs:
            for subdir in os.listdir(directory):
                if subdir[0] == 'f':
                    self.image_dirs.append(os.path.join(self.inder,directory,subdir))


        self.build_image_dict()
        self.make_dir('')
        with open(os.path.join(self.outdir, 'image_dict.json'), 'w') as f:
            json.dump(self.image_dict, f)

    def make_dir(self,directory):
        """
        Creates the output directory.
        """
        if not os.path.exists(os.path.join(self.outdir,directory)):
            os.makedirs(os.path.join(self.outdir,directory))
            print "Creating path: " + os.path.join(self.outdir,directory)

    def build_image_dict(self):
        """
        Pulls an image in with PIL and
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

    def crop_images(self):
        """
        Crops image
        """
        for im in self.image_dict.items():
            img = Image.open(im[1]['path'])
            img2 = img.crop(tuple(im[1]['bounds']))
            longer_side = max(img2.size)
            horizontal_padding = (longer_side - img2.size[0]) / 2
            vertical_padding = (longer_side - img2.size[1]) / 2
            img3 = img2.crop(
            (
                -horizontal_padding,
                -vertical_padding,
                img2.size[0] + horizontal_padding,
                img2.size[1] + vertical_padding
            )
            )
            if img3.size[0] > img3.size[1]:
                img4 = img3.crop((0,0,img3.size[1],img3.size[1]))
            elif img3.size[0] < img3.size[1]:
                img4 = img3.crop((0,0,img3.size[0],img3.size[0]))
            else:
                img4 = img3
            image_str = '{}{}'.format(im[1]['type'], str(img4.size))
            x = 0
            while image_str + str(x)in self.saved_images:
                x += 1
            image_str += str(x)
            self.make_dir(im[1]['type'])
            img4.save(os.path.join(self.outdir,im[1]['type'], "{}.jpg".format(image_str)))
            self.image_dict[im[0]]['cropped'] = image_str
            self.saved_images.append(image_str)
            if len(self.saved_images) % 1000 == 0:
                print "Cropped and saved {} images".format(len(self.saved_images))
        print "Cropped and saved {} images".format(len(self.saved_images))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Method for parsing LISA sign data into cropped images.')
    parser.add_argument('--indir', help='Directory ')
    parser.add_argument('--outdir', help='A file to save the pickled model object to.')
    args = parser.parse_args()
    image_maker = Make_Images(args.indir, args.outdir)
    image_maker.crop_images()
