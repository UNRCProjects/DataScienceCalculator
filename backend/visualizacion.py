import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generar_grafico_dispersion(df: pd.DataFrame, col_x: str, col_y: str):
    """
    Genera un gráfico de dispersión (scatterplot) usando Seaborn.

    Args:
        df (pd.DataFrame): El DataFrame con los datos.
        col_x (str): El nombre de la columna para el eje X.
        col_y (str): El nombre de la columna para el eje Y.

    Returns:
        matplotlib.figure.Figure: La figura del gráfico generado.
    """
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=col_x, y=col_y, ax=ax)
    ax.set_title(f'Gráfico de Dispersión: {col_y} vs {col_x}')
    return fig