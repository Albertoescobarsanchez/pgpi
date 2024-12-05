# Usar una imagen base oficial de Python
FROM python:3.12-slim

# Configuración del directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app/

# Instalar las dependencias necesarias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto en el que correrá el servidor (usualmente 8000 para Django)
EXPOSE 8000

# Definir el comando para iniciar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
