### The Problem

We are interested in applying Neural Networks in music classification. More specifically, we would like to build a Neural Network architecture to identify whether a particular recording is a cover of another recording, e.g. it is a different performance of the same song by a different artist. We plan to adopt the architecture and experiments from a number of papers that do this. Our goal is to test the effectiveness of our architecture in being able to identify multiple versions of the same song, some of which may differ in key, tempo, instrumentation, and style.
  Music-hosting websites often want to know whether or not a song is a cover of an already published song, so that they can make sure it is appropriately labeled as such. In addition, this
is of interest in the music industry when it comes to plagiarism; often songs are covered or used without the permission of the initial artist. Since the neural network is being trained to identify cover songs based on similarity of content, this could possibly be expanded to identify plagiarism. A neural network that can take in an audio file and identify whether or not it is a cover song would be useful for processing the large volume of such songs. In terms of intellectual interest, it will be very interesting to work with a neural network aimed at classifying something as complex as a song, and to find out what a network needs in order to do so effectively.


### Solving the Problem



###  Building and Testing the Network

For both the training and testing set, we used online datasets of cover songs, collected as MP3s  and converted to the Constant Q Transform format using the Librosa library. Our training dataset was a collection of 173 reference songs and 353 cover songs taken from the SecondHandSongs dataset. This resulted in 61069 (reference,cover) pairs for training. Our testing dataset was Covers80, which is a collection of 80 reference songs and their 80 corresponding covers, resulting in 3600 (reference,cover) pairs. 

![Figure 1](https://alexbanta4.github.io/networkarchitecture.png)

Our network architecture consists of a four-layer Siamese Convolutional Network based on Figure 1 from Stamenovic's paper on cover song detection using convolutional siamese networks (Stamenovic, 2020). Our input into the network is the Constant-Q Transform represenation of two songs and the network outputs a predicted label based on the distance between the two representations. To train the network, we took the mean squared error between our predicted label of the song pair and the true label of the song pair, where the true label is 0 if the pair contains a cover and 1 if the pair does not contain another. Figure 2 pictures our training loss.

![Figure 2](https://alexbanta4.github.io/LossCurve.png)
