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
import itertools

# nohup python3 train.py --dataset marcel --model output/Inception_ResNetV2.model --plot output/Inception_ResNetV2_plot.png > Inception_ResNetV2.out &

INIT_LR = 0.001
EPOCHS = 15
BS = 47
WIDTH = 299
HEIGHT = 299
DROPOUT = 0.8

def plot_confusion_matrix(classes, y_test, y_pred):
	cnf_matrix = confusion_matrix(y_test, y_pred)
	np.set_printoptions(precision=2)

	cnf_matrix = cnf_matrix.astype('float') / cnf_matrix.sum(axis=1)[:, np.newaxis]
	# Plot normalized confusion matrix
	plt.figure(figsize=(10, 10))
	plt.imshow(cnf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
	plt.title('Confusion matrix')
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=90)
	plt.yticks(tick_marks, classes)

	fmt = '.2f'
	thresh = cnf_matrix.max() / 2.
	for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
		plt.text(j, i, format(cnf_matrix[i, j], fmt), horizontalalignment="center",
					color="white" if cnf_matrix[i, j] > thresh else "black")

	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.tight_layout()
	plt.savefig("output/confusion_matrix_inception_resnetv2.png")

def main():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--dataset", required=True,
		help="path to input dataset of images")
	ap.add_argument("-m", "--model", required=True,
		help="path to output trained model")
	ap.add_argument("-p", "--plot", required=True,
		help="path to output accuracy/loss plot")
	args = vars(ap.parse_args())

	# initialize the data and labels
	print("[INFO] loading images...")

	# grab the image paths and randomly shuffle them
	datagen = ImageDataGenerator(horizontal_flip=True,
									width_shift_range=0.1,
									height_shift_range=0.1,
									zoom_range=0.2,
									shear_range=0.2,
									rotation_range=30,
									rescale=1./255,
									fill_mode="nearest",
									validation_split=0.25)

	train_generator = datagen.flow_from_directory(args["dataset"] + "/train",
													target_size=(HEIGHT, WIDTH),
													batch_size=BS,
													subset='training')

	valid_generator = datagen.flow_from_directory(args["dataset"] + "/train",
												target_size=(HEIGHT, WIDTH),
												batch_size=BS,
												subset='validation')

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
	stopper = EarlyStopping(patience=7, verbose=1, monitor="val_acc", mode="max")
	clr = CyclicLR(base_lr=INIT_LR, max_lr=0.006, step_size=8*train_generator.samples//BS, 
					mode="triangular2")
	# train the network
	H = model.fit_generator(train_generator, validation_data=valid_generator,
							steps_per_epoch=train_generator.samples // BS, 
							validation_steps=valid_generator.samples // BS, 
							epochs=EPOCHS, callbacks=[stopper, clr])

	##########################
	## EVALUATE THE NETWORK ##
	##########################
	print("[INFO] Saving the Model...")
	model.save(args["model"])
	print("[INFO] evaluating network...")
	datagen = ImageDataGenerator(rescale=1./255)
	test_generator = datagen.flow_from_directory(args["dataset"] + "/test", 
													target_size=(HEIGHT, WIDTH),
													batch_size=BS,
													shuffle=False)
	Y_pred = model.predict_generator(test_generator, verbose=1, steps=test_generator.samples // BS)
	# steps precisa ser um inteiro exato. samples tem que ser múltiplo do batch size
	y_pred = np.argmax(Y_pred, axis=1)
	acc = accuracy_score(test_generator.classes, y_pred)
	print("Accuracy: ", acc)
	print(confusion_matrix(test_generator.classes, y_pred))
	

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
	plt.title("Training Loss and Accuracy (InceptionResNetV2)")
	plt.xlabel("Epoch #")
	plt.ylabel("Loss/Accuracy")
	plt.legend()
	plt.savefig(args["plot"])

	target_names = ["A", "B", "C", "Five", "Point", "V"]
	print(classification_report(test_generator.classes, y_pred, target_names=target_names))
	plot_confusion_matrix(target_names, test_generator.classes, y_pred)

	plt.style.use("ggplot")
	plt.figure()
	plt.plot(clr.history['lr'], clr.history['acc'])
	plt.title("Training Learning Rate and Accuracy (InceptionResNetV2)")
	plt.xlabel("Learning Rate")
	plt.ylabel("Accuracy")
	plt.legend()
	plt.savefig("output/learning_rate_inception_restnetv2.png")
	print("Dropout: {} BS: {}".format(DROPOUT, BS))

if __name__ == '__main__':
	main()
