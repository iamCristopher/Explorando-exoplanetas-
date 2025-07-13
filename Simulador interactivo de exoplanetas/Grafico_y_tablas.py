import pandas as pd
import tkinter as tk
import math 
import numpy as np
import matplotlib.pyplot as plt
from datos_filtrados import sistemas_dict
from Leyes_de_kepler import tercera_ley_de_kepler
import tkinter as tk
from Leyes_de_kepler import segunda_ley_de_kepler,  primera_ley_de_kepler,resolver_E, obtener_theta
from tkinter import messagebox
import traceback
from pandas import DataFrame


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


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


#funcion para calcular el radio usando la segunda ley
def calcular_radio_orbital(t, a, e, T):
    """Usa la segunda ley para obtener solo el radio"""
    x, y = segunda_ley_de_kepler(t, a, e, T)  # obtiene las posiciones
    return math.sqrt(x**2 + y**2)  # Calcula r a partir de x,y


def graficar_orbita_tiempo(df, nombre_planeta):
    planeta = df[df["Nombre del Planeta"] == nombre_planeta].iloc[0]
    a = planeta["Semieje Mayor (AU)"]
    e = planeta["Excentricidad"]
    T = planeta["Periodo Orbital (días)"]

    t = np.linspace(0, 2 * T, 1000)
    r = [calcular_radio_orbital(ti, a, e, T) for ti in t]  # ← Usa la nueva función
    
    plt.figure(figsize=(10, 5))
    plt.plot(t, r, label="Órbita real")
    plt.hlines(a, t[0], t[-1], linestyle="--", color="gray", label="Órbita circular")
    plt.xlabel("Tiempo (días)")
    plt.ylabel("Radio orbital (AU)")
    plt.title(f"Radio orbital vs Tiempo para {nombre_planeta}")
    plt.legend()
    plt.grid(True)
    plt.show()

#segunda ley supuestamente para cualquer sistema 

def simulacion_segunda_ley_tk(sistema_seleccionado, df_filtrado):
    try:
        # Verificación inicial 
        if sistema_seleccionado not in df_filtrado["Estrella Anfitriona"].values:
            messagebox.showerror("Error", f"Sistema {sistema_seleccionado} no encontrado")
            return

        planetas_sistema = df_filtrado[df_filtrado["Estrella Anfitriona"] == sistema_seleccionado]
        
        if len(planetas_sistema) == 0:
            messagebox.showerror("Error", f"No hay planetas en {sistema_seleccionado}")
            return

        primer_planeta = planetas_sistema.iloc[0]
        nombre_planeta = primer_planeta["Nombre del Planeta"]
        
        # Validación de los datos del sistema correctos 
        try:
            a = float(primer_planeta["Semieje Mayor (AU)"])
            e = float(primer_planeta["Excentricidad"])
            T = float(primer_planeta["Periodo Orbital (días)"])
        except (ValueError, KeyError) as ve:
            messagebox.showerror("Error", f"Datos orbitales inválidos: {ve}")
            return

        if a <= 0 or T <= 0 or not (0 <= e < 1):
            messagebox.showerror("Error", f"Parámetros orbitales inválidos: a={a}, e={e}, T={T}")
            return

        # Configuración segura de la simulación
        pasos = 24
        intervalo_tiempo = max(T / pasos, 0.1)
        
        # Cálculo de posiciones
        posiciones = []
        for i in range(pasos + 1):
            t = i * intervalo_tiempo
            try:
                M = 2 * math.pi * (t / T) % (2 * math.pi)
                E = resolver_E(M, e)
                theta = obtener_theta(E, e)
                x, y = primera_ley_de_kepler(a, e, theta)
                posiciones.append((x, y))
            except:
                theta = 2 * math.pi * (t / T)
                posiciones.append((a * math.cos(theta), a * math.sin(theta)))

        # Configuración de la ventana
        win = tk.Toplevel()
        win.title(f"Segunda Ley de Kepler - {nombre_planeta}")
        win.geometry("500x550")
        
        frame_canvas = tk.Frame(win)
        frame_canvas.pack(padx=10, pady=(10, 0))
        canvas = tk.Canvas(frame_canvas, bg="black", width=400, height=400)
        canvas.pack()

        texto = tk.Label(win, text="", font=("Arial", 12), bg="white")
        texto.pack(pady=(10, 10))

        # Dibujo de la órbita
        cx, cy = 200, 200
        escala = 150 / (a * (1 + e)) if (a * (1 + e)) != 0 else 100
        
        puntos_orbita = []
        for ang in np.linspace(0, 2 * math.pi, 400):
            try:
                r = a * (1 - e**2) / (1 + e * math.cos(ang))
                x = cx + r * math.cos(ang) * escala
                y = cy + r * math.sin(ang) * escala
                puntos_orbita.append((x, y))
            except:
                continue

        for i in range(len(puntos_orbita) - 1):
            canvas.create_line(*puntos_orbita[i], *puntos_orbita[i+1], fill="white")

        canvas.create_oval(cx-8, cy-8, cx+8, cy+8, fill="yellow", outline="yellow")
        planeta = canvas.create_oval(0, 0, 0, 0, fill="cyan", outline="cyan")
        area_barrida = None

        # Cálculo de áreas
        areas = []
        for i in range(1, len(posiciones)):
            try:
                x0, y0 = posiciones[i-1]
                x1, y1 = posiciones[i]
                areas.append(0.5 * abs(x0 * y1 - x1 * y0))
            except:
                areas.append(0)

        # la Animación 
        paso_actual = 0
        def animar():
            nonlocal paso_actual, area_barrida
            
            if area_barrida:
                canvas.delete(area_barrida)
            
            if len(posiciones) < 2 or paso_actual >= len(posiciones):
                paso_actual = 0
                win.after(800, animar)
                return

            coords = [cx, cy]
            for i in range(min(paso_actual + 1, len(posiciones))):
                x, y = posiciones[i]
                coords.extend([cx + x * escala, cy + y * escala])
            
            area_barrida = canvas.create_polygon(coords, fill="orange", outline="orange", stipple="gray25")
            
            idx = paso_actual % len(posiciones)
            x, y = posiciones[idx]
            canvas.coords(planeta, 
                         cx + x * escala - 7, 
                         cy + y * escala - 7, 
                         cx + x * escala + 7, 
                         cy + y * escala + 7)

            texto.config(text=f"Tiempo: {paso_actual * intervalo_tiempo:.1f} días | Área: {areas[paso_actual % len(areas)]:.6f} AU²")
            
            paso_actual += 1
            win.after(800, animar)

        animar()

    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        print(f"Error completo: {traceback.format_exc()}")

def graficar_tercera_ley_kepler_sistema(sistemas_dict):
    """
    Grafica la Tercera Ley de Kepler para los planetas del sistema (o sistemas) que le pases.
    Recibe un diccionario: {estrella: [[nombre, periodo, semieje], ...]}
    Los colores de los planetas coinciden con los del simulador.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Colores igual que en el simulador
    colores = ["blue", "green", "red", "orange", "cyan", "magenta","purple", "brown", "pink", "lime", "teal"]

    nombres = []
    a = []
    T = []
    planet_colors = []
    constantes = []

    for estrella, planetas in sistemas_dict.items():
        for i, planeta_info in enumerate(planetas):
            nombres.append(planeta_info[0])
            T_val = float(planeta_info[1])
            a_val = float(planeta_info[2])
            T.append(T_val)
            a.append(a_val)
            planet_colors.append(colores[i % len(colores)])
            # Constante de la tercera ley para cada planeta: T^2 / a^3
            constantes.append(T_val**2 / a_val**3 if a_val != 0 else float('nan'))

    a = np.array(a)
    T = np.array(T)

    plt.figure(figsize=(8, 5))
    handles = []
    legend_labels = []
    for i, nombre in enumerate(nombres):
        sc = plt.scatter(np.log10(a[i]), np.log10(T[i]), color=planet_colors[i], s=60)
        handles.append(sc)
        legend_labels.append(f"{nombre} (K={constantes[i]:.3f})")

    plt.xlabel("log Semieje Mayor (AU)")
    plt.ylabel("log Período Orbital (días)")
    plt.title("Tercera Ley de Kepler para planetas del sistema")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(handles, legend_labels, loc="best", fontsize=8)
    plt.tight_layout()
    plt.show()

