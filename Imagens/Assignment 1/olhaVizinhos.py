def olhaVizinhos(y, x):
    listaVizinhos = [0, 0, 0, 0, 0, 0, 0, 0]

    listaVizinhos[0] = [x+1, y]
    listaVizinhos[1] = [x+1, y-1]
    listaVizinhos[2] = [x, y-1]
    listaVizinhos[3] = [x-1, y-1]
    listaVizinhos[4] = [x-1, y]
    listaVizinhos[5] = [x-1,y+1]
    listaVizinhos[6] = [x, y+1]
    listaVizinhos[7] = [x+1,y+1]

    return listaVizinhos