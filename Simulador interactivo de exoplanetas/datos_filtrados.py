import pandas as pd
import tkinter as tk
import math 

#leer archivo ( pd.read_csv),
#El archivo tiene comentarios que comienzan con '#', así que los omitimos
#hay que poner una separacion (sep) tabulación ('\t')

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
#pd.reset_option('display.max_rows')
#pd.reset_option('display.max_columns')

# Leer archivo
df = pd.read_csv("catalogo_exoplanet_filtrado.csv", comment='#', sep=',')
#print(df.head()) #eso lee las primeras lineas del archivo 

# Eliminar filas con algún NaN
df_filtrado = df.dropna()

# Cambiar los nombres de las columnas
nombres = ["Nombre del Planeta", "Estrella Anfitriona", "Periodo Orbital (días)", 
           "Semieje Mayor (AU)", "Radio Planeta (RT)", "Masa Planeta (MT)", "Excentricidad"]
df_filtrado.columns = nombres

# Resetear índices
df_filtrado = df_filtrado.reset_index(drop=True)

# Obtener sistemas únicos
sistemas = df_filtrado["Estrella Anfitriona"].unique().tolist()

# Crear un diccionario agrupado por estrella anfitriona
sistemas_dict = {}

for _, fila in df_filtrado.iterrows():
    estrella = fila["Estrella Anfitriona"]
    planeta_info = [fila["Nombre del Planeta"], fila["Periodo Orbital (días)"], fila["Semieje Mayor (AU)"]]
    
    if estrella not in sistemas_dict:
        sistemas_dict[estrella] = []
    
    sistemas_dict[estrella].append(planeta_info)

# Convertir a lista de listas
sistemas_lista = [[estrella, planetas] for estrella, planetas in sistemas_dict.items()]
