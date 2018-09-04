import argparse
import cv2
import numpy as np
from calcDists import calc_dist
from transform import transYcbcr

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
transYcbcr(image)

# cv2.rectangle(image, (415, 260), (430, 290), 0, -1)
# image[260, 415] = (0, 0, 255)
# image[260:263, 415:418] = (255, 255, 255)
# image[815:818, 1000:1003] = (255, 255, 255)
# image[815,1000] = (0, 0, 255)

pOrigem = [415, 260]
pAtual = pOrigem
pDestino = [1000, 815]
num_pixels = 0
energy = 0

width = image.shape[1]
height = image.shape[2]
dists = np.zeros((width+2, height+2), dtype = "int") - 1
for i in range(width):
    for j in range(height):
        dists[i][j] = np.sqrt((1000 - i)**2 + (815 - j)**2)

while(pAtual[0] != pDestino[0] or pAtual[1] != pDestino[1]):
    num_pixels += 1

    lista_dist = calc_dist(pAtual[0], pAtual[1], pDestino[0], pDestino[1], dists)
    
    lista_dist.sort()
    candidatos = [lista_dist[0], lista_dist[1], lista_dist[2]]

    aux = 10000
    for i in range(3):
        if(image[candidatos[i][2], candidatos[i][1], 0] < aux):
            aux = image[candidatos[i][2], candidatos[i][1], 0]
            pAtual[1] = candidatos[i][2]
            pAtual[0] = candidatos[i][1]
    energy += aux

    image[pAtual[1], pAtual[0]] = (0, 0, 0)


cv2.namedWindow("Saida", cv2.WINDOW_NORMAL)
cv2.imshow("Saida", image)
cv2.imwrite("Mars_Caminho.bmp", image)
cv2.waitKey(0)

print("Imagens salvas!")
print("O caminho de (%d;%d) até (%d;%d) foi completado em %d pixels com %d unidades de energia." 
        %(pOrigem[0], pOrigem[1], pDestino[0], pDestino[1], num_pixels, energy))


cv2.destroyAllWindows()