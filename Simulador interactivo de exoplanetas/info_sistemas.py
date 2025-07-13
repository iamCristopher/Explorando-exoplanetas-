sistemas_exoplanetarios_info = {
    "EPIC 249893012": (
        "EPIC 249893012 es un sistema exoplanetario ubicado a 1,000 años luz de la Tierra. "
        "Su estrella se caracteriza por ser una enana roja con una temperatura aprox de 5,256 K y el descubrimiento "
        "de los 3 planetas confirmados fue llevado a cabo el año 2020. "
    ),
    "KOI-351": (
        "KOI-351 es un sistema exoplanetario ubicado a 1,200 años luz de la Tierra. "
        "Su estrella es una enana amarilla similar al Sol con una temperatura de aprox 6,015 K y el descubrimiento de sus 5 planetas confirmados fue realizado en 2013 "
        "a excepción de KOI-351 i, que fue descubierto en 2017. "
    ),
    "Kepler-100": (
        "Kepler-100 es un sistema exoplanetario situado a 1,500 años luz de la Tierra. "
        "Su estrella es una enana amarilla con una temperatura de aprox de 5,854 K y el descubrimiento de sus 4 planetas confirmados fue realizado en 2013 "
        "a excepción de Kepler-100 e, que fue descubierto en 2023. "
    ),
    "TOI-125": (
        "TOI-125 es un sistema exoplanetario ubicado a 800 años luz de la Tierra. "
        "Su estrella es una enana roja con una temperatura de aprox 3,500 K y el descubrimiento de sus 3 planetas confirmados fue realizado en 2019. "
        "Se espera que se descubran más planetas en un futuro cercano, siendo por ejemplo, TOI-125.04 un candidato a ser confirmado. "
    ),
    "TRAPPIST-1": (
        "TRAPPIST-1 es un sistema exoplanetario ubicado a 40 años luz de la Tierra. "
        "Su estrella es una enana roja con una temperatura de aprox 2,566 K y el descubrimiento de sus 7 planetas confirmados fue realizado en 2016 y 2017. "
    ),
    "HD 20782": (
        "HD-20782 es un sistema exoplanetario ubicado a 100 años luz de la Tierra. "
        "Su estrella es una enana amarilla con una temperatura de aprox 5,774 K y el descubrimiento de su planeta confirmado fue realizado en 2006. "
    ),
    "HD 20794": (
        "HD-20794 es un sistema exoplanetario ubicado a 150 años luz de la Tierra. "
        "Su estrella es una enana amarilla con una temperatura de aprox 5,368 K y el descubrimiento de sus 3 planetas confirmados fue realizado en 2011 y 2025, "
        "sin embargo, en el año 2011 se dió un falso positivo para el planeta HD-20794 c, y HD-20794 e se encuentra en una confirmación controversial."
    )
}

#quiero una función que reciba el nombre de un sistema exoplanetario y retorne su información y que lea la  informacion dentro del diccionario sistemas_exoplanetarios_info que cuente 30 letras, si hay mas de 30 separe la frase cuando el iterador sea un " "(espacio) y retorne la información de ese sistema exoplanetario.
def obtener_info(sistema_seleccionado):
    """
    Obtiene la información de un sistema exoplanetario dado su nombre.
    Si la información supera las 30 letras, la separa en frases cortas.
    """
    info = sistemas_exoplanetarios_info.get(sistema_seleccionado, "Información no disponible para este sistema.")
    
    # Si la información es muy larga, la divide en frases de máximo peo caracteres
    if len(info) > 30:
        palabras = info.split()
        resultado = []
        frase_actual = ""
        
        for palabra in palabras:
            if len(frase_actual) + len(palabra) + 1 <= 111:  # +1 por el espacio
                frase_actual += " " + palabra if frase_actual else palabra
            else:
                resultado.append(frase_actual)
                frase_actual = palabra
        
        if frase_actual:
            resultado.append(frase_actual)
        
        return "\n".join(resultado)
    
    return info

def obtener_info_sistema(nombre_sistema):
    """Obtiene la información de un sistema exoplanetario dado su nombre."""
    return sistemas_exoplanetarios_info.get(nombre_sistema, "Información no disponible para este sistema.")