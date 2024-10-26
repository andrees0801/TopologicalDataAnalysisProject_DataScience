import matplotlib.pyplot as plt

def mostrar_en_grid(imagenes, filas, columnas, tamano_figura=(10, 10)):
    fig, axs = plt.subplots(filas, columnas, figsize=tamano_figura)
    axs = axs.ravel()
    
    for i, imagen in enumerate(imagenes):
        axs[i].imshow(imagen)
        axs[i].axis('off')

    plt.tight_layout()
    plt.show()