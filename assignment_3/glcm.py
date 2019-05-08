import numpy as np

def glcm_hist_dict(image):
    height, width = image.shape
    list_histogram = []
    image_histogram = {}
    glcm_dict = {}
    for i, x in zip(range(height), range(height)):
        for j, y in zip(range(width), range(width - 1)):
            pixel_pair = (image[x, y], image[x, y + 1])
            if pixel_pair in glcm_dict:
                glcm_dict[pixel_pair] += 1
            else:
                glcm_dict[pixel_pair] = 1
            if image[i, j] in image_histogram:
                image_histogram[image[i, j]] += 1
            else:
                image_histogram[image[i, j]] = 1
                list_histogram.insert(0, image[i, j])
    list_histogram.sort()
    return [list_histogram, image_histogram, glcm_dict]

def glcm_mounter(image):
    list_histogram, image_histogram, glcm_dict = glcm_hist_dict(image)
    aux_shape = len(list_histogram)

    matrix_glcm = np.zeros((aux_shape, aux_shape), dtype=np.float32)

    for n, i in zip(list_histogram, range(aux_shape)):
        for m, j in zip(list_histogram, range(aux_shape)):
            if (n, m) in glcm_dict:
                matrix_glcm[i, j] = glcm_dict[(n, m)]

    return matrix_glcm

