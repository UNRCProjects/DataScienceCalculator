"""
Módulo backend para la multiplicación de matrices.
Implementa la multiplicación desde cero sin usar Numpy.
"""

def multiplicar_matrices(A, B):
    """
    Multiplica dos matrices A y B si sus dimensiones son compatibles.
    Devuelve la matriz resultado o None si no se pueden multiplicar.
    """
    try:
        filas_A = len(A)
        columnas_A = len(A[0])
        filas_B = len(B)
        columnas_B = len(B[0])

        # Validar compatibilidad
        if columnas_A != filas_B:
            return None

        # Crear matriz resultado con ceros
        resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]

        # Multiplicación clásica
        for i in range(filas_A):
            for j in range(columnas_B):
                for k in range(columnas_A):
                    resultado[i][j] += A[i][k] * B[k][j]

        return resultado
    except Exception as e:
        return f"Error: {str(e)}"
