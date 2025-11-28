
# 💻 LP_GO — Guía de Instalación y Ejecución

Este proyecto combina un **backend en Python** con un **editor web en Vite + npm**.  
Sigue estos pasos para levantar todo correctamente.

---

## 🚀 1. Crear y activar el entorno virtual

### Crear el venv
```bash
python3 -m venv venv
````

### Activar el venv

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD)**

```cmd
venv\Scripts\activate.bat
```

---

## 📦 2. Instalar dependencias de Python

Desde la raíz del proyecto:

```bash
pip install -r requirements.txt
```

---

## 🌐 3. Instalar dependencias del editor web

Navega a la carpeta del editor:

```bash
cd lp-editor
npm install
```

---

## ▶️ 4. Ejecutar el proyecto

### Ejecutar el frontend

Abre una terminal y desde la carpeta `lp-go`:

```bash
npm run dev
```

Luego abre en el navegador:

```
http://localhost:5173/
```

### Ejecutar el backend

En otra terminal, desde la raíz del proyecto:

```bash
python -m backend.server
```

---

## 🎉 Listo

El proyecto estará corriendo con el backend en Python y el editor web en Vite.

```
```
