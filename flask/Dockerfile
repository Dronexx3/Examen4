# Usa una imagen base de Python
FROM python:3.9

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el código fuente
COPY . .

EXPOSE 5000

# Define el comando para ejecutar la aplicación
CMD ["python", "app.py"]

