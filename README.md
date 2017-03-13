# Sign Edge

### Overview:
This is a project to create a machine learning method for classification of the type of street sign that is shown in a image. The method will be to use transfer learning from a pre-trained convolutional neural network and training a classification model on the features obtained.

### Business Understanding:
There is always need for new methods in recognition and classification of symbols and street signs for a number of uses including: self driving cars, street mapping, and driver safety systems. In sign classification, there aren't a lot of different methods that have been tried in an open source environment.

### The Data:
Data from a few different sources will be used. The first will be annotated LISA traffic sign dataset that can be found [here](http://cvrr.ucsd.edu/LISA/lisa-traffic-sign-dataset.html). Another source will be some pre-labeled images that was donated by the people at [Mapillary.com](http://mapillary.com). The bulk of the data will be scraped from public images on Flickr and Google images. The data will need to be cleaned by way of picking out the signs to be trained on, as well as weeding out any erroneous images by hand.

### Model:
* ***TBD***

### Outcome:
* The first benchmark for a minimal viable product would be a model that makes predictions off a small data set after using transfer learning.




### Possible Expansion:
 A possible expansion to this project would be to use a image vision technique (e.g. OpenCV libraries) to pick the signs out of the image.




### Citations:
Mapillary:
> Donation of 100 street signs around Seattle through correspondence with Janine Yoong of Mapillary.

LISA Dataset:
> Andreas Møgelmose, Mohan M. Trivedi, and Thomas B. Moeslund, "Vision based Traffic Sign Detection and Analysis for Intelligent Driver Assistance Systems: Perspectives and Survey," IEEE Transactions on Intelligent Transportation Systems, 2012.
