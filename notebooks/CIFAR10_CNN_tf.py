# Train LeNet with tensorflow on CIFAR10 image classification

import numpy as np
import tensorflow as tf
import matplotlib.image as img
import pdb

# Load data: Convert .png images in training and testing datasets into addressable matrices.

# Get the current directory for getting the png data
# import os
# cwd = os.getcwd()

# Load data: Convert .png images in training and testing datasets into addressable matrices.

# Get the current directory for getting the png data
# import os
# cwd = os.getcwd()

ntrain = 1000 # per class
ntest = 100 # per class
nclass = 10 # number of classes
imsize = 28
nchannels = 1  # No color, only grey scale

# Train = np.zeros((ntrain*nclass,imsize,imsize,nchannels))
Train = np.zeros((ntrain*nclass,imsize * imsize))
Test = np.zeros((ntest*nclass,imsize * imsize))
LTrain = np.zeros((ntrain*nclass,nclass))
LTest = np.zeros((ntest*nclass,nclass))
itrain = -1
itest = -1

for iclass in range(0, nclass):
    for isample in range(0, ntrain):
        path = '/notebooks/CIFAR10/Train/%d/Image%05d.png' % (iclass,isample)
        im = img.imread(path); # 28 by 28
        im = im.astype(float)
        itrain += 1
        # Train[itrain,:,:,0] = im
        im_mean = np.mean(im.reshape(1, imsize * imsize))
        Train[itrain, :] = im.reshape(1, imsize * imsize) -  im_mean 
        LTrain[itrain, iclass] = 1 # 1-hot lable
    for isample in range(0, ntest):
        path = '/notebooks/CIFAR10/Test/%d/Image%05d.png' % (iclass,isample)
        im = img.imread(path); # 28 by 28
        im = im.astype(float)
        itest += 1
        # Test[itest,:,:,0] = im
        im_mean = np.mean(im.reshape(1, imsize * imsize))
        Test[itest,:] = im.reshape(1, imsize * imsize) - im_mean 
        LTest[itest,iclass] = 1 # 1-hot lable

# Shuffle the dataset

num_examples = itrain + 1
perm = np.arange(num_examples)
np.random.shuffle(perm)
Train = Train[perm, :]
LTrain = LTrain[perm, :]

def next_batch(x, y, batch_size, index_in_epoch):
    start = index_in_epoch
    index_in_epoch += batch_size
    num_examples = 10000
    if index_in_epoch > num_examples:
        # Shuffle the data
        # perm = np.arange(num_examples)
        # np.random.shuffle(perm)
        # x = x[perm, :]
        # y = y[perm, :]
        # Start next epoch
        start = 0
        index_in_epoch = batch_size
    # assert batch_size <= num_examples
    end = index_in_epoch
    return x[start:end, :], y[start:end, :], index_in_epoch

# Parameters
learning_rate = 0.001
training_iters = 200000
batch_size = 128
display_step = 10
imsize = 28

# Network Parameters
n_input = imsize ** 2 # MNIST data input (img shape: 28*28)
n_classes = 10 # MNIST total classes (0-9 digits)
dropout = 0.75 # Dropout, probability to keep units

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) #dropout (keep probability)

# Create some wrappers for simplicity
def conv2d(x, W, b, strides=1):
    # Conv2D wrapper, with bias and relu activation
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def maxpool2d(x, k=2):
    # MaxPool2D wrapper
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],
                          padding='SAME')


# Create model
def conv_net(x, weights, biases, dropout):
    # Reshape input picture
    x = tf.reshape(x, shape=[-1, 28, 28, 1])

    # Convolution Layer
    conv1 = conv2d(x, weights['wc1'], biases['bc1'])
    # Max Pooling (down-sampling)
    conv1 = maxpool2d(conv1, k=2)

    # Convolution Layer
    conv2 = conv2d(conv1, weights['wc2'], biases['bc2'])
    # Max Pooling (down-sampling)
    conv2 = maxpool2d(conv2, k=2)

    # Fully connected layer
    # Reshape conv2 output to fit fully connected layer input
    fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
    fc1 = tf.nn.relu(fc1)
    # Apply Dropout
    fc1 = tf.nn.dropout(fc1, dropout)

    # Output, class prediction
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
    return out

# Store layers weight & bias
weights = {
    # 5x5 conv, 1 input, 32 outputs
    'wc1': tf.Variable(tf.random_normal([5, 5, 1, 32])),
    # 5x5 conv, 32 inputs, 64 outputs
    'wc2': tf.Variable(tf.random_normal([5, 5, 32, 64])),
    # fully connected, 7*7*64 inputs, 1024 outputs
    'wd1': tf.Variable(tf.random_normal([7*7*64, 1024])),
    # 1024 inputs, 10 outputs (class prediction)
    'out': tf.Variable(tf.random_normal([1024, n_classes]))
}

biases = {
    'bc1': tf.Variable(tf.random_normal([32])),
    'bc2': tf.Variable(tf.random_normal([64])),
    'bd1': tf.Variable(tf.random_normal([1024])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Construct model
pred = conv_net(x, weights, biases, keep_prob)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
overlap = [pred, y]
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.initialize_all_variables()

#  Launch the gragh
with tf.Session() as sess:
    sess.run(init)
    step = 1
    # Keep training until reach max iterations
    index_in_epoch = 0
    while step * batch_size < training_iters:
        # Train CIFAR data
        batch_x, batch_y, index_in_epoch = next_batch(Train, LTrain, batch_size, index_in_epoch)
        # Run optimization op (backprop)
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, keep_prob: dropout})
        if step % display_step == 0:
            # Calculate batch loss and accuracy
            loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x, y: batch_y, keep_prob: 1.})

            print ("Iter " + str(step*batch_size) + ", Minibatch Loss= " + "{:.6f}".format(loss) + ", Training Accuracy= " + "{:.5f}".format(acc))
        step += 1
    print ("Optimization Finished!")
    final_w = sess.run([weights], feed_dict={x: batch_x, y: batch_y, keep_prob: 1.})
    test = sess.run([overlap], feed_dict={x: batch_x, y: batch_y, keep_prob: 1.})

    # Calculate accuracy for 256 mnist test images
    print ("Testing Accuracy:", sess.run(accuracy, feed_dict={x: Test[:256], y: LTest[:256], keep_prob: 1.}))