# Calculadora para Ciencia de Datos

Este proyecto es una calculadora desarrollada 100% en **Python + Streamlit**, diseñada como práctica para estudiantes de Ciencia de Datos.  

La aplicación permite realizar operaciones matemáticas, estadísticas, gráficas, procesamiento de imágenes en un entorno sencillo y visual.  

Fue diseñado como un ejercicio de **colaboración con Git y GitHub**, donde cada grupo de estudiantes aporta un módulo distinto.

## Objetivos del proyecto

* Practicar el uso de **Git y GitHub** en un flujo de trabajo colaborativo.
* Desarrollar código modular en **Python**.
* Implementar operaciones utilizadas en el campo de ciencia de datos.

## Estructura del repositorio

```
DataScienceCalculator/
│── .gitignore
│── README.md
│── requirements.txt
│── app.py 
├── assets/
│ ├── imagen1.png
│ ├── imagen2.png
├── backend/
│ ├── modulo1.py
├── frontend/ (vistas)
│ ├── home_view.py
│ ├── autores_view.py
│ ├── modulo1/
│ │ ├── operacion1.py
│ │ ├── operacion2.py
```

## Ejecutar en local 

1. Clona el repositorio

   ```bash
   git clone https://github.com/UNRCProjects/DataScienceCalculator.git
   cd DataScienceCalculator
   ```
2. Crear y activar un entorno virtual  
    En Windows
	```bash
	python -m venv venv
	venv\Scripts\activate
	```  
	En Linux/MacOS
	```bash
	python3 -m venv venv
	source venv/bin/activate	
	```
3. Instalar las dependencias desde requirements.txt
	```bash
	pip install -r requirements.txt
	```

### Ejecutar Servicio Web
4a. Ejecuta el archivo principal

   ```bash
   streamlit run app.py
   ```
5a. Abrir en el navegador `http://localhost:8501`

## Despliegue en Streamlit Cloud

1. Asegúrate de que tu repositorio está en GitHub y contiene `requirements.txt` y `app.py` en la raíz.
2. Ve a https://share.streamlit.io y conecta tu cuenta de GitHub.
3. Crea una nueva aplicación seleccionando el repositorio y el branch `main`, y configura el archivo de entrada como `app.py`.
4. Streamlit Cloud instalará las dependencias y desplegará la app automáticamente. Si hay errores revisa los logs en la interfaz de Streamlit Cloud.

Alternativamente puedes desplegar en servicios como Heroku, Railway o Render siguiendo sus guías para aplicaciones Python basadas en web.

<!--
### Ejecutar API
4b. Ejecuta el archivo principal

   ```bash
   uvicorn backend.api.main:app --reload
   ```
5b. Probar la operacion suma `http://localhost:8000/aritmetica/suma?a=1&b=2`  

6b. Probar la operacion división `http://localhost:8000/aritmetica/division?a=4&b=2`
-->

## Autores

Este proyecto es desarrollado por estudiantes de 8vo semestre (2025-2) de la Universidad Nacional Rosario Castellanos Campus Magdalena Contreras.
