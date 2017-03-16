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
    def __init__(self, indir, outdir, con_in = False):
        self.con_in = con_in
        self.indir = indir
        if outdir[-1] == '/':
            self.outdir = outdir
        else:
            self.outdir = outdir + '/'
        self.annot = 'frameAnnotations.csv'
        self.image_str = None
        self.image_dirs = [str(x) for x in os.listdir(self.indir) if x[-1].isdigit()]
        self.image_paths = []
        self.image_paths = []
        self.save_paths = []
        self.saved_images = []
        for direct in self.image_dirs:
            for subdir in os.listdir(self.indir+direct):
                if subdir[0].isalpha():
                    self.image_paths.append(self.indir+direct+'/'+subdir+'/')
        if con_in:
            self.main_call()
    def main_call(self):
        """
        Main loop for standard run of the code.
        """
        for ind in range(len(self.image_paths)):
            self.make_out_dir(ind)
            image_dict  = self.get_image_dict(ind)
            self.crop_images(ind,image_dict)
            print "Finished set: {}".format(ind)
    def make_out_dir(self,index):
        """
        Creates the output directory.
        """
        save_path = self.outdir + r'fullset/set_{}'.format(index)
        self.save_paths.append(save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print "Creating path: " + save_path
        with open(save_path + '/path.txt', 'w') as f:
            f.write(self.image_paths[index])
    def get_image_dict(self,index):
        """
        Pulls an image in with PIL and
        """
        print "Starting set: " + str(index)
        current = self.image_paths[index]
        images = [x for x in os.listdir(current) if '.png' in x]
        image_annot = pd.read_csv(current+self.annot, delimiter=';')
        image_bounds = {}
        for row in range(len(image_annot)):
            image_bounds[image_annot.loc[row][0]] = (image_annot.loc[row][1],
                                                    [float(x) for x in str(image_annot.loc[row][2:6]).split() if x.isdigit()]                                        )
        return image_bounds
    def crop_images(self,index,img_dict):
        """
        Crops image
        """
        saved_images = []
        for im in img_dict.keys():
            img = Image.open(self.image_paths[index]+im)
            img2 = img.crop(tuple(img_dict[im][1]))
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
            image_str = '{}{}'.format(img_dict[im][0], str(img4.size))

            self.write_images(img4,index,img_dict[im][0])
            saved_images.append(self.image_str)

    def write_images(self,image,index,img_str):
        self.image_str = '{}{}'.format(img_str, str(image.size))
        x = 0
        while self.image_str + str(x) in self.saved_images:
            x += 1
        self.image_str += str(x)
        image.save(self.outdir+"set_{}/{}.jpg".format(index, self.image_str))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Method for parsing LISA sign data into cropped images.')
    parser.add_argument('--indir', help='Directory ')
    parser.add_argument('--outdir', help='A file to save the pickled model object to.')
    args = parser.parse_args()
    image_maker = Make_Images(args.indir, args.outdir, con_in = True)
