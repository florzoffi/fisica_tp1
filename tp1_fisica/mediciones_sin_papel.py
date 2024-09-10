import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar el archivo Excel con las mediciones
archivo_excel = 'mediciones_sin_papel.xlsx'
df = pd.read_excel(archivo_excel)

# Define la fórmula de conversión basada en tu calibración previa
def conversion_formula(x):
    return 0.0185 * x - 1.6121

# Función para calcular la incertidumbre en la distancia usando los errores del ajuste lineal
def incertidumbre_distancia(valor_sensor, incertidumbre_a, incertidumbre_b):
    return np.sqrt((valor_sensor * incertidumbre_a) ** 2 + incertidumbre_b ** 2)

# Valores de las incertidumbres del ajuste lineal (obtenidas previamente)
incertidumbre_a = 0.0004  # Reemplaza con la incertidumbre real de 'a' que calculaste
incertidumbre_b = 0.6575    # Reemplaza con la incertidumbre real de 'b' que calculaste

# Inicializar variables
experimentos = []
datos_experimentales = []
aceleraciones_vs_m = []
aceleraciones_vs_M = []
m_actual = None
M_actual = None

# Asumimos que las columnas son correctas
columna_etiqueta = 'm'
columna_M = 'M'
columna_datos = 't, arduino'

for _, row in df.iterrows():
    etiqueta = row[columna_etiqueta]
    etiqueta_M = row[columna_M]
    
    if pd.notna(etiqueta) or pd.notna(etiqueta_M):
        if datos_experimentales:
            experimentos.append((m_actual, M_actual, datos_experimentales))
            velocidad = np.gradient([punto[1] for punto in datos_experimentales], [punto[0] for punto in datos_experimentales])
            aceleracion = np.gradient(velocidad, [punto[0] for punto in datos_experimentales])
            aceleracion_media = np.mean(aceleracion)
            
            aceleraciones_vs_m.append((m_actual, aceleracion_media))
            aceleraciones_vs_M.append((M_actual, aceleracion_media))
            
            datos_experimentales = []
        
        m_actual = etiqueta if pd.notna(etiqueta) else m_actual
        M_actual = etiqueta_M if pd.notna(etiqueta_M) else M_actual
    
    datos = row[columna_datos]
    if pd.notna(datos):
        try:
            valor1, valor2 = map(lambda x: float(x.replace(',', '.')), datos.split(','))
            distancia = conversion_formula(valor2)
            error_distancia = incertidumbre_distancia(valor2, incertidumbre_a, incertidumbre_b)
            datos_experimentales.append((valor1, distancia, error_distancia))
        except ValueError:
            print(f"Error al procesar los datos: {datos}")

# Asegurarse de agregar el último experimento si existen datos
if datos_experimentales:
    experimentos.append((m_actual, M_actual, datos_experimentales))
    velocidad = np.gradient([punto[1] for punto in datos_experimentales], [punto[0] for punto in datos_experimentales])
    aceleracion = np.gradient(velocidad, [punto[0] for punto in datos_experimentales])
    aceleracion_media = np.mean(aceleracion)
    
    aceleraciones_vs_m.append((m_actual, aceleracion_media))
    aceleraciones_vs_M.append((M_actual, aceleracion_media))

# Graficar cada experimento con barras de error
if experimentos:
    for i, (m, M, exp) in enumerate(experimentos):
        t = [punto[0] for punto in exp]
        distancia = [punto[1] for punto in exp]
        error_distancia = [punto[2] for punto in exp]

        velocidad = np.gradient(distancia, t)
        aceleracion = np.gradient(velocidad, t)
        
        plt.figure(figsize=(8, 6))
        plt.errorbar(t, distancia, yerr=error_distancia, fmt='o', color='b', ecolor='r', capsize=5, label=f'Experimento {i + 1}')
        plt.xlabel('Tiempo (ms)')
        plt.ylabel('Distancia calculada (cm)')
        plt.title(f'Gráfico de Distancia vs Tiempo - Experimento {i + 1}')
        plt.legend()
        plt.grid(True)
        plt.show()