import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# Cargar el archivo Excel
archivo_excel = 'calibrate.xlsx'  # Reemplaza con la ruta a tu archivo Excel
df = pd.read_excel(archivo_excel)

# Asumimos que el archivo tiene dos columnas
distancias = df.iloc[:, 0].tolist()  # Primera columna
distancias.pop()
valores = df.iloc[:, 1].tolist()     # Segunda columna
valores.pop()

# Definir el error en distancias (±0.1 cm)
error_distancias = [0.1] * len(distancias)  # Error en las distancias (±0.1 cm)

# Imprimir las listas
print("Distancias:", distancias)
print("Valores:", valores)

# Definir una función lineal para el ajuste
def modelo_lineal(x, a, b):
    return a * x + b

# Ajustar la curva a los datos
popt, pcov = curve_fit(modelo_lineal, valores, distancias)

# Parámetros optimizados
a_opt, b_opt = popt
print(f"Parámetros optimizados: a = {a_opt}, b = {b_opt}")

# Crear una serie de valores ajustados para la gráfica
valores_fit = np.linspace(min(valores), max(valores), 100)
distancias_fit = modelo_lineal(valores_fit, a_opt, b_opt)

# Crear el gráfico con barras de error y la curva ajustada
plt.figure(figsize=(8, 6))
plt.errorbar(valores, distancias, yerr=error_distancias, fmt='o', color='b', ecolor='r', capsize=5, label='Datos experimentales', markersize=3)
plt.plot(valores_fit, distancias_fit, 'g--', label=f'Ajuste lineal: y = {a_opt:.4f}x + {b_opt:.4f}')

# Añadir etiquetas y título
plt.xlabel('Valores Arduino')
plt.ylabel('Distancias (cm)')
plt.title('Gráfico de Distancias vs Arduino con Ajuste Lineal')
plt.legend()

# Mostrar la gráfica
plt.grid(True)
plt.show()

# Propagación de la incertidumbre (para la fórmula y = a*x + b)
def incertidumbre_distancia(valor, incertidumbre_a, incertidumbre_b):
    return np.sqrt((valor * incertidumbre_a)**2 + (incertidumbre_b)**2)

# Obtener las incertidumbres de los parámetros (desviaciones estándar)
incertidumbre_a = np.sqrt(pcov[0, 0])
incertidumbre_b = np.sqrt(pcov[1, 1])

# Reportar pendiente y ordenada del origen con sus incertezas
print(f"Pendiente (a) = {a_opt:.4f} ± {incertidumbre_a:.4f}")
print(f"Ordenada al origen (b) = {b_opt:.4f} ± {incertidumbre_b:.4f}")

# Valor del sensor
valor_sensor = 876

# Conversión a distancia
distancia_calculada = modelo_lineal(valor_sensor, a_opt, b_opt)

print(f"Para un valor de {valor_sensor} U.A., la distancia es {distancia_calculada:.2f} cm ± {incertidumbre_distancia(valor_sensor, incertidumbre_a, incertidumbre_b):.2f} cm")
