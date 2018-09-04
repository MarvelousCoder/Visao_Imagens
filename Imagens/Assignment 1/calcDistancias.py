import numpy as np
""" 
Os pixels vizinhos são definidos conforme slide 66 do Tópico 2.
Para um pixel p temos:
[ (x-1, y-1); (x, y-1); (x+1, y-1) ]
[ (x-1, y);   p;        (x+1, y)   ]
[ (x-1, y+1); (x, y+1); (x+1,y+1)  ]

Os vizinhos em relação a p são denotados como: 
sudoeste, sul, sudeste, leste, nordeste, norte, noroeste e oeste.
Aqui temos uma lista de listas listDistancias, onde cada elemento de listDistancias é uma lista xi, 
onde i varia de 0 até 7.
Cada uma das 8 listas xi contém o a distância do pixel x até o destino, além das coordenadas de x
em relação à p (ponto atual). 
"""

def calcDist(atualX, atualY, destX, destY):
    listDistancias = [0, 0, 0, 0, 0, 0, 0, 0]

    sudoeste = np.sqrt( (destX - (atualX-1))**2 + (destY - (atualY+1))**2 )

    sul = np.sqrt( (destX - (atualX))**2 + (destY - (atualY+1))**2 )

    sudeste = np.sqrt( (destX - (atualX+1))**2 + (destY - (atualY+1))**2 )

    leste = np.sqrt( (destX - (atualX+1))**2 + (destY - (atualY))**2 )

    nordeste = np.sqrt( (destX - (atualX+1))**2 + (destY - (atualY-1))**2 )

    norte = np.sqrt( (destX - (atualX))**2 + (destY - (atualY-1))**2 )

    noroeste = np.sqrt( (destX - (atualX-1))**2 + (destY - (atualY-1))**2 )

    oeste = np.sqrt( (destX - (atualX-1))**2 + (destY - (atualY))**2 )

    listDistancias[0] = [sudoeste, atualX-1, atualY+1]
    listDistancias[1] = [sul, atualX, atualY+1]
    listDistancias[2] = [sudeste, atualX+1, atualY+1]
    listDistancias[4] = [leste, atualX+1, atualY]
    listDistancias[7] = [nordeste, atualX+1, atualY-1]
    listDistancias[6] = [norte, atualX, atualY-1]
    listDistancias[5] = [noroeste, atualX-1, atualY-1]
    listDistancias[3] = [oeste, atualX-1, atualY]

    return listDistancias