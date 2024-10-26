from scipy.ndimage import label
import numpy as np

def betti_numeros(bin_matriz):
    # Invert the matrix to find the white components
    inverted_matriz = 1 - bin_matriz

    # Definir una estructura de conectividad personalizada
    structure = np.array([[1, 1, 1],
                    [1, 1, 1],
                    [1, 1, 1]])

    # Obtenemos las regiones encontradas en la matriz binaria
    ciclos_matriz, num_hoyos = label(inverted_matriz, structure=structure)
    beta1 = num_hoyos
    return beta1, ciclos_matriz