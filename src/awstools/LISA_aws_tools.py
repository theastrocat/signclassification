import numpy as np
from PIL import Image
import os
import pandas as pd
import json
import boto3


"""
Provides a method for pulling sign images out of the LISA traffic sign dataset in aws s3 bucket.
Outputs cropped images of signs to square. Unsquare images will be padded with black.


Arguments
---------

indir   :   str
            The base directory for unchanged LISA file system.

outdir  :   str
            The ouput directory for the sets of cropped images

"""


class Make_Images(object):
    def __init__(self, inbucket, outbucket):
        self.s3 = boto3.resource('s3')
        self.inbucket = inbucket
        self.outbucket = outbucket

        self.saved_images = []

        # Downloads the image dictionary for the raw images.
        self.s3.meta.client.download_file(self.inbucket, 'image_dict_full.json', 'image_dict.json')
        with open('image_dict.json') as data_file:
            self.image_dict = json.load(data_file)
        os.remove('image_dict.json')

    def crop_images(self):
        """
        Crops images in the dictionary and saves it to the specified bucket.
        """
        for im in self.image_dict.items():
            current_image = im[0]
            self.s3.meta.client.download_file(self.inbucket, current_image, current_image)
            img = Image.open(current_image)
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
            self.save_image(img4,im[1]['type'],im[0])
            if len(self.saved_images) % 1000 == 0:
                print "Cropped and saved {} images".format(len(self.saved_images))
        print "Cropped and saved {} images".format(len(self.saved_images))

    def save_image(self,image,name,d_key):
        image_str = '{}{}'.format(name, str(image.size))
        x = 0
        while image_str + str(x)in self.saved_images:
            x += 1
        image_str += str(x)
        image_str += '.jpg'
        if image.size[0] > 12:
            img4.save(image_str)
            self.s3.meta.client.upload_file(self.outbucket,image_str,image_str)
            self.image_dict[d_key]['cropped'] = image_str
        self.saved_images.append(image_str)

    def save_image_dictionary(self):
        with open('image_dict.json'), 'w') as f:
            json.dump(self.image_dict, f)
        self.s3.meta.client.upload_file(self.outbucket, 'image_dict.json', 'cropped_image_dict.json')
        print 'Saved Dictionary'
        os.remove('image_dict.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Method for parsing LISA sign data into cropped images.')
    parser.add_argument('--inbucket', help='Input bucket name with raw images')
    parser.add_argument('--outbucket', help='Output bucket name')
    args = parser.parse_args()
    image_maker = Make_Images(args.inbucket, args.outbucket)
    image_maker.crop_images()
    image_maker.save_image_dictionary()
