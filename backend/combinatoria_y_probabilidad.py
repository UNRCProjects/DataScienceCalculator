"""
Módulo de Combinatoria y Probabilidad Básica
=============================================

Este módulo proporciona funciones para realizar cálculos combinatorios y probabilísticos
fundamentales en ciencia de datos. Incluye operaciones como:

- Factoriales
- Permutaciones (nPr)
- Combinaciones (nCr) 
- Probabilidades básicas
- Distribución binomial

Autor: Gloria Ury
Fecha: 2025
"""

import math
from scipy.stats import binom
import numpy as np


def factorial(n):
    """
    Calcula el factorial de un número n.
    
    El factorial de n (n!) es el producto de todos los enteros positivos
    desde 1 hasta n. Por definición, 0! = 1.
    
    Args:
        n (int): Número entero no negativo
        
    Returns:
        int: Factorial de n
        
    Raises:
        ValueError: Si n es negativo o no es entero
    """
    n = int(n)
    if n < 0:
        raise ValueError("El factorial solo está definido para números no negativos")
    return math.factorial(n)


def permutacion_sin_repeticion(n, r):
    """
    Calcula el número de permutaciones de n elementos tomados de r en r sin repetición.
    
    Una permutación es un arreglo ordenado de elementos. La fórmula es:
    P(n,r) = n! / (n-r)!
    
    Args:
        n (int): Total de elementos disponibles
        r (int): Número de elementos a seleccionar
        
    Returns:
        int: Número de permutaciones posibles
        
    Raises:
        ValueError: Si r > n o alguno de los valores es negativo
    """
    n, r = int(n), int(r)
    if r < 0 or n < 0:
        raise ValueError("Los valores deben ser no negativos")
    if r > n:
        raise ValueError("r no puede ser mayor que n")
    return factorial(n) // factorial(n - r)


def permutacion_con_repeticion(n, r):
    """
    Calcula el número de permutaciones de n elementos tomados de r en r con repetición.
    
    Cuando se permite repetición, cada posición puede ser ocupada por cualquiera
    de los n elementos. La fórmula es: n^r
    
    Args:
        n (int): Total de elementos disponibles
        r (int): Número de posiciones a llenar
        
    Returns:
        int: Número de permutaciones con repetición
        
    Raises:
        ValueError: Si alguno de los valores es negativo
    """
    n, r = int(n), int(r)
    if n < 0 or r < 0:
        raise ValueError("Los valores deben ser no negativos")
    return n ** r


def combinacion(n, r):
    """
    Calcula el número de combinaciones de n elementos tomados de r en r.
    
    Una combinación es una selección no ordenada de elementos. La fórmula es:
    C(n,r) = n! / (r! * (n-r)!) = (n r) (coeficiente binomial)
    
    Args:
        n (int): Total de elementos disponibles
        r (int): Número de elementos a seleccionar
        
    Returns:
        int: Número de combinaciones posibles
        
    Raises:
        ValueError: Si r > n o alguno de los valores es negativo
    """
    n, r = int(n), int(r)
    if r < 0 or n < 0:
        raise ValueError("Los valores deben ser no negativos")
    if r > n:
        raise ValueError("r no puede ser mayor que n")
    return factorial(n) // (factorial(r) * factorial(n - r))


def probabilidad_evento_simple(casos_favorables, casos_posibles):
    """
    Calcula la probabilidad de un evento simple.
    
    La probabilidad de un evento es el cociente entre el número de casos
    favorables y el número total de casos posibles.
    P(A) = casos_favorables / casos_posibles
    
    Args:
        casos_favorables (int): Número de casos que favorecen el evento
        casos_posibles (int): Número total de casos posibles
        
    Returns:
        float: Probabilidad del evento (entre 0 y 1)
        
    Raises:
        ValueError: Si casos_posibles es 0 o casos_favorables > casos_posibles
    """
    casos_favorables, casos_posibles = int(casos_favorables), int(casos_posibles)
    if casos_posibles == 0:
        raise ValueError("El número de casos posibles no puede ser cero")
    if casos_favorables < 0 or casos_posibles < 0:
        raise ValueError("Los valores deben ser no negativos")
    if casos_favorables > casos_posibles:
        raise ValueError("Los casos favorables no pueden ser mayores que los casos posibles")
    return casos_favorables / casos_posibles


def probabilidad_binomial(n, k, p):
    """
    Calcula la probabilidad de exactamente k éxitos en n ensayos de Bernoulli.
    
    La distribución binomial modela el número de éxitos en una secuencia de n
    ensayos independientes, cada uno con probabilidad de éxito p.
    
    Args:
        n (int): Número total de ensayos
        k (int): Número de éxitos deseados
        p (float): Probabilidad de éxito en cada ensayo (0 ≤ p ≤ 1)
        
    Returns:
        float: Probabilidad de exactamente k éxitos
        
    Raises:
        ValueError: Si los parámetros están fuera de rango
    """
    n, k = int(n), int(k)
    if n < 0 or k < 0:
        raise ValueError("n y k deben ser no negativos")
    if k > n:
        raise ValueError("k no puede ser mayor que n")
    if not (0 <= p <= 1):
        raise ValueError("p debe estar entre 0 y 1")
    
    return binom.pmf(k, n, p)


def probabilidad_binomial_acumulada(n, k, p, tipo="menor_igual"):
    """
    Calcula la probabilidad acumulada de la distribución binomial.
    
    Args:
        n (int): Número total de ensayos
        k (int): Número de éxitos
        p (float): Probabilidad de éxito en cada ensayo
        tipo (str): "menor_igual" para P(X ≤ k), "mayor_igual" para P(X ≥ k)
        
    Returns:
        float: Probabilidad acumulada
        
    Raises:
        ValueError: Si los parámetros están fuera de rango o tipo es inválido
    """
    n, k = int(n), int(k)
    if n < 0 or k < 0:
        raise ValueError("n y k deben ser no negativos")
    if k > n:
        raise ValueError("k no puede ser mayor que n")
    if not (0 <= p <= 1):
        raise ValueError("p debe estar entre 0 y 1")
    
    if tipo == "menor_igual":
        return binom.cdf(k, n, p)
    elif tipo == "mayor_igual":
        return 1 - binom.cdf(k - 1, n, p)
    else:
        raise ValueError("tipo debe ser 'menor_igual' o 'mayor_igual'")


def variacion_sin_repeticion(n, r):
    """
    Sinónimo de permutacion_sin_repeticion para compatibilidad con terminología.
    """
    return permutacion_sin_repeticion(n, r)


def variacion_con_repeticion(n, r):
    """
    Sinónimo de permutacion_con_repeticion para compatibilidad con terminología.
    """
    return permutacion_con_repeticion(n, r)


def coeficiente_binomial(n, r):
    """
    Sinónimo de combinacion para compatibilidad con terminología matemática.
    """
    return combinacion(n, r)


def probabilidad_complemento(probabilidad_evento):
    """
    Calcula la probabilidad del evento complementario.
    
    P(A') = 1 - P(A)
    
    Args:
        probabilidad_evento (float): Probabilidad del evento original
        
    Returns:
        float: Probabilidad del evento complementario
        
    Raises:
        ValueError: Si la probabilidad no está entre 0 y 1
    """
    if not (0 <= probabilidad_evento <= 1):
        raise ValueError("La probabilidad debe estar entre 0 y 1")
    return 1 - probabilidad_evento


def probabilidad_union_eventos_independientes(p_a, p_b):
    """
    Calcula la probabilidad de la unión de dos eventos independientes.
    
    P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
    Para eventos independientes: P(A ∩ B) = P(A) * P(B)
    
    Args:
        p_a (float): Probabilidad del evento A
        p_b (float): Probabilidad del evento B
        
    Returns:
        float: Probabilidad de A ∪ B
        
    Raises:
        ValueError: Si las probabilidades no están entre 0 y 1
    """
    if not (0 <= p_a <= 1) or not (0 <= p_b <= 1):
        raise ValueError("Las probabilidades deben estar entre 0 y 1")
    return p_a + p_b - (p_a * p_b)
