import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
from Leyes_de_kepler import primera_ley_de_kepler, segunda_ley_de_kepler, tercera_ley_de_kepler
import math
from Grafico_y_tablas import graficar_orbita_tiempo, graficar_tercera_ley_kepler_sistema, simulacion_segunda_ley_tk
from tkinter import ttk
from datos_filtrados import sistemas_dict 
import random
from info_sistemas import obtener_info
from tkinter import filedialog
from tkinter import filedialog, messagebox
from Trivia import preguntas


#from dff import df_filtrado, sistemas_dict, sistemas, planetas
# Codigo para crear la ventana principal
ventana = tk.Tk()
ventana.title("Simulador de Sistemas")
ventana.geometry("800x600")
ventana.minsize(1366, 768)
#font = ("Orbitron", 12)
font = ("Quicksand", 12)

# Nombres estándar de columnas
nombres = ["Nombre del Planeta", "Estrella Anfitriona", "Periodo Orbital (días)",
           "Semieje Mayor (AU)", "Radio Planeta (RT)", "Masa Planeta (MT)", "Excentricidad"]

# Importamos la imagen de fondo
imagen = Image.open("fondo_generico.jpg")
fondo_label = tk.Label(ventana)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
fondo_label.lower()  # Envía el fondo detrás de los demás widgets
imagen_logo = Image.open("Logo Astrofisica-blanco.png")  #Ruta de logo astrofísica
imagen_redimensionada = imagen_logo.resize((210,60 ), Image.LANCZOS)
logo_tk = ImageTk.PhotoImage(imagen_redimensionada)
logo_label = tk.Label(ventana, image=logo_tk, bg="black", borderwidth=0)
logo_label.image = logo_tk
logo_label.place(relx=0.01, rely=0.99, anchor="sw")


ascii_art = """


✨ S I M U L A D O R   D E   S I S T E M A S  ✨
E X O P L A N E T A R I O S 
🪐 

"""

marco_titulo = tk.Frame(ventana, bg="black")
marco_titulo.place(relx=0.5, rely=0.08, anchor="center")

titulo_ascii = tk.Label(
    marco_titulo,
    text=ascii_art,
    font=("Orbitron", 18),
    bg="black",
    fg="#00d5ff",
    justify="center"
)
titulo_ascii.pack(padx=10, pady=5)

# Crea un label para la descripción
marco_descripcion = tk.Frame(ventana, bg="black")  # Fondo negro
marco_descripcion.place(relx=0.5, rely=0.27, anchor="center")
descripcion = (
    "Este software es un simulador de sistemas exoplanetarios con datos reales procedentes de NASA. "
    "Utilizando las leyes de Kepler, se han realizado animaciones de órbitas, exploración de tablas comparativas, interacciones "
    "con distintos cuerpos celestes y actividades que ayudan a la educación. También ofrece comparaciones con el Sistema Solar, facilitando el aprendizaje sobre "
    "el comportamiento dinámico de sistemas planetarios reales."
)
descripcion_label = tk.Label(marco_descripcion, text=descripcion, font=("Michroma",9), bg="black", fg="white")
descripcion_label.pack(padx=10, pady=6)
descripcion_label.config(wraplength=650)

###########################################
############ Carga de datos ###############
###########################################


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

#################################################


# Marco de sistemas y barra de búsqueda
marco_sistemas = tk.Frame(ventana, bg="black", bd=2, relief="groove")
marco_sistemas.place(relx=0.5, rely=0.65, anchor="center", relwidth=0.5, relheight=0.5)

marco_busqueda = tk.Frame(marco_sistemas, bg="black")
marco_busqueda.pack(fill=tk.X, padx=10, pady=(10, 0))
label_busqueda = tk.Label(marco_busqueda, text="Buscar sistema:", font=("Michroma",9), bg="black", fg="#00d5ff")
label_busqueda.pack(side=tk.LEFT, padx=(0, 5))
entry_busqueda = tk.Entry(marco_busqueda, font=("Orbitron",9), bg="black", fg="#00d5ff", insertbackground="#00d5ff", width=30)
entry_busqueda.pack(side=tk.LEFT, padx=(0, 10))

scrollbar = tk.Scrollbar(marco_sistemas)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_sistemas = tk.Listbox(marco_sistemas, font=("Michroma",8), bg="black", fg="white", selectbackground="#222244", selectforeground="white")

lista_sistemas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
scrollbar.config(command=lista_sistemas.yview)
lista_sistemas.config(yscrollcommand=scrollbar.set)

def filtrar_sistemas(event=None):
    filtro = entry_busqueda.get().lower()
    lista_sistemas.delete(0, tk.END)
    for sistema in sistemas:
        if filtro in sistema.lower():
            lista_sistemas.insert(tk.END, sistema)

entry_busqueda.bind("<KeyRelease>", filtrar_sistemas)
filtrar_sistemas()

##################################################################
############# Funciones para abrir ventanas de sistemas ##########
##################################################################

# Por cada sistema, se puede crear un botón que abra una nueva ventana con la información del sistema
# Pero cada pantalla sera unica para cada sistema, por lo que se puede crear una función que abra una nueva ventana con la información del sistema seleccionado
# Event sera una animacion unica del sistema seleccionado, por lo que se puede crear una función que abra una nueva ventana con la animación del sistema seleccionado


def abrir_sistema(event):
    """
    Abre una nueva ventana con la información del sistema seleccionado.
    """
    sistema_seleccionado = lista_sistemas.get(lista_sistemas.curselection())
    ventana_sistema = tk.Toplevel(ventana)
    ventana_sistema.title(f"Información del Sistema: {sistema_seleccionado}")
    ventana_sistema.minsize(700, 500)
    ventana_sistema.geometry("900x700")

    # Obtén los planetas del sistema seleccionado
    planetas_sistema = df_filtrado[df_filtrado["Estrella Anfitriona"] == sistema_seleccionado]
    num_planetas = len(planetas_sistema)

    # Define primer_planeta para usar en el botón
    if not planetas_sistema.empty:
        primer_planeta = planetas_sistema.iloc[0]["Nombre del Planeta"]
    else:
        primer_planeta = None

    # Estructura principal
    ventana_sistema.rowconfigure(0, weight=1)
    ventana_sistema.columnconfigure(0, weight=1)

    main_frame = tk.Frame(ventana_sistema)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)

    # Canvas de scroll
    canvas = tk.Canvas(main_frame)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame interno
    scrollable_frame = tk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.columnconfigure(0, weight=1)
    scrollable_frame.rowconfigure(0, weight=1)    # Descripción/tabla
    scrollable_frame.rowconfigure(1, weight=100)  # Simulación ocupa mucho espacio vertical

    def resize_scrollable(event):
        canvas.itemconfig(window_id, width=event.width)
    canvas.bind("<Configure>", resize_scrollable)
    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # --- Descripción y tabla ---
    marco_descripcion = tk.Frame(scrollable_frame, bg="black", bd=2, relief=tk.GROOVE)
    marco_descripcion.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    titulo_desc = tk.Label(
        marco_descripcion,
        text=f"⭐ Sistema: {sistema_seleccionado} | 🪐 Planetas: {num_planetas}",
        font=("Michroma", 12),
        bg="black",
        fg="#00d5ff",
        justify=tk.LEFT,
    )
    titulo_desc.pack(padx=10, pady=(10, 5), anchor="center")

    descripcion_sistema = obtener_info(sistema_seleccionado)
    label_desc = tk.Label(marco_descripcion, text=descripcion_sistema, font=("Michroma",9), bg="black", fg="white")
    label_desc.pack(padx=10, pady=(0, 10), anchor="center")

    # --- Tabla ---
    tree_frame = tk.Frame(marco_descripcion, bg="black")
    tree_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    tree_scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
    tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    columnas = list(planetas_sistema.columns)
    tree = ttk.Treeview(
        tree_frame,
        columns=columnas,
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set,
        style="Michroma.Treeview"
    )
    tree.pack(fill=tk.BOTH, expand=True)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for _, row in planetas_sistema.iterrows():
        valores = [row[col] for col in columnas]
        tree.insert("", tk.END, values=valores)

    # --- Simulación ---
    marco_simulacion = tk.Frame(scrollable_frame, bg="black", bd=2, relief=tk.GROOVE)
    marco_simulacion.grid(row=1, column=0, padx=1, pady=10, sticky="nsew")
    scrollable_frame.rowconfigure(1, weight=1)
    scrollable_frame.columnconfigure(0, weight=1)
    marco_simulacion.rowconfigure(1, weight=1)
    marco_simulacion.columnconfigure(0, weight=1)
    canvas_animacion = tk.Canvas(marco_simulacion, bg="black", height=500)
    canvas_animacion.grid(row=1, column=0, pady=10, sticky="nsew")  

    label_simulacion = tk.Label(
        marco_simulacion, text="Simulación del Sistema", font=("Michroma",8), bg="black", fg="#00d5ff"
    )
    label_simulacion.grid(row=0, column=0, sticky="ew")

    estrellas = []
    num_estrellas = 300  # Cantidad de estrellas a generar

    def inicializar_estrellas(canvas):

        nonlocal estrellas
        # Borrar estrellas previas
        for (estrella_id, _, _, _) in estrellas:
            canvas.delete(estrella_id)
        estrellas.clear()
        ancho = canvas.winfo_width()
        alto = canvas.winfo_height()
        if ancho < 2 or alto < 2:
            return
        for _ in range(num_estrellas):
            x = random.randint(0, ancho-1)
            y = random.randint(0, alto-1)
            tamaño = random.randint(1, 2)
            estrella_id = canvas.create_oval(x, y, x+tamaño, y+tamaño, fill="white", outline="")
            estrellas.append((estrella_id, x, y, tamaño))

    def on_canvas_resize(event):
        inicializar_estrellas(canvas_animacion)
        dibujar_orbitas(escala_actual)

    canvas_animacion.bind("<Configure>", on_canvas_resize)

    def animar_estrellas(canvas):
        #Función para que las estrellas parpadeen
        for i, (estrella_id, x, y, tamaño) in enumerate(estrellas):
            brillo = random.choice(["white", "gray90", "gray80","gray70", "gray60","gray50","gray40", "gray30"])
            canvas.itemconfig(estrella_id, fill=brillo)
        canvas.after(300, lambda: animar_estrellas(canvas))

    cx, cy = 450, 300  # Centro inicial, pero se recalcula dinámicamente

    planetas = planetas_sistema.reset_index(drop=True)
    max_a = planetas["Semieje Mayor (AU)"].max()
    radio_maximo = 350
    escala = radio_maximo / max_a
    escala_actual = escala

    planetas_canvas = []
    tiempos = []
    colores = ["blue", "green", "red", "orange", "cyan", "magenta","purple", "brown", "pink", "lime", "teal"]

    for i, (_, planeta) in enumerate(planetas.iterrows()):
        a = float(planeta["Semieje Mayor (AU)"])
        e = float(planeta["Excentricidad"])
        T = float(planeta["Periodo Orbital (días)"])
        tiempos.append(T * i / len(planetas))
        planeta_id = canvas_animacion.create_oval(0, 0, 0, 0, fill=colores[i % len(colores)])
        planetas_canvas.append((planeta_id, a, e, T))

    def dibujar_orbitas(escala_actual):
        canvas_animacion.delete("orbita")
        ancho = canvas_animacion.winfo_width()
        alto = canvas_animacion.winfo_height()
        centro_x = ancho // 2
        centro_y = alto // 2
        canvas_animacion.create_oval(
            centro_x - 10, centro_y - 10, centro_x + 10, centro_y + 10, fill="yellow", tags="orbita"
        )  # Estrella

        # Dibuja todas las órbitas completas (sin filtrar puntos)
        for i, (_, planeta) in enumerate(planetas.iterrows()):
            a = float(planeta["Semieje Mayor (AU)"])
            e = float(planeta["Excentricidad"])
            puntos = []
            for t in range(0, 360, 3):
                theta = math.radians(t)
                x, y = primera_ley_de_kepler(a, e, theta)
                x_canvas = centro_x + x * escala_actual
                y_canvas = centro_y + y * escala_actual
                puntos.append(x_canvas)
                puntos.append(y_canvas)
            canvas_animacion.create_line(
                puntos, fill=colores[i % len(colores)], width=1, smooth=True, tags="orbita"
            )

        # Actualiza la posición de los planetas
        for i, (planeta_id, a, e, T) in enumerate(planetas_canvas):
            x, y = segunda_ley_de_kepler(tiempos[i], a, e, T)
            x_canvas = centro_x + x * escala_actual
            y_canvas = centro_y + y * escala_actual
            canvas_animacion.coords(planeta_id, x_canvas - 7, y_canvas - 7, x_canvas + 7, y_canvas + 7)

    def animar():
        for i, (planeta_id, a, e, T) in enumerate(planetas_canvas):
            tiempos[i] += 0.1
            ancho = canvas_animacion.winfo_width()
            alto = canvas_animacion.winfo_height()
            centro_x = ancho // 2
            centro_y = alto // 2
            x, y = segunda_ley_de_kepler(tiempos[i], a, e, T)
            x_canvas = centro_x + x * escala_actual
            y_canvas = centro_y + y * escala_actual
            canvas_animacion.coords(planeta_id, x_canvas - 7, y_canvas - 7, x_canvas + 7, y_canvas + 7)
        canvas_animacion.after(50, animar)

    def on_mouse_wheel(event):
        nonlocal escala_actual
        if event.delta > 0:
            escala_actual *= 1.1
        else:
            escala_actual /= 1.1
        escala_actual = max(min(escala_actual, escala * 10), escala * 0.1)
        dibujar_orbitas(escala_actual)

    canvas_animacion.bind("<MouseWheel>", on_mouse_wheel)
    canvas_animacion.bind("<Button-4>", lambda e: on_mouse_wheel(type("Event", (object,), {"delta": 120})()))
    canvas_animacion.bind("<Button-5>", lambda e: on_mouse_wheel(type("Event", (object,), {"delta": -120})()))

    def iniciar_animacion_canvas():
        canvas_animacion.update_idletasks()
        canvas_animacion.update()
        if canvas_animacion.winfo_width() > 1 and canvas_animacion.winfo_height() > 1:
            inicializar_estrellas(canvas_animacion)
            animar_estrellas(canvas_animacion)
            dibujar_orbitas(escala_actual)
        else:
            canvas_animacion.after(100, iniciar_animacion_canvas)
    
    iniciar_animacion_canvas()
    dibujar_orbitas(escala_actual)
    animar()

    # --- Leyenda de planetas ---
    leyenda_frame = tk.Frame(scrollable_frame, bg="black")
    leyenda_frame.grid(row=2, column=0, pady=(0, 10), sticky="ew")
    scrollable_frame.rowconfigure(2, weight=0)

    for i, planeta in enumerate(planetas["Nombre del Planeta"]):
        color = colores[i % len(colores)]
        item = tk.Frame(leyenda_frame, bg="black")
        item.pack(side=tk.LEFT, padx=8)
        color_box = tk.Canvas(item, width=18, height=18, bg="black", highlightthickness=0)
        color_box.create_oval(2, 2, 16, 16, fill=color, outline=color)
        color_box.pack(side=tk.LEFT)
        label = tk.Label(item, text=planeta, font=("Orbitron",8), bg="black", fg="#00d5ff")
        label.pack(side=tk.LEFT, padx=(3, 0))

    # --- Frame para los botones ---
    frame_botones = tk.Frame(scrollable_frame, bg="black")
    frame_botones.grid(row=3, column=0, pady=10, sticky="ew")
    scrollable_frame.rowconfigure(3, weight=0)

    marco_botones = tk.Frame(frame_botones, bg="black")
    marco_botones.pack(side=tk.TOP, pady=(0, 5))

    boton_primera_ley = tk.Button(
        marco_botones,
        text="Primera Ley de Kepler",
        font=("Michroma",8),
        bg="black",
        fg="#00d5ff",
        command=lambda: graficar_orbita_tiempo(df_filtrado, primer_planeta)
    )
    boton_primera_ley.pack(side=tk.LEFT, padx=5)

    boton_segunda_ley = tk.Button(
        marco_botones,
        text="Segunda Ley de Kepler",
        font=("Michroma",8),
        bg="black",
        fg="#00d5ff",
        command=lambda: simulacion_segunda_ley_tk(sistema_seleccionado,df_filtrado  )
    )
    boton_segunda_ley.pack(side=tk.LEFT, padx=5)

    boton_tercera_ley = tk.Button(
        marco_botones,
        text="Tercera Ley de Kepler",
        font=("Michroma",8),
        bg="black",
        fg="#00d5ff",
        command=lambda: graficar_tercera_ley_kepler_sistema(
            {sistema_seleccionado: sistemas_dict[sistema_seleccionado]}
        )
    )
    boton_tercera_ley.pack(side=tk.LEFT, padx=5)

    boton_volver = tk.Button(frame_botones, text="Volver a la lista de sistemas",
                             font=("Orbitron"), bg="black", fg="#00d5ff", command=ventana_sistema.destroy)
    boton_volver.pack(side=tk.TOP, pady=(5, 0))

lista_sistemas.bind("<Double-Button-1>", abrir_sistema) # Llama a la función al hacer doble clic en un sistema de la lista

def actualizar_fondo():
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    imagen_redimensionada = imagen.resize((ancho, alto), Image.LANCZOS)
    fondo_img = ImageTk.PhotoImage(imagen_redimensionada)
    fondo_label.config(image=fondo_img)
    fondo_label.image = fondo_img  # Evita que la imagen se elimine por el recolector de basura

ventana.bind("<Configure>", lambda event: actualizar_fondo())



# Botón para cargar nueva data - MOVER ESTO ANTES DEL mainloop()
def cargar_nueva_data():
    """
    Carga nuevos datos y los combina con los existentes sin duplicados
    """
    messagebox.showinfo("Instrucciones",
        "El archivo debe ser un archivo.csv y debe tener la siguiente estructura para poder procesar los datos correctamente:\n\n"
        "🚀 Columnas requeridas\n\n"
        "1ra. Nombre del Planeta\n" \
        "2da. Estrella Anfitriona\n" \
        "3ra. Periodo Orbital (días)\n" \
        "4ta. Semieje Mayor (AU)\n" \
        "5ta. Radio Planeta (RT)\n" \
        "6ta. Masa Planeta (MT)\n" \
        "7ma. Excentricidad\n\n"
        "Asegúrate de que el archivo CSV no tenga filas vacías o comentarios que no comiencen con '#'.\n"
    )

    
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo CSV de sistemas exoplanetarios",
        filetypes=[("Archivos CSV", "*.csv")]
    )
    if not archivo:  
        return

    try:
        
        loading = tk.Label(ventana, text="🛰 Procesando datos...", 
                         font=("Orbitron", 10), bg="black", fg="#00d5ff")
        loading.place(relx=0.5, rely=0.37, anchor="center")
        ventana.update_idletasks()

        # Lee y valida el archivo
        nuevo_df = pd.read_csv(archivo, comment='#', sep=',')
        columnas_requeridas = ["Nombre del Planeta", "Estrella Anfitriona", 
                             "Periodo Orbital (días)", "Semieje Mayor (AU)"]
        
        if not all(col in nuevo_df.columns for col in columnas_requeridas):
            messagebox.showerror("Error", "❌ El archivo no tiene las columnas requeridas")
            return

        nuevo_df.columns = nombres[:len(nuevo_df.columns)]
        nuevo_df = nuevo_df.dropna()

        # Combinar con datos existentes
        global df_filtrado, sistemas, sistemas_dict
        df_filtrado = pd.concat([df_filtrado, nuevo_df]).drop_duplicates(
            subset=["Nombre del Planeta", "Estrella Anfitriona"]
        ).reset_index(drop=True)

        # Actualizar lista de sistemas y el diccionario
        sistemas = df_filtrado["Estrella Anfitriona"].unique().tolist()
        
        sistemas_dict = {}
        for sistema in sistemas:
            planetas_sistema = df_filtrado[df_filtrado["Estrella Anfitriona"] == sistema]
            sistemas_dict[sistema] = planetas_sistema[["Nombre del Planeta", "Periodo Orbital (días)", "Semieje Mayor (AU)"]].values.tolist()
        
        filtrar_sistemas()

        # Confirmación
        success = tk.Label(ventana, text="✅ Datos agregados exitosamente", 
                         font=("Orbitron", 10), bg="green", fg="#f5f5f5")
        success.place(relx=0.5, rely=0.37, anchor="center")
        ventana.after(3000, success.destroy)

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar:\n{str(e)}")
    finally:
        loading.destroy() if 'loading' in locals() else None

boton_cargar_data = tk.Button(
    ventana,
    text="📤 Subir nuevos sistemas exoplanetarios 📤 ",
    font=("Orbitron", 10),
    bg="black",
    fg="#00d5ff",
    command=cargar_nueva_data 
)
boton_cargar_data.place(relx=0.5, rely=0.95, anchor="center")

def trivia_escolar_tk():
    # Crea una ventana emergente para la trivia
    trivia_win = tk.Toplevel(ventana)
    trivia_win.title("Trivia: Leyes de Kepler")
    trivia_win.geometry("500x400")
    trivia_win.resizable(False, False)

    # Frame para la pregunta y opciones
    frame = tk.Frame(trivia_win, bg="white")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Variables para el estado de la trivia
    preguntas_copia = preguntas.copy()
    random.shuffle(preguntas_copia)
    puntaje = [0]
    idx = [0]

    pregunta_var = tk.StringVar()
    explicacion_var = tk.StringVar()
    seleccion = tk.StringVar()
    seleccion.set(None)  

    def mostrar_pregunta():
        if idx[0] < len(preguntas_copia):
            p = preguntas_copia[idx[0]]
            pregunta_var.set(f"Pregunta {idx[0]+1}: {p['pregunta']}")
            for i, op in enumerate(p['opciones']):
                botones[i].config(text=op, value=op[0])
            explicacion_var.set("")
            seleccion.set(None)
        else:
            pregunta_var.set(f"Resultado: {puntaje[0]}/{len(preguntas_copia)} correctas")
            for b in botones:
                b.pack_forget()
            if puntaje[0] == len(preguntas_copia):
                explicacion_var.set("¡Felicidades! Has respondido todas las preguntas correctamente.")
            elif puntaje[0] >= 5:
                explicacion_var.set("¡Excelente comprensión de las Leyes de Kepler!")
            elif puntaje[0] >= 3:
                explicacion_var.set("¡Buen trabajo! Sigue practicando.")
            else:
                explicacion_var.set("¡Revísalas nuevamente! Recuerda las Leyes de Kepler")

    def responder():
        p = preguntas_copia[idx[0]]
        if seleccion.get() == p['respuesta']:
            explicacion_var.set(f"☆⋆ CORRECTO, {p['explicacion']}")
            puntaje[0] += 1
        else:
            explicacion_var.set(f"𝔁 INCORRECTO. La correcta es [{p['respuesta'].upper()}], {p['explicacion']}")
        idx[0] += 1
        trivia_win.after(1500, mostrar_pregunta)

    # Widgets
    pregunta_lbl = tk.Label(frame, textvariable=pregunta_var, font=("Orbitron",10), bg="white", wraplength=450, justify="left")
    pregunta_lbl.pack(pady=(10, 10), anchor="w")

    botones = []
    for i, letra in enumerate(["a", "b", "c", "d"]):
        b = tk.Radiobutton(
            frame,
            text="",
            variable=seleccion,
            value=letra,
            font=("Orbitron",10),
            bg="white",
            anchor="w",
            command=responder
        )
        b.pack(anchor="w", pady=2)
        botones.append(b)

    explicacion_lbl = tk.Label(frame, textvariable=explicacion_var, font=font, bg="white", fg="blue", wraplength=450, justify="left")
    explicacion_lbl.pack(pady=(10, 0), anchor="w")

    mostrar_pregunta()

# --- Botón para abrir la trivia en la esquina superior derecha ---
btn_trivia = tk.Button(ventana, text="🎲 ¡Trivia Kepler!", font=("Orbitron",10), bg="#000000", fg="#ffffff", command=trivia_escolar_tk)
btn_trivia.place(relx=0.98, rely=0.98, anchor="se")  # Esquina superior derecha
lista_sistemas.bind("<Double-Button-1>", abrir_sistema) # Llama a la función al hacer doble clic en un sistema de la lista

# Actualizar el fondo al iniciar
actualizar_fondo()
ventana.mainloop() # Inicia el bucle principal de la ventana

