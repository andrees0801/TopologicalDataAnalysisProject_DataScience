import openslide
import numpy as np

def abrir_svs(svs_file_path):
    try:
        slide = openslide.OpenSlide(svs_file_path)
    except Exception as e:
        print(f"Error al abrir el archivo {svs_file_path}: {e}")
        return None
    return slide

def mostrar_niveles(slide):
    level_count = slide.level_count
    print(f'Niveles de resolución disponibles: {level_count}')
    for level in range(level_count):
        print(f'Nivel {level}: {slide.level_dimensions[level]}')
    return level_count

def region_wsi(level, x, y, region_width, region_height, slide):
    width, height = slide.dimensions
    # Verifica que las coordenadas y el tamaño de la región sean válidos
    if x + region_width > width or y + region_height > height:
        raise ValueError("La región especificada está fuera de los límites de la imagen.")
    # Extrae la región
    region = slide.read_region((x, y), level, (region_width, region_height))
    # Convierte la región a un formato que se pueda mostrar con PIL
    region = region.convert("L")
    return region

def procesar_imagenes(svs_file_paths, coordenadas, niveles, tamanio):
    regiones_wsi = []
    for svs_file_path, (coords, tam, levels) in zip(svs_file_paths, zip(coordenadas, tamanio, niveles)):
        slide = abrir_svs(svs_file_path)
        if slide is None:
            continue
        
        mostrar_niveles(slide)

        for (x_init, y_init), (region_width, region_height), level in zip(coords, tam, levels):
            region = region_wsi(level, x_init, y_init, region_width, region_height, slide)
            if x_init != 0 and y_init != 0:
                regiones_wsi.append(region)
            # plt.imshow(region)
            # plt.axis('off')
            # plt.show()
        slide.close()
    return regiones_wsi

def convertir_y_binarizar(regiones, umbral):
    regiones_binarizadas = []
    
    for region in regiones:
        region_gris = np.array(region)
        m, n = region_gris.shape
        for t in range(umbral):
            region_binarizada = np.zeros((m, n), dtype=int)
            for i in range(m):
                for j in range(n):
                    if region_gris[i, j] < t:
                        region_binarizada[i, j] = 0
                        # Incluir las esquinas y lados
                        if i > 0: region_binarizada[i-1, j] = 0
                        if i < m-1: region_binarizada[i+1, j] = 0
                        if j > 0: region_binarizada[i, j-1] = 0
                        if j < n-1: region_binarizada[i, j+1] = 0
                        if i > 0 and j > 0: region_binarizada[i-1, j-1] = 0
                        if i > 0 and j < n-1: region_binarizada[i-1, j+1] = 0
                        if i < m-1 and j > 0: region_binarizada[i+1, j-1] = 0
                        if i < m-1 and j < n-1: region_binarizada[i+1, j+1] = 0
                    else:
                        region_binarizada[i, j] = 1
            # Agregar a la lista de regiones binarizadas
            regiones_binarizadas.append(region_binarizada)
    return regiones_binarizadas