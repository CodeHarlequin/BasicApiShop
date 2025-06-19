# 🛍️ Basic Shop API

Este proyecto es una API RESTful basica para la gestión de inventario, desarrollada con **FastAPI**. Incluye funcionalidades como creación, actualización, filtrado, activación/desactivación y eliminación de productos.

---

## 🚀 Tecnologías

- ⚡ FastAPI
- 🧬 SQLAlchemy
- 🪶 SQLite
- 🔐 Pydantic
- 🌱 Alembic (opcional, para migraciones)
- 🐍 Python 3.13.1

---

## 📦 Instalación y puesta en marcha

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

## 2️⃣ Crear entorno virtual

### Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows: 

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```
## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4️⃣ Migraciones 

### Alembic
```bash
alembic revision --autogenerate -m "first migration"  
alembic upgrade head 
```

## 5️⃣ Ejecutar servidor
```bash
# ./app
uvicorn app.main:app --reload
```
