import pandas as pd

class ETLProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_csv(self):
        self.df = pd.read_csv(self.file_path)
        return self.df

    def clean_data(self):
        if self.df is None:
            raise ValueError("No data loaded")
        # Eliminar duplicados
        self.df = self.df.drop_duplicates()
        # Eliminar filas completamente vacías
        self.df = self.df.dropna(how='all')
        # Rellenar valores numéricos faltantes con la media
        num_cols = self.df.select_dtypes(include='number').columns
        for col in num_cols:
            self.df[col] = self.df[col].fillna(self.df[col].mean())
        # Rellenar valores de texto faltantes con 'desconocido'
        obj_cols = self.df.select_dtypes(include='object').columns
        for col in obj_cols:
            self.df[col] = self.df[col].fillna('desconocido')
        return self.df

    def get_summary(self):
        if self.df is None:
            raise ValueError("No data loaded")
        return self.df.describe(include='all').T
