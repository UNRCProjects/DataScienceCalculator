import pandas as pd
import numpy as np
from typing import List, Union, Dict, Any

def cargar_datos(archivo_path, columna: str = None) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV o Excel.
    
    Args:
        archivo_path: Ruta del archivo a cargar o objeto UploadedFile
        columna: Nombre de la columna específica a analizar (opcional)
    
    Returns:
        DataFrame con los datos cargados
    """
    try:
        # Verificar si es un archivo subido (UploadedFile) o una ruta
        if hasattr(archivo_path, 'name'):
            # Es un archivo subido
            nombre_archivo = archivo_path.name.lower()
            if nombre_archivo.endswith('.csv'):
                df = pd.read_csv(archivo_path)
            elif nombre_archivo.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(archivo_path)
            else:
                raise ValueError("Formato de archivo no soportado. Use CSV o Excel.")
        else:
            # Es una ruta de archivo
            archivo_path_str = str(archivo_path).lower()
            if archivo_path_str.endswith('.csv'):
                df = pd.read_csv(archivo_path)
            elif archivo_path_str.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(archivo_path)
            else:
                raise ValueError("Formato de archivo no soportado. Use CSV o Excel.")
        
        if columna and columna in df.columns:
            return df[[columna]]
        return df
    except Exception as e:
        raise Exception(f"Error al cargar el archivo: {str(e)}")

def detectar_valores_vacios(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detecta valores vacíos en el DataFrame.
    
    Args:
        df: DataFrame a analizar
    
    Returns:
        Diccionario con información sobre valores vacíos
    """
    valores_vacios = df.isnull().sum()
    total_valores = len(df)
    porcentaje_vacios = (valores_vacios / total_valores) * 100
    
    return {
        'valores_vacios': valores_vacios.to_dict(),
        'total_registros': total_valores,
        'porcentaje_vacios': porcentaje_vacios.to_dict()
    }

def rellenar_valores_vacios(df: pd.DataFrame, metodo: str = 'promedio') -> pd.DataFrame:
    """
    Rellena valores vacíos en el DataFrame.
    
    Args:
        df: DataFrame con valores vacíos
        metodo: Método para rellenar ('promedio', 'mediana', 'moda')
    
    Returns:
        DataFrame con valores vacíos rellenados
    """
    df_rellenado = df.copy()
    
    for columna in df_rellenado.select_dtypes(include=[np.number]).columns:
        if metodo == 'promedio':
            df_rellenado[columna].fillna(df_rellenado[columna].mean(), inplace=True)
        elif metodo == 'mediana':
            df_rellenado[columna].fillna(df_rellenado[columna].median(), inplace=True)
        elif metodo == 'moda':
            moda = df_rellenado[columna].mode()
            if not moda.empty:
                df_rellenado[columna].fillna(moda[0], inplace=True)
    
    return df_rellenado

def calcular_medidas_tendencia_central(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula las medidas de tendencia central para cada columna numérica.
    
    Args:
        df: DataFrame con datos numéricos
    
    Returns:
        Diccionario con las medidas de tendencia central
    """
    medidas = {}
    
    for columna in df.select_dtypes(include=[np.number]).columns:
        datos = df[columna].dropna()
        
        medidas[columna] = {
            'media': datos.mean(),
            'mediana': datos.median(),
            'moda': datos.mode().tolist() if not datos.mode().empty else [],
            'cuartil_25': datos.quantile(0.25),
            'cuartil_75': datos.quantile(0.75),
            'minimo': datos.min(),
            'maximo': datos.max(),
            'rango': datos.max() - datos.min()
        }
    
    return medidas

def calcular_desviacion_estandar(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula la desviación estándar y otras medidas de dispersión.
    
    Args:
        df: DataFrame con datos numéricos
    
    Returns:
        Diccionario con medidas de dispersión
    """
    medidas_dispersion = {}
    
    for columna in df.select_dtypes(include=[np.number]).columns:
        datos = df[columna].dropna()
        
        medidas_dispersion[columna] = {
            'desviacion_estandar': datos.std(),
            'varianza': datos.var(),
            'coeficiente_variacion': (datos.std() / datos.mean()) * 100 if datos.mean() != 0 else 0,
            'rango_intercuartilico': datos.quantile(0.75) - datos.quantile(0.25)
        }
    
    return medidas_dispersion

def analisis_completo(archivo_path, columna: str = None, rellenar_vacios: bool = True, metodo_relleno: str = 'promedio') -> Dict[str, Any]:
    """
    Realiza un análisis completo de estadística descriptiva.
    
    Args:
        archivo_path: Ruta del archivo a analizar o objeto UploadedFile
        columna: Columna específica a analizar (opcional)
        rellenar_vacios: Si rellenar valores vacíos
        metodo_relleno: Método para rellenar valores vacíos
    
    Returns:
        Diccionario con análisis completo
    """
    # Cargar datos
    df = cargar_datos(archivo_path, columna)
    
    # Detectar valores vacíos
    info_vacios = detectar_valores_vacios(df)
    
    # Rellenar valores vacíos si se solicita
    if rellenar_vacios and info_vacios['valores_vacios']:
        df = rellenar_valores_vacios(df, metodo_relleno)
    
    # Calcular medidas
    medidas_centrales = calcular_medidas_tendencia_central(df)
    medidas_dispersion = calcular_desviacion_estandar(df)
    
    # Resumen estadístico
    resumen_estadistico = df.describe()
    
    return {
        'datos_originales': df,
        'info_valores_vacios': info_vacios,
        'medidas_tendencia_central': medidas_centrales,
        'medidas_dispersion': medidas_dispersion,
        'resumen_estadistico': resumen_estadistico,
        'columnas_numericas': list(df.select_dtypes(include=[np.number]).columns),
        'total_registros': len(df)
    }

def generar_reporte_estadistico(analisis: Dict[str, Any]) -> str:
    """
    Genera un reporte estadístico en formato texto.
    
    Args:
        analisis: Resultado del análisis completo
    
    Returns:
        Reporte estadístico formateado
    """
    reporte = []
    reporte.append("=== REPORTE DE ANÁLISIS ESTADÍSTICO ===\n")
    
    # Información general
    reporte.append(f"Total de registros: {analisis['total_registros']}")
    reporte.append(f"Columnas numéricas: {', '.join(analisis['columnas_numericas'])}\n")
    
    # Información de valores vacíos
    info_vacios = analisis['info_valores_vacios']
    if any(info_vacios['valores_vacios'].values()):
        reporte.append("=== VALORES VACÍOS ===")
        for col, vacios in info_vacios['valores_vacios'].items():
            if vacios > 0:
                reporte.append(f"{col}: {vacios} valores vacíos ({info_vacios['porcentaje_vacios'][col]:.1f}%)")
        reporte.append("")
    
    # Medidas de tendencia central
    reporte.append("=== MEDIDAS DE TENDENCIA CENTRAL ===")
    for columna, medidas in analisis['medidas_tendencia_central'].items():
        reporte.append(f"\n{columna.upper()}:")
        reporte.append(f"  Media: {medidas['media']:.4f}")
        reporte.append(f"  Mediana: {medidas['mediana']:.4f}")
        if medidas['moda']:
            reporte.append(f"  Moda: {medidas['moda']}")
        reporte.append(f"  Mínimo: {medidas['minimo']:.4f}")
        reporte.append(f"  Máximo: {medidas['maximo']:.4f}")
        reporte.append(f"  Rango: {medidas['rango']:.4f}")
    
    # Medidas de dispersión
    reporte.append("\n=== MEDIDAS DE DISPERSIÓN ===")
    for columna, medidas in analisis['medidas_dispersion'].items():
        reporte.append(f"\n{columna.upper()}:")
        reporte.append(f"  Desviación estándar: {medidas['desviacion_estandar']:.4f}")
        reporte.append(f"  Varianza: {medidas['varianza']:.4f}")
        reporte.append(f"  Coeficiente de variación: {medidas['coeficiente_variacion']:.2f}%")
        reporte.append(f"  Rango intercuartílico: {medidas['rango_intercuartilico']:.4f}")
    
    return "\n".join(reporte)
