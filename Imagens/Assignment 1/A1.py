import argparse
import cv2
from calcDistancias import calcDist
from transform import transGray
from olhaVizinhos import olhaVizinhos
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])

    # cv2.rectangle(image, (415, 260), (430, 290), 0, -1) # Desenha um retângulo na base
    # achaCaminho(image)
    contaComponentes(image)
    cv2.destroyAllWindows()

def achaCaminho(image):
    img = transGray(image)
    pOrigem = [415, 260]
    pAtual = [415, 260]
    pDestino = [1000, 815]
    num_pixels = 0
    energy = 0
    image[260, 415] = (0,0,0) # Base de operações 
    while(pAtual[0] != pDestino[0] or pAtual[1] != pDestino[1]): 
        # Enquanto não chegar ao destino continuo andando
        num_pixels += 1

        lista_dist = calcDist(pAtual[0], pAtual[1], pDestino[0], pDestino[1])
        # Calculo as distâncias dos 8 vizinhos do ponto atual até o ponto de destino.

        lista_dist.sort(key = lambda dist : dist[0]) # Ordenamos a lista de listas pelas distâncias 
        candidatos = [lista_dist[0], lista_dist[1], lista_dist[2]] # Pixels candidatos

        aux = 10000
        # Nesse for é escolhido o pixel com o nível de intensidade de cinza mais baixo da imagem cinza
        for i in range(3):
            if(img[candidatos[i][2], candidatos[i][1]] < aux): # Através do if atualizamos pixel atual
                aux = img[candidatos[i][2], candidatos[i][1]]
                pAtual[1] = candidatos[i][2]
                pAtual[0] = candidatos[i][1]
            # Mudamos o pixel atual considerando as distâncias e nível de intensidade de cinza
        energy += aux

        image[pAtual[1], pAtual[0]] = (0, 0, 0) # Pintamos o pixel de preto

    # cv2.WINDOW_NORMAL permite que a janela seja redimensionada!
    cv2.namedWindow("Saida", cv2.WINDOW_NORMAL) 
    cv2.imshow("Saida", image)
    cv2.imwrite("Mars_Caminho.bmp", image)
    cv2.waitKey(0)

    print("Imagens salvas!")
    print("O caminho de (%d;%d) até (%d;%d) foi feito em %d pixels com %d unidades de energia." 
            %(pOrigem[0], pOrigem[1], pDestino[0], pDestino[1], num_pixels, energy))

def contaComponentes(img):
    # blurred = cv2.GaussianBlur(image, (11, 11), 0)
    # edged = cv2.Canny(blurred, 30, 150)

    # # ARGUMENTOS findCountours:
    # # first - edged image, a copy only since this function is destructive
    # # second - type of contour
    # # third - how we want to approximate the contour

    # (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print("I found %d coins in this image" % (len(cnts)))
    # cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)

    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    count = 1
    fifo = [] # Fila First in First Out para fazer busca em largura

    # aux = img.copy()
    width = img.shape[1] 
    height = img.shape[0] 
    arr = np.zeros((width + 2, height + 2, 3), dtype = int) + 255

    arr[1:(width+1), 1:(height+1)] = img[0:512, 0:512]
    width = arr.shape[1] 
    height = arr.shape[0]
    black = (0, 0, 0)

    for j in range(1, height):
        for i in range(1, width):
            if(arr[j, i, 0] == 0):
                fifo.append([count, j, i])
                arr[j, i, 0] = count
                while (fifo):
                    pixel = fifo.pop(0)
                    lista = olhaVizinhos(pixel[1], pixel[2])
                    for vizinho in lista:
                        y = vizinho[1]
                        x = vizinho[0]
                        if(arr[y, x, 0] == 0):
                            arr[y, x, 0] = pixel[0]
                            fifo.append([pixel[0], y, x])
                count += 1

    print("Eu encontrei %d componentes conectados" %(count-1))
    print("height: {}, width: {}".format(height, width))





if __name__ == "__main__":
    main()

