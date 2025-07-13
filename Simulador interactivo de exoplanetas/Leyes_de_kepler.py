import tkinter as tk
import math 

def primera_ley_de_kepler(a,e, theta):
    """
    Calcula la posición de un planeta en una órbita elíptica según la primera ley de Kepler.

    Parámetros:
    a (float): Semi-eje mayor de la elipse.
    e (float): Excentricidad de la elipse.
    theta (float): Ángulo verdadero en radianes.

    Retorna:
    tuple: Coordenadas (x, y) del planeta en la órbita.
    """
    r = a * (1 - e**2) / (1 + e * math.cos(theta))  # Distancia radial
    x = r * math.cos(theta)  # Coordenada x
    y = r * math.sin(theta)  # Coordenada y
    return x, y


def segunda_ley_de_kepler(t, a, e, T):
    M = 2 * math.pi * (t / T) % (2 * math.pi)
    E = resolver_E(M, e)
    theta = obtener_theta(E, e)
    return primera_ley_de_kepler(a, e, theta)

def resolver_E(M, e, tol=1e-6):
    E = M if e < 0.8 else math.pi
    for _ in range(100):
        sinE = math.sin(E)
        f = E - e * sinE - M
        if abs(f) < tol:
            return E
        f_prime = 1 - e * math.cos(E)
        # Protección contra división por cero
        if abs(f_prime) > 1e-12:
            E -= f / f_prime
        else:
            E = M  
    return E
def obtener_theta(E, e):
    """
    Convierte la anomalía excéntrica E a ángulo verdadero θ.
    Parámetros:
    E (float): Anomalía excéntrica.
    e (float): Excentricidad de la órbita.
    Retorna:
    float: Ángulo verdadero θ en radianes.
    """
    tan_half_theta = math.sqrt((1 + e) / (1 - e)) * math.tan(E / 2)
    theta = 2 * math.atan(tan_half_theta)
    return theta

def tercera_ley_de_kepler(a, T):
    """
    Calcula la relación entre el semieje mayor y el período orbital según la tercera ley de Kepler.

    Parámetros:
    a (float): Semi-eje mayor de la órbita.
    T (float): Período orbital del planeta.

    Retorna:
    float: Relación entre el semieje mayor y el período orbital.
    """
    return a**3 / T**2  # Ley de Kepler: T^2 ∝ a^3
