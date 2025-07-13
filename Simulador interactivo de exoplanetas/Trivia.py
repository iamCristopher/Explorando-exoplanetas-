import random

# Datos simplificados de exoplanetas (esto es lo de las tablas)
exoplanetas = [
    {"nombre": "EPIC 249893012 b", "a": 0.047, "T": 3.6, "e": 0.06, "tipo": "Júpiter caliente"},
    {"nombre": "KOI-351 b", "a": 0.074, "T": 7.0, "e": 0.0, "tipo": "Mini-Neptuno"},
    {"nombre": "TRAPPIST-1 b", "a": 0.012, "T": 1.5, "e": 0.006, "tipo": "Planeta rocoso"}
]

# Preguntas diccionario (la idea es hacer preguntas para complementar cuando el profe haga una clase 
# acerca de las leyes de keplery use el simulador como ejemplo) 
preguntas = [
    {
        "pregunta": "Según la 3° Ley de Kepler, si un planeta está más cerca de su estrella:",
        "opciones": [
            "a) Orbita más rápido",
            "b) Orbita más lento",
            "c) Su órbita se hace más ovalada",
            "d) Gira más rápido sobre sí mismo"
        ],
        "respuesta": "a",
        "explicacion": "A menor distancia, mayor velocidad orbital (como TRAPPIST-1 b que tarda solo 1.5 días)."
    },
    {
        "pregunta": "¿Qué forma tiene la órbita de KOI-351 b si su excentricidad es 0?",
        "opciones": [
            "a) Círculo perfecto",
            "b) Óvalo pronunciado",
            "c) Espiral",
            "d) Elipse alargada"
        ],
        "respuesta": "a",
        "explicacion": "Exacto. Excentricidad 0 indica órbita circular perfecta."
    },
    {
        "pregunta": "¿Qué ley explica que los planetas barran áreas iguales en tiempos iguales?",
        "opciones": [
            "a) 1° Ley de Kepler",
            "b) 2° Ley de Kepler",
            "c) 3° Ley de Kepler",
            "d) Ley de Gravitación"
        ],
        "respuesta": "b",
        "explicacion": "Así es. La 2° Ley o 'Ley de las áreas' lo explica."
    },
    {
        "pregunta": "¿Qué planeta de la lista sería más fácil detectar según Kepler?",
        "opciones": [
            "a) EPIC 249893012 b (órbita de 3.6 días)",
            "b) KOI-351 b (órbita de 7 días)",
            "c) TRAPPIST-1 b (órbita de 1.5 días)",
            "d) Todos igual"
        ],
        "respuesta": "c",
        "explicacion": "TRAPPIST-1 b es el más cercano a su estrella, por lo que su tránsito sería más fácil de detectar."
    },
    {
        "pregunta": "La 3° Ley relaciona:",
        "opciones": [
            "a) Tamaño del planeta con su temperatura",
            "b) Distancia orbital con período de traslación",
            "c) Masa del planeta con su gravedad",
            "d) Edad de la estrella con número de planetas"
        ],
        "respuesta": "b",
        "explicacion": "Relaciona el semieje mayor (a) con el período orbital (T)."
    },
    {
        "pregunta": "La constante de proporcionalidad en la 3° Ley de Kepler es:",
        "opciones": [
            "a) Universal para todos los sistemas",
            "b) Universal para sistemas similares",
            "c) Específica de cada estrella",
            "d) Igual a la masa del planet"
        ],
        "respuesta": "c",
        "explicacion": "Depende de la masa de la estrella central del sistema (como el Sol en nuestro caso)."
    },
    {
        "pregunta": "¿Cómo debe verse un gráfico sobre la primera ley de Kepler para demostrar que una órbita es elíptica?",
        "opciones": [
            "a) debe mostrar un círculo perfecto",
            "b) debe mostrar una línea recta",
            "c) debe mostrar una onda sinusoidal",
            "d) debe mostrar un espiral"
        ],
        "respuesta": "c",
        "explicacion": "Un gráfico debe mostrar una onda sinusoidal para demostrar que la órbita es elíptica, ya que las órbitas elípticas tienen una forma ovalada y no son circulares ni lineales."
    }
]