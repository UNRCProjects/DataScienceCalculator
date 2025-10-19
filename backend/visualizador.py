# -*- coding: utf-8 -*-
"""
Modulo de Visualizacion y Analisis de Datos

Este modulo proporciona funciones para cargar, limpiar, analizar y visualizar datos
desde archivos CSV y Excel. Todas las funciones estan documentadas en espanol.

Autor: DataScienceCalculator Team
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
import io


def cargar_datos(ruta_archivo):
    """
    Carga un archivo CSV o Excel y retorna un DataFrame de pandas.

    Args:
        ruta_archivo (str): Ruta completa al archivo (.csv, .xls, .xlsx)

    Returns:
        pandas.DataFrame: DataFrame con los datos cargados

    Raises:
        ValueError: Si el formato del archivo no es compatible
        FileNotFoundError: Si el archivo no existe
    """
    try:
        # Detectar extension del archivo
        if ruta_archivo.name.endswith('.csv'):
            df = pd.read_csv(ruta_archivo)
        elif ruta_archivo.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(ruta_archivo)
        else:
            raise ValueError("Formato no soportado. Use archivos .csv, .xls o .xlsx")

        return df
    except Exception as e:
        raise Exception(f"Error al cargar el archivo: {str(e)}")


def convertir_a_numerico(dataframe, columna):
    """
    Convierte una columna de texto a tipo numerico (int o float).

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene la columna
        columna (str): Nombre de la columna a convertir

    Returns:
        pandas.Series: Serie con los valores convertidos a numerico
    """
    try:
        # Intentar convertir a numerico, valores invalidos se convierten a NaN
        serie_numerica = pd.to_numeric(dataframe[columna], errors='coerce')
        return serie_numerica
    except Exception as e:
        raise Exception(f"Error al convertir columna '{columna}': {str(e)}")


def manejar_nulos(dataframe, columna, estrategia='eliminar'):
    """
    Maneja valores nulos en una columna especifica.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene la columna
        columna (str): Nombre de la columna a procesar
        estrategia (str): Estrategia a usar - 'eliminar', 'media' o 'moda'

    Returns:
        pandas.DataFrame: DataFrame procesado segun la estrategia
    """
    df_copia = dataframe.copy()

    if estrategia == 'eliminar':
        # Eliminar filas con valores nulos en la columna
        df_copia = df_copia.dropna(subset=[columna])

    elif estrategia == 'media':
        # Rellenar con la media (solo para columnas numericas)
        if pd.api.types.is_numeric_dtype(df_copia[columna]):
            media = df_copia[columna].mean()
            df_copia[columna] = df_copia[columna].fillna(media)
        else:
            raise ValueError(f"La columna '{columna}' no es numerica. No se puede usar la media.")

    elif estrategia == 'moda':
        # Rellenar con la moda (valor mas frecuente)
        moda = df_copia[columna].mode()
        if len(moda) > 0:
            df_copia[columna] = df_copia[columna].fillna(moda[0])

    else:
        raise ValueError("Estrategia no valida. Use 'eliminar', 'media' o 'moda'")

    return df_copia


def analisis_estadistico(dataframe, columna):
    """
    Calcula estadisticas basicas de una columna.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene la columna
        columna (str): Nombre de la columna a analizar

    Returns:
        dict: Diccionario con las estadisticas calculadas
    """
    serie = dataframe[columna]

    # Calcular frecuencias
    frecuencias = serie.value_counts().to_dict()

    estadisticas = {
        'total_datos': len(serie),
        'valores_nulos': serie.isna().sum(),
        'valores_unicos': serie.nunique(),
        'frecuencias': frecuencias
    }

    # Si la columna es numerica, calcular estadisticas adicionales
    if pd.api.types.is_numeric_dtype(serie):
        serie_limpia = serie.dropna()

        estadisticas.update({
            'media': serie_limpia.mean(),
            'mediana': serie_limpia.median(),
            'moda': serie_limpia.mode().tolist() if len(serie_limpia.mode()) > 0 else None,
            'minimo': serie_limpia.min(),
            'maximo': serie_limpia.max(),
            'desviacion_estandar': serie_limpia.std(),
            'varianza': serie_limpia.var(),
            'cuartil_25': serie_limpia.quantile(0.25),
            'cuartil_75': serie_limpia.quantile(0.75)
        })

    return estadisticas


def generar_tabla_frecuencia(dataframe, columna, limite=20):
    """
    Genera un grafico de barras con la tabla de frecuencias.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene la columna
        columna (str): Nombre de la columna a analizar
        limite (int): Numero maximo de categorias a mostrar

    Returns:
        matplotlib.figure.Figure: Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Calcular frecuencias
    frecuencias = dataframe[columna].value_counts().head(limite)

    # Crear grafico de barras
    ax.bar(range(len(frecuencias)), frecuencias.values, color='steelblue', edgecolor='black')
    ax.set_xticks(range(len(frecuencias)))
    ax.set_xticklabels(frecuencias.index, rotation=45, ha='right')
    ax.set_xlabel('Categorias', fontsize=12)
    ax.set_ylabel('Frecuencia', fontsize=12)
    ax.set_title(f'Tabla de Frecuencias - {columna}', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig


def generar_diagrama_dispersion(dataframe, columna_x, columna_y):
    """
    Genera un diagrama de dispersion entre dos variables.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene las columnas
        columna_x (str): Nombre de la columna para el eje X
        columna_y (str): Nombre de la columna para el eje Y

    Returns:
        matplotlib.figure.Figure: Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Eliminar filas con valores nulos
    df_limpio = dataframe[[columna_x, columna_y]].dropna()

    ax.scatter(df_limpio[columna_x], df_limpio[columna_y], alpha=0.6,
               color='steelblue', edgecolor='black', s=80)
    ax.set_xlabel(columna_x, fontsize=12)
    ax.set_ylabel(columna_y, fontsize=12)
    ax.set_title(f'Diagrama de Dispersion: {columna_x} vs {columna_y}',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def generar_grafico_pastel(dataframe, columna, limite=10):
    """
    Genera un grafico de pastel mostrando la distribucion de categorias.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene la columna
        columna (str): Nombre de la columna a analizar
        limite (int): Numero maximo de categorias a mostrar

    Returns:
        matplotlib.figure.Figure: Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calcular frecuencias
    frecuencias = dataframe[columna].value_counts().head(limite)

    # Crear grafico de pastel
    colores = plt.cm.Set3(range(len(frecuencias)))
    wedges, texts, autotexts = ax.pie(frecuencias.values, labels=frecuencias.index,
                                        autopct='%1.1f%%', startangle=90,
                                        colors=colores, textprops={'fontsize': 10})

    ax.set_title(f'Grafico de Pastel - {columna}', fontsize=14, fontweight='bold')

    # Mejorar legibilidad
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')

    plt.tight_layout()
    return fig


def generar_histograma(dataframe, columna, bins=30):
    """
    Genera un histograma de distribucion para una variable numerica.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene la columna
        columna (str): Nombre de la columna a analizar
        bins (int): Numero de intervalos (bins) para el histograma

    Returns:
        matplotlib.figure.Figure: Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Eliminar valores nulos
    datos = dataframe[columna].dropna()

    # Crear histograma
    n, bins_edges, patches = ax.hist(datos, bins=bins, color='steelblue',
                                      edgecolor='black', alpha=0.7)

    # Anadir linea de densidad
    ax2 = ax.twinx()
    datos.plot.kde(ax=ax2, color='red', linewidth=2, label='Densidad')
    ax2.set_ylabel('Densidad', fontsize=12)
    ax2.legend(loc='upper right')

    ax.set_xlabel(columna, fontsize=12)
    ax.set_ylabel('Frecuencia', fontsize=12)
    ax.set_title(f'Histograma de Distribucion - {columna}', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig


def generar_diagrama_caja(dataframe, columnas):
    """
    Genera un diagrama de caja (boxplot) para una o varias columnas.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene las columnas
        columnas (list): Lista de nombres de columnas a analizar

    Returns:
        matplotlib.figure.Figure: Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Preparar datos
    datos = [dataframe[col].dropna() for col in columnas]

    # Crear boxplot
    bp = ax.boxplot(datos, labels=columnas, patch_artist=True,
                    notch=True, showmeans=True)

    # Colorear cajas
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_edgecolor('black')

    ax.set_ylabel('Valores', fontsize=12)
    ax.set_title('Diagrama de Caja', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    return fig


def generar_mapa_calor(dataframe, columnas):
    """
    Genera un mapa de calor de correlaciones entre variables numericas.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene las columnas
        columnas (list): Lista de nombres de columnas a analizar

    Returns:
        matplotlib.figure.Figure: Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Seleccionar solo columnas numericas
    df_numerico = dataframe[columnas].select_dtypes(include=[np.number])

    # Calcular matriz de correlacion
    correlacion = df_numerico.corr()

    # Crear mapa de calor
    sns.heatmap(correlacion, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                ax=ax)

    ax.set_title('Mapa de Calor de Correlaciones', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    return fig


def generar_regresion_lineal(dataframe, columna_x, columna_y):
    """
    Genera un grafico de regresion lineal entre dos variables.

    Args:
        dataframe (pandas.DataFrame): DataFrame que contiene las columnas
        columna_x (str): Nombre de la columna para el eje X (variable independiente)
        columna_y (str): Nombre de la columna para el eje Y (variable dependiente)

    Returns:
        tuple: (matplotlib.figure.Figure, dict) - Figura y diccionario con estadisticas
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Eliminar filas con valores nulos
    df_limpio = dataframe[[columna_x, columna_y]].dropna()

    X = df_limpio[columna_x].values.reshape(-1, 1)
    y = df_limpio[columna_y].values

    # Crear modelo de regresion lineal
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Predecir valores
    y_pred = modelo.predict(X)

    # Calcular R cuadrado
    r_cuadrado = modelo.score(X, y)

    # Calcular correlacion de Pearson
    correlacion, p_valor = stats.pearsonr(df_limpio[columna_x], df_limpio[columna_y])

    # Graficar puntos
    ax.scatter(X, y, alpha=0.6, color='steelblue', edgecolor='black',
               s=80, label='Datos observados')

    # Graficar linea de regresion
    ax.plot(X, y_pred, color='red', linewidth=2, label='Linea de regresion')

    ax.set_xlabel(columna_x, fontsize=12)
    ax.set_ylabel(columna_y, fontsize=12)
    ax.set_title(f'Regresion Lineal: {columna_x} vs {columna_y}',
                 fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Anadir ecuacion y estadisticas
    ecuacion = f'y = {modelo.coef_[0]:.4f}x + {modelo.intercept_:.4f}'
    texto_stats = f'{ecuacion}\nR2 = {r_cuadrado:.4f}\nCorrelacion = {correlacion:.4f}'
    ax.text(0.05, 0.95, texto_stats, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    estadisticas = {
        'pendiente': modelo.coef_[0],
        'intercepto': modelo.intercept_,
        'r_cuadrado': r_cuadrado,
        'correlacion': correlacion,
        'p_valor': p_valor,
        'ecuacion': ecuacion
    }

    return fig, estadisticas
