from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def entrenar_modelo_clasificacion(df, features, target, modelo="RandomForest"):
    """Entrena un modelo de clasificación y retorna métricas.
    modelo: 'RandomForest', 'LogisticRegression', 'SVM', 'DecisionTree', 'NaiveBayes'"""
    X = df[features]
    y = df[target]
    # Eliminar filas con NaN en features o target
    datos = pd.concat([X, y], axis=1).dropna()
    X = datos[features]
    y = datos[target]
    if X.empty or y.empty:
        raise ValueError("Las columnas de características o objetivo están vacías.")
    """entrenamiento del modelos"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if modelo == "RandomForest":
        clf = RandomForestClassifier()
    elif modelo == "LogisticRegression":
        clf = LogisticRegression(max_iter=1000)
    elif modelo == "SVM":
        clf = SVC()
    elif modelo == "DecisionTree":
        clf = DecisionTreeClassifier()
    elif modelo == "NaiveBayes":
        clf = GaussianNB()
    else:
        raise ValueError("Modelo no soportado. Usa 'RandomForest', 'LogisticRegression', 'SVM', 'DecisionTree' o 'NaiveBayes'.")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    reporte = classification_report(y_test, y_pred)
    return acc, reporte


def entrenar_modelo_regresion(df, features, target, modelo="RandomForest"):
    """Entrena un modelo de regresión y retorna métricas (MSE, R2).
    modelo: 'RandomForest', 'LinearRegression', 'SVR', 'DecisionTree'"""
    X = df[features]
    y = df[target]
    # Eliminar filas con NaN en features o target
    datos = pd.concat([X, y], axis=1).dropna()
    X = datos[features]
    y = datos[target]
    if X.empty or y.empty:
        raise ValueError("Las columnas de características o objetivo están vacías.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if modelo == "RandomForest":
        reg = RandomForestRegressor()
    elif modelo == "LinearRegression":
        reg = LinearRegression()
    elif modelo == "SVR":
        reg = SVR()
    elif modelo == "DecisionTree":
        reg = DecisionTreeRegressor()
    else:
        raise ValueError("Modelo no soportado. Usa 'RandomForest', 'LinearRegression', 'SVR' o 'DecisionTree'.")

    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2, y_test, y_pred
