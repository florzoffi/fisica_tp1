import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar el archivo Excel con las mediciones
archivo_excel = 'estudio_aceleraciones_M110_mesa.xlsx'
df = pd.read_excel(archivo_excel)

# Define la fórmula de conversión basada en tu calibración previa
def conversion_formula(x):
    return 0.0185 * x - 1.6121

# Función para calcular la incertidumbre en la distancia usando los errores del ajuste lineal
def incertidumbre_distancia(valor_sensor, incertidumbre_a, incertidumbre_b):
    return np.sqrt((valor_sensor * incertidumbre_a) ** 2 + incertidumbre_b ** 2)

# Valores de las incertidumbres del ajuste lineal (obtenidas previamente)
incertidumbre_a = 0.0004  # Reemplaza con la incertidumbre real de 'a' que calculaste
incertidumbre_b = 0.6575  # Reemplaza con la incertidumbre real de 'b' que calculaste

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
            
            # Cálculo de la velocidad usando diferencias finitas
            tiempos = [punto[0] for punto in datos_experimentales]
            distancias = [punto[1] for punto in datos_experimentales]
            
            # Ajuste lineal para obtener la aceleración constante
            coeficientes_velocidad = np.polyfit(tiempos, distancias, 2)  # Polinomio de grado 2 para MRUV
            aceleracion_constante = 2 * coeficientes_velocidad[0]  # a(t) = 2 * coef. cuadrático
            
            aceleraciones_vs_m.append((m_actual, aceleracion_constante))
            aceleraciones_vs_M.append((M_actual, aceleracion_constante))
            
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
    
    # Cálculo de la velocidad usando diferencias finitas
    tiempos = [punto[0] for punto in datos_experimentales]
    distancias = [punto[1] for punto in datos_experimentales]
    
    # Ajuste lineal para obtener la aceleración constante
    coeficientes_velocidad = np.polyfit(tiempos, distancias, 2)  # Polinomio de grado 2 para MRUV
    aceleracion_constante = 2 * coeficientes_velocidad[0]  # a(t) = 2 * coef. cuadrático
    
    aceleraciones_vs_m.append((m_actual, aceleracion_constante))
    aceleraciones_vs_M.append((M_actual, aceleracion_constante))

# Separar las listas para graficar
m_vals, aceleracion_m_vals = zip(*aceleraciones_vs_m)
M_vals, aceleracion_M_vals = zip(*aceleraciones_vs_M)

# Gráfico de todos los m vs aceleración
plt.figure(figsize=(8, 6))
plt.scatter(aceleracion_m_vals, m_vals, color='b', marker='o')
plt.xlabel('Aceleración [cm/ms^2]')
plt.ylabel('m (g)')
plt.title('Aceleración vs m (todos los experimentos)')
plt.grid(True)
plt.show()

# Gráfico de todos los M vs aceleración
plt.figure(figsize=(8, 6))
plt.scatter(aceleracion_M_vals, M_vals, color='r', marker='o')
plt.xlabel('Aceleración [cm/ms^2]')
plt.ylabel('M (g)')
plt.title('Aceleración vs M (todos los experimentos)')
plt.grid(True)
plt.show()
