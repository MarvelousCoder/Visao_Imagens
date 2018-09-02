import numpy as np

def calc_dist(atualX, atualY, destX, destY):
    listDistancias = [0, 0, 0, 0, 0, 0, 0, 0]

    sudoeste = np.sqrt( (destX - (atualX-1))**2 + (destY - (atualY+1))**2 )

    sul = np.sqrt( (destX - (atualX))**2 + (destY - (atualY+1))**2 )

    sudeste = np.sqrt( (destX - (atualX+1))**2 + (destY - (atualY+1))**2 )

    oeste = np.sqrt( (destX - (atualX-1))**2 + (destY - (atualY))**2 )

    leste = np.sqrt( (destX - (atualX+1))**2 + (destY - (atualY))**2 )

    noroeste = np.sqrt( (destX - (atualX-1))**2 + (destY - (atualY-1))**2 )

    norte = np.sqrt( (destX - (atualX))**2 + (destY - (atualY-1))**2 )

    nordeste = np.sqrt( (destX - (atualX+1))**2 + (destY - (atualY-1))**2 )

    listDistancias[0] = [sudoeste, atualX-1, atualY+1]
    listDistancias[1] = [sul, atualX, atualY+1]
    listDistancias[2] = [sudeste, atualX+1, atualY+1]
    listDistancias[4] = [leste, atualX+1, atualY]
    listDistancias[7] = [nordeste, atualX+1, atualY-1]
    listDistancias[6] = [norte, atualX, atualY-1]
    listDistancias[5] = [noroeste, atualX-1, atualY-1]
    listDistancias[3] = [oeste, atualX-1, atualY]

    return listDistancias