# Transportes Sanluiseña Express 🚌

Sistema de gestión para operaciones diarias de una central de autobuses, desarrollado con Python y Django.

## Características

- **Gestión de Flota**: Registro de autobuses con capacidad y placa.
- **Rutas y Precios**: Control de destinos, orígenes y tarifas.
- **Programación de Viajes**: Asignación de buses a rutas en fechas y horas específicas.
- **Reserva de Boletos**: Interfaz para pasajeros con validación de asientos y capacidad.
- **Seguridad**: Validaciones automáticas para evitar traslapes de buses y sobreventa.
- **Interfaz Premium**: Diseño moderno en modo claro, optimizado para usabilidad.

## Requisitos Previos

- Python 3.8+
- Git (para control de versiones)

## Instalación y Configuración Local

1. **Clonar el repositorio** (una vez subido):
   ```bash
   git clone <url-de-tu-repo>
   cd transporte
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Migraciones y Superusuario**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Iniciar Servidor**:
   ```bash
   python manage.py runserver
   ```

## Preparación para Producción

### 1. Variables de Entorno
Crea un archivo `.env` o configura las variables en tu servidor:
- `DEBUG=False`
- `SECRET_KEY` (Genera una nueva para producción)
- `ALLOWED_HOSTS` (Añade tu dominio o IP)

### 2. Base de Datos
Para producción, se recomienda usar **PostgreSQL** o **MySQL** en lugar de SQLite.

### 3. Servidor Web
Se recomienda usar **Gunicorn** con **Nginx** o **Daphne** para despliegues en Linux.

## Subir a GitHub

Si tienes Git instalado en tu máquina:
1. `git init`
2. `git add .`
3. `git commit -m "Primer commit: Transportes Sanluiseña Express"`
4. `git remote add origin <tu-url-de-github>`
5. `git push -u origin main`

---
Desarrollado con ❤️ para Transportes Sanluiseña Express.
