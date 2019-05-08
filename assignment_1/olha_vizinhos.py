def olha_vizinhos(y, x):
    lista_vizinhos = [0, 0, 0, 0, 0, 0, 0, 0]

    lista_vizinhos[0] = [x+1, y]
    lista_vizinhos[1] = [x+1, y-1]
    lista_vizinhos[2] = [x, y-1]
    lista_vizinhos[3] = [x-1, y-1]
    lista_vizinhos[4] = [x-1, y]
    lista_vizinhos[5] = [x-1,y+1]
    lista_vizinhos[6] = [x, y+1]
    lista_vizinhos[7] = [x+1,y+1]

    return lista_vizinhos