# Módulo de Probabilidad y Estadística

Este módulo proporciona funcionalidades para el análisis estadístico de datos, incluyendo medidas de tendencia central, dispersión y manejo de valores vacíos.

## Funcionalidades

### 📊 Análisis Estadístico Completo
- **Carga de datos**: Soporte para archivos CSV y Excel
- **Medidas de tendencia central**: Media, mediana, moda, cuartiles
- **Medidas de dispersión**: Desviación estándar, varianza, coeficiente de variación
- **Manejo de valores vacíos**: Relleno automático con promedio, mediana o moda
- **Visualizaciones**: Histogramas y gráficos de líneas
- **Reportes**: Generación de reportes estadísticos completos

## Archivos

### Backend (`backend/probabilidad.py`)
- `cargar_datos()`: Carga datos desde archivos CSV/Excel
- `detectar_valores_vacios()`: Identifica valores faltantes
- `rellenar_valores_vacios()`: Rellena valores vacíos con diferentes métodos
- `calcular_medidas_tendencia_central()`: Calcula media, mediana, moda, etc.
- `calcular_desviacion_estandar()`: Calcula medidas de dispersión
- `analisis_completo()`: Función principal que ejecuta todo el análisis
- `generar_reporte_estadistico()`: Genera reporte en texto plano

### Frontend (`frontend/probabilidad/`)
- `analisis_estadistico_view.py`: Interfaz de usuario para el análisis
- `__init__.py`: Inicialización del módulo

## Uso

1. **Carga de datos**: Sube un archivo CSV/Excel o proporciona una ruta local
2. **Configuración**: Selecciona método de relleno para valores vacíos
3. **Análisis**: Elige columna específica o analiza todas las numéricas
4. **Resultados**: Visualiza medidas estadísticas, gráficos y reportes

## Formatos soportados
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)

## Métodos de relleno para valores vacíos
- **Promedio**: Media aritmética
- **Mediana**: Valor central
- **Moda**: Valor más frecuente

## Ejemplo de uso

```python
from backend.probabilidad import analisis_completo

# Análisis completo con relleno por promedio
resultado = analisis_completo(
    archivo_path="datos.csv",
    columna="edad",  # opcional
    rellenar_vacios=True,
    metodo_relleno="promedio"
)

# Acceder a resultados
medidas_centrales = resultado['medidas_tendencia_central']
medidas_dispersion = resultado['medidas_dispersion']
```
