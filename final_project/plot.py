import matplotlib.pyplot as plt
import numpy as np
import itertools

classes = ["A", "B", "C", "Five", "Point", "V"]

cnf_matrix = np.array(
[[ 88,   0,   0,   7,   1,   0],
 [  0,  83,   0,  19,   0,   0],
 [  0,   0, 110,   2,   0,   0],
 [  0,   0,   0, 127,   1,   6],
 [  1,   0,   0,   0, 118,   0],
 [  0,   1,   0,   5,  13,  76]]
)

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
plt.savefig("resultados/confusion_matrix_inception.png")