""" 
Nome: Raphael Soares Ramos
Matrícula: 140160299

Leia o read_me.txt para mais informações.
"""

import argparse
import cv2
from calcula_dist import calcula_dist
from transform import trans_gray_eq
from olha_vizinhos import olha_vizinhos
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i1", "--image1", required = True, help="Path para a imagem Mars.bmp")
    ap.add_argument("-i2", "--image2", required = True, help = "Path para a imagem spots.tif")
    args = vars(ap.parse_args())

    image_1 = cv2.imread(args["image1"]) # Abre a imagem Mars.bmp
    image_2 = cv2.imread(args["image2"]) # Abre a imagem spots.tif

    # cv2.rectangle(image, (415, 260), (430, 290), 0, -1) # Desenha um retângulo na base
    acha_caminho(image_1)
    conta_componentes(image_2, "preto")
    image_neg = cv2.bitwise_not(image_2) # Usamos a imagem "negada" para encontrar os buracos :)
    conta_componentes(image_neg, "buracos")
    cv2.destroyAllWindows()

def acha_caminho(image):
    img = trans_gray_eq(image) # Imagem cinza equalizada passa a ter um único canal a partir daqui!
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
    cv2.imwrite("Mars_Eq.bmp", img)
    cv2.waitKey(0)

    print("Imagens salvas!")
    print("O caminho de (%d;%d) até (%d;%d) foi feito em %d pixels com %d unidades de energia." 
            %(p_origem[0], p_origem[1], p_destino[0], p_destino[1], num_pixels, energy))

def conta_componentes(img, tarefa): # A estratégia BFS será usada para contar os componentes e rotulá-los
    count = 1 # Contador do número de componentes
    fila = [] # Fila First in First Out para fazer busca em largura

    width = img.shape[1] 
    height = img.shape[0] 
    arr = np.zeros((width + 2, height + 2, 3), dtype = int) + 255
    """ Criamos um numpy array, que é como as imagens são representadas em OpenCV para python, 
        cheios com a cor branca para tratar os vizinhos de pixels da borda da imagem. 
        Depois colocamos a imagem original no centro deste array, através do próximo comando.
    """ 
    arr[1:(width+1), 1:(height+1)] = img[0:width, 0:height] 

    # Começamos a percorrer o numpy array a partir do 1, pois o 0 é apenas o contorno.
    for j in range(1, height): # linhas: altura na imagem são as linhas (eixo y)
        for i in range(1, width): # colunas: largura na imagem são as colunas (eixo x)
            if(arr[j, i, 0] == 0): # Verificamos se o pixel é preto olhando o primeiro canal
                fila.append([j, i]) # Se for preto colocamos na fila First in First Out.
                arr[j, i, 0] = count # Marcamos o pixel atual como visitado, setando-o para count
                while (fila): # Enquanto a fila for diferente de vazio
                    pixel = fila.pop(0) # Retiramos o primeiro elemento (First in First Out).
                    lista_vizinhos = olha_vizinhos(pixel[0], pixel[1]) # Olhamos todos os vizinhos
                    for vizinho in lista_vizinhos: # Analisamos os vizinhos
                        y = vizinho[1]
                        x = vizinho[0]
                        if(arr[y, x, 0] == 0): # Se for preto, ou seja, não tiver marcado ainda
                            arr[y, x, 0] = count # Marcamos para que não seja analisado novamente
                            fila.append([y, x]) # E colocamos na fila
                count += 1 # Incrementamos count

    if(tarefa == "preto"):
        print("%d componentes conectados foram encontrados em spots.tif." %(count-1)) 
        # count-1, pois count já começa com valor 1
    elif(tarefa == "buracos"):
        print("%d buracos foram encontrados em spots.tif." %(count-2)) 
        """ count-2, pois:
        1 - A variável count já começa com valor 1;
        2 - O fundo branco vai ser contado como um componente conectado;
        OBS: Na antiga imagem spots.tif precisava fazer count-3, pois havia um pixel branco isolado.
        """

if __name__ == "__main__":
    main()

