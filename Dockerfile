FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Instalar Chrome y ChromeDriver
RUN apt-get update && apt-get install -y chromium-browser chromium-chromedriver

# Copiar el código del proyecto
COPY . /workspace

WORKDIR /workspace
