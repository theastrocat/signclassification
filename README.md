# Sign Edge

### Overview:
This is a project to create a machine learning method for classification of the type of street sign that is shown in a image. The method will use transfer learning from a pre-trained convolutional neural network and training a classification model on the features obtained.

In general, training a good neural network to do image classification can take a lot of time and resources. Luckily there exists extremely complex networks that have been pre-trained to classify many different items. But what happens when we want to use this method on something the neural network has never seen before? It wouldn't be able to make these classifications.

This is where transfer learning comes in. Transfer learning is an extremely powerful tool in machine learning when it comes to utilizing neural networks. By passing an image through the network without retraining it, but stopping it before making its classification prediction, you can extract features that the network thought were important enough about your image. You can then train a classification model on these features with good results.

### Business Understanding:
There is always need for new methods in recognition and classification of symbols and street signs for a number of uses including: self driving cars, street mapping, and driver safety systems. Classification has been done before, but there are no references that can be found for utilizing a transfer learning from a pre trained neural network.

### The Data:
The data used was the LISA traffic sign dataset that can be found [here](http://cvrr.ucsd.edu/LISA/lisa-traffic-sign-dataset.html). Labeled data from other sources will be utilized to improve the model further if needed.

To prepare the images they were cropped to the signs as well as weeding out any erroneous (small) images by hand. Reducing the number of classes by grouping or by removing the classes with the least images.

In all there were 15 classes with about 5500 images ranging from 12x12 to ~150x150 pixels. The classes are fairly unbalanced with stop signs making up the majority of the dataset.

### Model steps:
* Passing the LISA dataset through Inception V3 and ripping off the last node for training a classification model.
  * The bottleneck feature, which is a 2048 dimensional vector per image was used as a feature space for training a multinomial logistic regression classifier on.


### Feature Visualization:
* TSNE dimensionality reduction on the feature space to look at the groupings of the classes that my regression model is looking at.

### Outcome:
##### Benchmarks for a minimal viable product:
* A model that makes predictions off a small data set after using transfer learning.
* Building a website to house and show off the project.

### Next Steps:
 Using the LIME method for explanation of where the predictive power comes from in my image set.




### Citations:
LISA Dataset:
> Andreas Møgelmose, Mohan M. Trivedi, and Thomas B. Moeslund, "Vision based Traffic Sign Detection and Analysis for Intelligent Driver Assistance Systems: Perspectives and Survey," IEEE Transactions on Intelligent Transportation Systems, 2012.
