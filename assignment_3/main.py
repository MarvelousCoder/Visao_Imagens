import cv2 as cv
import glob
import argparse
import matplotlib.pyplot as plt
import os
import itertools

from sklearn.metrics import confusion_matrix, f1_score, classification_report, accuracy_score
from sklearn.preprocessing import normalize
from sklearn.neighbors import KNeighborsClassifier
from imutils import paths

from glcm import *
from features import *

def rgb_to_greyscale(image):
    height, width, channels = image.shape
    grey = np.zeros((height, width), dtype = np.uint8)

    grey[:, :] = (0.114 * image[:, :, 0]) + (0.587 * image[:, :, 1]) + (0.299 * image[:, :, 2])
    return grey

# Para cada imagem adquiro sua matriz GLCM e suas respectivas features.
def extract_features(images, discard=False):
    features_array = []

    for img in images:
        matrix_glcm = glcm_mounter(rgb_to_greyscale(img))
        matrix_glcm /= np.sum(matrix_glcm)

        if(discard): # Descarta uma feature
            features = all_features(matrix_glcm, 3)
            for l in features:
                features_array.append(l)
        else:
            features = all_features(matrix_glcm) 
            features_array.append(features)
        
    features_array = np.array(features_array, dtype = np.float32)
    if(discard):
        data = np.reshape(features_array, (features_array.shape[0]//3, 3))
        return data
    return features_array

def plot_confusion_matrix(classes, y_test, y_pred):
	cnf_matrix = confusion_matrix(y_test, y_pred)
	np.set_printoptions(precision=2)

	cnf_matrix = cnf_matrix.astype('float') / cnf_matrix.sum(axis=1)[:, np.newaxis]

	# Plot normalized confusion matrix
	plt.figure(figsize=(4, 4))
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
	plt.savefig("confusion_matrix.png")


def split(image_path):
	data = []
	labels = []

	for img in image_path:
		image = cv.imread(img)
		data.append(image)

		label = img.split(os.path.sep)[-2]
		labels.append(label)

	data = np.array(data, dtype="float")
	labels = np.array(labels)

	return data, labels

def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset",
        help="path to input directory of images", default="images")
    args = vars(ap.parse_args())

    print("[INFO] loading images...")
    image_path = sorted(list(paths.list_images(args["dataset"] + "/train")))
    trainX, trainY = split(image_path)

    print("[INFO] extracting features...")
    train_feat_array = extract_features(trainX)

    print("[INFO] making feature relation...")
    # Descubro qual feature devo ignorar #
    feature_relation(train_feat_array)

    clf = KNeighborsClassifier(n_jobs=-1, n_neighbors=5)

    print("[INFO] loading images with one feature discarded...")
    trainX = extract_features(trainX, discard=True)
    normalize(trainX)
    clf.fit(trainX, trainY)
    
    image_path = sorted(list(paths.list_images(args["dataset"] + "/test")))
    testX, testY = split(image_path)
    testX = extract_features(testX, discard=True)

    normalize(testX)
    print("[INFO] evaluating the classifier for binary and multiclass classification...")
    y_pred = clf.predict(testX)
    print("Accuracy: {}".format(accuracy_score(testY, y_pred)))
    classes = ["asphalt", "danger", "grass"]
    plot_confusion_matrix(classes, testY, y_pred)

    trainY[(trainY != "asphalt")] = "not"
    trainY[(trainY == "asphalt")] = "safe"
    testY[(testY != "asphalt")] = "not"
    testY[(testY == "asphalt")] = "safe"
    clf.fit(trainX, trainY)
    y_pred = clf.predict(testX)
    print(classification_report(testY, y_pred))
    # print("F1-Score: {}".format(f1_score(testY, y_pred)))


if __name__ == "__main__":
    main()