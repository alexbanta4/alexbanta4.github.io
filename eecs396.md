### Class Info and Contact Info

This project is for EECS 396, the Deep Learning seminar taught by Professor Bryan Pardo at Northwestern University.
If you have any further questions, reach out to Alex Banta at johnbanta2021@u.northwestern.edu, Noah Schaffer at noahschaffer2022@u.northwestern.edu, or Paulina Tarasul at paulinatarasul2022@u.northwestern.edu

### The Problem

We are interested in applying Neural Networks in music classification. More specifically, we would like to build a Neural Network architecture to identify whether a particular recording is a cover of another recording, e.g. it is a different performance of the same song by a different artist. We plan to adopt the architecture and experiments from a number of papers that do this. Our goal is to test the effectiveness of our architecture in being able to identify multiple versions of the same song, some of which may differ in key, tempo, instrumentation, and style.
  Music-hosting websites often want to know whether or not a song is a cover of an already published song, so that they can make sure it is appropriately labeled as such. In addition, this
is of interest in the music industry when it comes to plagiarism; often songs are covered or used without the permission of the initial artist. Since the neural network is being trained to identify cover songs based on similarity of content, this could possibly be expanded to identify plagiarism. A neural network that can take in an audio file and identify whether or not it is a cover song would be useful for processing the large volume of such songs. In terms of intellectual interest, it will be very interesting to work with a neural network aimed at classifying something as complex as a song, and to find out what a network needs in order to do so effectively.

###  Building and Testing the Network

For both the training and testing set, we used online datasets of cover songs, collected as MP3s  and converted to the Constant Q Transform format using the Librosa library. Our training dataset was a collection of 173 reference songs and 353 cover songs taken from the SecondHandSongs dataset. This resulted in 61069 (reference,cover) pairs for training. Our testing dataset was Covers80, which is a collection of 80 reference songs and their 80 corresponding covers, resulting in 3600 (reference,cover) pairs. 

![Figure 1](https://alexbanta4.github.io/networkarchitecture.png)

Our network architecture consists of a four-layer Siamese Convolutional Network based on Figure 1 from Stamenovic's paper on cover song detection using convolutional siamese networks (Stamenovic, 2020). Our input into the network is the Constant-Q Transform represenation of two songs and the network outputs a predicted label based on the distance between the two representations. To train the network, we took the mean squared error between our predicted label of the song pair and the true label of the song pair, where the true label is 0 if the pair contains a cover and 1 if the pair does not contain another. Figure 2 pictures our training loss.

![Figure 2](https://alexbanta4.github.io/LossCurve.png)

We tested the network by comparing each reference song in the testing set to each of the cover songs, and producing a ranking of the cover songs by similarity to the reference song. For each reference song, we then found where the correct corresponding cover song had been ranked. We measured our network’s success by how many cover songs were correctly ranked as their reference song’s first most similar, as well as how many cover songs were correctly ranked in the top ten most similar to their reference song. We chose to compare our network’s performance to the probable results of rankings set by chance alone. 

### Testing

We tested the network by comparing each reference song in the testing set to each of the cover songs, and producing a ranking of the cover songs by similarity to the reference song. For each reference song, we then found where the correct corresponding cover song had been ranked. We measured our network’s success by how many cover songs were correctly ranked as their reference song’s first most similar, as well as how many cover songs were correctly ranked in the top ten most similar to their reference song. We chose to compare our network’s performance to the probable results of rankings set by chance alone. 

### Results
![Figure 3](https://alexbanta4.github.io/RanksPlot.png)

For the 80 reference songs and 80 corresponding cover songs, we found that the network correctly ranked 3/80 covers first for their reference songs, and 21/80 correct covers in the top ten. This result is certainly better than chance. If the cover songs were ranked purely by chance, then the probability of any reference song correctly ranking its cover first would be 1/80. The probability of 3 reference songs ranking their correct covers first, then, would be 1.95x10-6, making our network’s performance significantly better than chance. The probability of 21/80 covers being correctly ranked in the top 10 for their reference songs would be 1.08x10-19 if the ranking were to happen by chance, making our network’s performance in this respect significantly better than chance as well. This means that our network performs very well as compared to the baseline to which we chose to compare it, that of chance performance.

### Final Paper

For further information, read the paper [Here](https://alexbanta4.github.io/Deep_Learning_Final_Paper.pdf)
