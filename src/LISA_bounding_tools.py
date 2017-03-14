import numpy as np
from PIL import Image
import argparse
import os
import pandas as pd


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
    def __init__(self, inder, outdir):
        self.inder = inder
        self.outdir = outdir
        self.annot = 'frameAnnotations.csv'
        self.image_dirs = [str(x) for x in os.listdir(self.inder) if x[-1].isdigit()]
        self.image_paths = []
        self.image_paths = []
        for direct in self.image_dirs:
            for subdir in os.listdir(self.inder+direct):
                if subdir[0].isalpha():
                    self.image_paths.append(self.inder+direct+'/'+subdir+'/')
        def main_call(self):
            """
            Main loop for standard run of the code.
            """
            for i in range(len(self.image_paths)):
                self.make_out_dir(i)

                print "Finished set: {}".format(i)
        def mak_out_dir(self,index):
            """
            Creates the output directory.
            """
            pass

        def get_image(self,index):
            """
            Pulls an image in with PIL
            """
            pass

        def crop_images(self,index):
            """
            Crops image
            """
            pass

        def write_images(self,image,index):
            pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Method for parsing LISA sign data into cropped images.')
    parser.add_argument('--inder', help='Directory ')
    parser.add_argument('--outdir', help='A file to save the pickled model object to.')
    args = parser.parse_args()
    image_maker = Make_images(args.inder, args.outdir)
