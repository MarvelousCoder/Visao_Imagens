import argparse
import cv2
from calcula_dist import calcula_dist
from transform import trans_gray
from olha_vizinhos import olha_vizinhos
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i1", "--image1", required=True, help="Caminho para a imagem 1 e 2")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image1"])

    # cv2.rectangle(image, (415, 260), (430, 290), 0, -1) # Desenha um retângulo na base
    # acha_caminho(image)
    conta_componentes(image)
    cv2.destroyAllWindows()

def acha_caminho(image):
    img = trans_gray(image)
    p_origem = [415, 260]
    p_atual = [415, 260]
    p_destino = [1000, 815]
    num_pixels = 0
    energy = 0
    image[260, 415] = (0,0,0) # Base de operações 
    while(p_atual[0] != p_destino[0] or p_atual[1] != p_destino[1]): 
        # Enquanto não chegar ao destino continuo andando
        num_pixels += 1

        lista_dist = calcula_dist(p_atual[0], p_atual[1], p_destino[0], p_destino[1])
        # Calculo as distâncias dos 8 vizinhos do ponto atual até o ponto de destino.

        lista_dist.sort(key = lambda dist : dist[0]) # Ordenamos a lista de listas pelas distâncias 
        candidatos = [lista_dist[0], lista_dist[1], lista_dist[2]] # Pixels candidatos

        aux = 10000
        # Nesse for é escolhido o pixel com o nível de intensidade de cinza mais baixo da imagem cinza
        for candidato in candidatos:
            if(img[candidato[2], candidato[1]] < aux): # Através do if atualizamos pixel atual
                aux = img[candidato[2], candidato[1]]
                p_atual[1] = candidato[2]
                p_atual[0] = candidato[1]
            # Mudamos o pixel atual considerando as distâncias e nível de intensidade de cinza   
        energy += aux

        image[p_atual[1], p_atual[0]] = (0, 0, 0) # Pintamos o pixel de preto

    # cv2.WINDOW_NORMAL permite que a janela seja redimensionada!
    cv2.namedWindow("Saida", cv2.WINDOW_NORMAL) 
    cv2.imshow("Saida", image)
    cv2.imwrite("Mars_Caminho.bmp", image)
    cv2.waitKey(0)

    print("Imagens salvas!")
    print("O caminho de (%d;%d) até (%d;%d) foi feito em %d pixels com %d unidades de energia." 
            %(p_origem[0], p_origem[1], p_destino[0], p_destino[1], num_pixels, energy))

def conta_componentes(img):
    count = 1
    fila = [] # Fila First in First Out para fazer busca em largura

    width = img.shape[1] 
    height = img.shape[0] 
    arr = np.zeros((width + 2, height + 2, 3), dtype = int) + 255

    arr[1:(width+1), 1:(height+1)] = img[0:width, 0:height]

    for j in range(height):
        for i in range(width):
            if(arr[j, i, 0] == 0):
                fila.append([j, i])
                arr[j, i, 0] = count
                while (fila):
                    pixel = fila.pop(0)
                    lista_vizinhos = olha_vizinhos(pixel[0], pixel[1])
                    for vizinho in lista_vizinhos:
                        y = vizinho[1]
                        x = vizinho[0]
                        if(arr[y, x, 0] == 0):
                            arr[y, x, 0] = count
                            fila.append([y, x])
                count += 1

    print("Eu encontrei %d componentes conectados" %(count-1))


if __name__ == "__main__":
    main()

