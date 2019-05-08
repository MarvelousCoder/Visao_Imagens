# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.xception import Xception
from keras.preprocessing import image
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from clr_callback import *
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Dropout
from keras import backend as K
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2 as cv
import os
import sys
import itertools
import glob

# nohup python3 train_Inception.py --dataset marcel --model output/Inception.model --label-bin output/Inception_lb.pickle --plot output/Inception_plot.png > Inception.out &

INIT_LR = 0.001
EPOCHS = 11
BS = 128
WIDTH = 299
HEIGHT = 299
DROPOUT = 0.75

def plot_confusion_matrix(classes, y_test, y_pred):
	cnf_matrix = confusion_matrix(y_test, y_pred)
	np.set_printoptions(precision=2)

	cnf_matrix = cnf_matrix.astype('float') / cnf_matrix.sum(axis=1)[:, np.newaxis]
	# Plot normalized confusion matrix
	plt.figure(figsize=(5, 5))
	plt.imshow(cnf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
	plt.title('Confusion matrix')
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=0)
	plt.yticks(tick_marks, classes)

	fmt = '.2f'
	thresh = cnf_matrix.max() / 2.
	for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
		plt.text(j, i, format(cnf_matrix[i, j], fmt), horizontalalignment="center",
					color="white" if cnf_matrix[i, j] > thresh else "black")

	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.tight_layout()
	plt.savefig("output/confusion_matrix_Inception.png")

def split(image_path):
	data = []
	labels = []

	lista = ["A", "B", "C", "Five", "Point", "V"]
	for sub in lista:
		for arq in glob.glob(image_path + sub +  "/*.ppm"):
			image = cv.imread(arq)
			image = cv.resize(image, (HEIGHT, WIDTH))
			data.append(image)
			labels.append(sub)
		
	# scale the raw pixel intensities to the range [0, 1]
	data = np.array(data, dtype="float")
	data = np.array(data, dtype="float") / 255.0
	labels = np.array(labels)

	return data, labels


def main():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--dataset", required=True,
		help="path to input dataset of images")
	ap.add_argument("-m", "--model", required=True,
		help="path to output trained model")
	ap.add_argument("-l", "--label-bin", required=True,
		help="path to output label binarizer")
	ap.add_argument("-p", "--plot", required=True,
		help="path to output accuracy/loss plot")
	args = vars(ap.parse_args())

	# initialize the data and labels
	print("[INFO] loading images...")

	# grab the image paths and randomly shuffle them
	image_path = args["dataset"] + "/train/"
	data, labels = split(image_path)
	(trainX, valX, trainY, valY) = train_test_split(data, labels, test_size=0.25)

	# convert the labels from integers to vectors (for 2-class, binary
	# classification you should use Keras' to_categorical function
	# instead as the scikit-learn's LabelBinarizer will not return a
	# vector)
	lb = LabelBinarizer()
	trainY = lb.fit_transform(trainY)
	valY = lb.transform(valY)

	# construct the image generator for data augmentation
	aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
		height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
		horizontal_flip=True, fill_mode="nearest")

	# base_model = InceptionV3(input_shape=(HEIGHT, WIDTH, 3),
							#  weights = 'imagenet', 
							#  include_top = False, 
							#  pooling = 'avg')
	base_model = InceptionResNetV2(input_shape=(HEIGHT, WIDTH, 3),
							 weights = 'imagenet', 
							 include_top = False, 
							 pooling = 'avg')
	# base_model = Xception(input_shape=(HEIGHT, WIDTH, 3),
							#  weights = 'imagenet', 
							#  include_top = False, 
							#  pooling = 'avg')
	x = base_model.output
	x = Dense(1024, activation="relu")(x)
	x = Dropout(DROPOUT)(x)
	predictions = Dense(6, activation="softmax")(x)

	model = Model(inputs=base_model.input, outputs=predictions)

	# initialize the model and optimizer
	print("[INFO] training network...")
	opt = SGD(lr=INIT_LR, momentum = 0.9, clipnorm = 5.)
	model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

	# saver = ModelCheckpoint("output/model.hdf5", verbose=1,
                            # save_best_only=True, monitor="val_acc",
                            # mode="max")
	# reduce_lr = ReduceLROnPlateau(monitor="loss", factor=0.5,
                                #   patience=5, verbose=1, min_lr=0.0001)
	stopper = EarlyStopping(patience=8, verbose=1, monitor="val_acc", mode="max")
	clr = CyclicLR(base_lr=INIT_LR, max_lr=0.005, step_size=8*len(trainX)//BS, mode='triangular2')
	# train the network
	H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
		validation_data=(valX, valY), steps_per_epoch=len(trainX) // BS,
		validation_steps=len(valX) // BS,
		epochs=EPOCHS, callbacks=[stopper, clr])

	##########################
	## EVALUATE THE NETWORK ##
	##########################
	print("[INFO] evaluating network...")
	image_path = args["dataset"] + "/test/"
	testX, testY = split(image_path)
	testY = lb.transform(testY)

	predictions = model.predict(testX, batch_size=BS)
	print(classification_report(testY.argmax(axis=1),
		predictions.argmax(axis=1), target_names=lb.classes_))
	print("Accuracy: {}".format(accuracy_score(testY.argmax(axis=1), predictions.argmax(axis=1))))
	print(confusion_matrix(testY.argmax(axis=1), predictions.argmax(axis=1)))

	# save the model and label binarizer to disk
	print("[INFO] serializing network and label binarizer...")
	model.save(args["model"])
	f = open(args["label_bin"], "wb")
	f.write(pickle.dumps(lb))
	f.close()

	print("[INFO] plotting and saving results...")
	# plot the training loss and accuracy
	N = np.arange(0, EPOCHS) if stopper.stopped_epoch == 0 else np.arange(0, stopper.stopped_epoch+1)
	# Se não parou antes então stopper.stopped_epoch será 0
	plt.style.use("ggplot")
	plt.figure()
	plt.plot(N, H.history["loss"], label="train_loss")
	plt.plot(N, H.history["val_loss"], label="val_loss")
	plt.plot(N, H.history["acc"], label="train_acc")
	plt.plot(N, H.history["val_acc"], label="val_acc")
	plt.title("Training Loss and Accuracy (Inception)")
	plt.xlabel("Epoch #")
	plt.ylabel("Loss/Accuracy")
	plt.legend()
	plt.savefig(args["plot"])

	plot_confusion_matrix(lb.classes_, testY.argmax(axis=1), predictions.argmax(axis=1))

	plt.style.use("ggplot")
	plt.figure()
	plt.plot(clr.history['lr'], clr.history['acc'])
	plt.title("Training Learning Rate and Accuracy (Inception)")
	plt.xlabel("Learning Rate")
	plt.ylabel("Accuracy")
	plt.legend()
	plt.savefig("output/learning_rate_Inception.png")
	print("Dropout: {} BS: {}".format(DROPOUT, BS))

if __name__ == '__main__':
	main()
