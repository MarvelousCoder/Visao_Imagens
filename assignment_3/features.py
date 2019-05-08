import numpy as np
import matplotlib.pyplot as plt


def contrast(matrix):
    height, width = matrix.shape
    sum_contrast = 0

    for i in range(height):
        for j in range(width):
            sum_contrast += ((abs(i - j))**2) * matrix[i, j]
    return sum_contrast

def energy(matrix):
    height, width = matrix.shape
    sum_energy = 0

    for i in range(height):
        for j in range(width):
            sum_energy += (matrix[i, j])**2
    return sum_energy

def homogeneity(matrix):
    height, width = matrix.shape
    sum_homogeneity = 0

    for i in range(height):
        for j in range(width):
            sum_homogeneity += matrix[i, j]/(1 + (abs(i - j)))
    return sum_homogeneity

def correlation(matrix):
    height, width = matrix.shape
    list_sum_i = []
    list_sum_j = []

    for i, j in zip(range(height), range(width)):
        sum_i = np.sum(matrix[i, :])
        sum_j = np.sum(matrix[:, j])
        list_sum_i.append(sum_i)
        list_sum_j.append(sum_j)
        sum_i = 0
        sum_j = 0

    average_sum_i = 0
    average_sum_j = 0

    for i in range(1, height+1):
        average_sum_i += i * (list_sum_i[i-1])
    for j in range(1, width+1):
        average_sum_j += j * (list_sum_j[j-1])

    sum_aux = 0
    for i in range(1, height+1):
        sum_aux += ((i - average_sum_i)**2) * list_sum_i[i - 1]
    std_i = sum_aux**(1/2)
    sum_aux = 0
    for j in range(1, width+1):
        sum_aux += ((j - average_sum_j)**2) * list_sum_j[j - 1]
    std_j = sum_aux**(1/2)

    sum_corr = 0
    for i in range(1, height+1):
        for j in range(1, width+1):
            sum_corr += ((i - average_sum_i) * (j - average_sum_j) * matrix[i-1, j-1])/(std_i * std_j)
    return sum_corr

def all_features(matrix, exclude = 0):
    height, width = matrix.shape
    sum_contrast = 0
    sum_corr = 0
    sum_energy = 0
    sum_homogeneity = 0
    list_sum_i = []
    list_sum_j = []

    for i, j in zip(range(height), range(width)):
        sum_i = np.sum(matrix[i, :])
        sum_j = np.sum(matrix[:, j])
        list_sum_i.append(sum_i)
        list_sum_j.append(sum_j)

    average_sum_i = 0
    average_sum_j = 0
    if exclude != 4:
        for i in range(1, height + 1):
            average_sum_i += i * (list_sum_i[i - 1])
        for j in range(1, width + 1):
            average_sum_j += j * (list_sum_j[j - 1])

        sum_aux = 0
        for i in range(1, height + 1):
            sum_aux += ((i - average_sum_i) ** 2) * list_sum_i[i - 1]
        std_i = sum_aux ** (1 / 2)
        sum_aux = 0
        for j in range(1, width + 1):
            sum_aux += ((j - average_sum_j) ** 2) * list_sum_j[j - 1]
        std_j = sum_aux ** (1 / 2)

    for i in range(1, height + 1):
        for j in range(1, width + 1):
            if exclude != 1:
                sum_contrast += ((abs(i - j))**2) * matrix[i - 1, j - 1]
            if exclude != 2:
                sum_energy += (matrix[i - 1, j - 1])**2
            if exclude != 3:
                sum_homogeneity += matrix[i - 1, j - 1]/(1 + (abs(i - j)))
            if exclude != 4:
                sum_corr += ((i - average_sum_i) * (j - average_sum_j) *
                                 matrix[i - 1, j - 1]) / (std_i * std_j)

    if(exclude == 3):
        return [sum_contrast, sum_corr, sum_energy]
    return [sum_contrast, sum_corr, sum_energy, sum_homogeneity]

# Faço a relação de todas as features entre os três tipos de terreno #
# 1 = Asfalto, primeiras 25 imagens #
# 2 = Perigo, próximas 25 imagens #
# 3 = Grama, próximas 25 imagens #
# Com esses valores, seleciono o maior valor de cada terreno e identifico a característica em comum nas 3 relações, então a elimino #

def feature_relation(feat_array):
    for type in range(3):
        if type == 1:
            relation_con_cor = np.corrcoef(feat_array[:25, 0], feat_array[:25, 1])
            relation_con_ene = np.corrcoef(feat_array[:25, 0], feat_array[:25, 2])
            relation_con_hom = np.corrcoef(feat_array[:25, 0], feat_array[:25, 3])
            relation_cor_ene = np.corrcoef(feat_array[:25, 1], feat_array[:25, 2])
            relation_cor_hom = np.corrcoef(feat_array[:25, 1], feat_array[:25, 3])
            relation_ene_hom = np.corrcoef(feat_array[:25, 2], feat_array[:25, 3])
            relation_list_1 = [(abs(relation_con_cor[0, 1]), 'Contrast&Correlation'), (abs(relation_con_ene[0, 1]), 'Contrast&Energy'), (abs(relation_con_hom[0, 1]), 'Contrast&Homogeneity'),
                             (abs(relation_cor_ene[0, 1]), 'Correlation&Energy'), (abs(relation_cor_hom[0, 1]), 'Correlation&Homogeneity'), (abs(relation_ene_hom[0, 1]), 'Energy&Homogeneity')]
            relation_list_1.sort()
        elif type == 2:
            relation_con_cor = np.corrcoef(feat_array[25:50, 0], feat_array[25:50, 1])
            relation_con_ene = np.corrcoef(feat_array[25:50, 0], feat_array[25:50, 2])
            relation_con_hom = np.corrcoef(feat_array[25:50, 0], feat_array[25:50, 3])
            relation_cor_ene = np.corrcoef(feat_array[25:50, 1], feat_array[25:50, 2])
            relation_cor_hom = np.corrcoef(feat_array[25:50, 1], feat_array[25:50, 3])
            relation_ene_hom = np.corrcoef(feat_array[25:50, 2], feat_array[25:50, 3])
            relation_list_2 = [(abs(relation_con_cor[0, 1]), 'Contrast&Correlation'), (abs(relation_con_ene[0, 1]), 'Contrast&Energy'), (abs(relation_con_hom[0, 1]), 'Contrast&Homogeneity'),
                             (abs(relation_cor_ene[0, 1]), 'Correlation&Energy'), (abs(relation_cor_hom[0, 1]), 'Correlation&Homogeneity'), (abs(relation_ene_hom[0, 1]), 'Energy&Homogeneity')]
            relation_list_2.sort()
        else:
            relation_con_cor = np.corrcoef(feat_array[50:, 0], feat_array[50:, 1])
            relation_con_ene = np.corrcoef(feat_array[50:, 0], feat_array[50:, 2])
            relation_con_hom = np.corrcoef(feat_array[50:, 0], feat_array[50:, 3])
            relation_cor_ene = np.corrcoef(feat_array[50:, 1], feat_array[50:, 2])
            relation_cor_hom = np.corrcoef(feat_array[50:, 1], feat_array[50:, 3])
            relation_ene_hom = np.corrcoef(feat_array[50:, 2], feat_array[50:, 3])
            relation_list_3 = [(abs(relation_con_cor[0, 1]), 'Contrast&Correlation'), (abs(relation_con_ene[0, 1]), 'Contrast&Energy'), (abs(relation_con_hom[0, 1]), 'Contrast&Homogeneity'),
                             (abs(relation_cor_ene[0, 1]), 'Correlation&Energy'), (abs(relation_cor_hom[0, 1]), 'Correlation&Homogeneity'), (abs(relation_ene_hom[0, 1]), 'Energy&Homogeneity')]
            relation_list_3.sort()

    greatest_relation_1 = relation_list_1[5]
    greatest_relation_2 = relation_list_2[5]
    greatest_relation_3 = relation_list_3[5]

    print("- Greatest Relations -")
    print("Asphalt: \n - Value: [", greatest_relation_1[0], "]  Relation: [", greatest_relation_1[1], "]")
    print("Danger: \n - Value: [", greatest_relation_2[0], "]  Relation: [", greatest_relation_2[1], "]")
    print("Grass: \n - Value: [", greatest_relation_3[0], "]  Relation: [", greatest_relation_3[1], "]")
    print()

    # Contraste e Correlação #
    plt.scatter(feat_array[:26, 0], feat_array[:26, 1], color='blue')
    plt.scatter(feat_array[26:51, 0], feat_array[26:51, 1], color='red')
    plt.scatter(feat_array[51:, 0], feat_array[51:, 1], color='green')
    plt.xlabel('Contrast')
    plt.ylabel('Correlation')
    plt.savefig("./CONvsCOR.png")
    plt.close()

    # Contraste e Energia #
    plt.scatter(feat_array[:26, 0], feat_array[:26, 2], color='darkblue')
    plt.scatter(feat_array[26:51, 0], feat_array[26:51, 2], color='crimson')
    plt.scatter(feat_array[51:, 0], feat_array[51:, 2], color='darkgreen')
    plt.xlabel('Contrast')
    plt.ylabel('Energy')
    plt.savefig("./CONvsENE.png")
    plt.close()

    # Correlação e Energia #
    plt.scatter(feat_array[:26, 1], feat_array[:26, 2], color='lightblue')
    plt.scatter(feat_array[26:51, 1], feat_array[26:51, 2], color='coral')
    plt.scatter(feat_array[51:, 1], feat_array[51:, 2], color='lightgreen')
    plt.xlabel('Correlation')
    plt.ylabel('Energy')
    plt.savefig("./CORvsENE.png")
    plt.close()