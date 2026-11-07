# PF-SIIEC

Proyecto final de Infraestructura del Desarrollo Continuo: **Sistema de inventario con integración y entrega continua**.

## Ejecutar

Con Docker Desktop iniciado y `.env` configurado:

```powershell
cd C:\PF-SIIEC
docker compose up --build -d --wait
```

Abre <http://127.0.0.1:8000>. La base PostgreSQL conserva sus datos en un volumen. El catálogo comienza vacío. Para detener: `docker compose down` (sin `-v`).

También puedes ejecutar directamente en Windows con SQLite:

```powershell
.\.venv\Scripts\python.exe run.py
```

Usa un solo modo a la vez. La instalación, las variables y las instrucciones completas están en [Desarrollo y operación](docs/Desarrollo.md).

## Funciones

- Alta, búsqueda, edición y desactivación de productos con código único.
- Entradas y salidas enteras positivas, sin permitir stock negativo.
- Historial persistente y movimientos transaccionales.
- Protección CSRF en formularios y endpoint de salud `/health`.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Pruebas SQLite aisladas localmente y PostgreSQL en CI, incluyendo concurrencia y persistencia. No usar `TEST_DATABASE_URL` con una base de datos real: las pruebas borran los datos de esa base.

## Automatización

GitHub Actions ejecuta pruebas y construye Docker. En `main`, publica la imagen en GHCR con el SHA del commit después de pasar ambas verificaciones. La ejecución en GitHub queda pendiente de subir los cambios; el despliegue automático a un servidor Linux requiere definir ese servidor y conectar sus credenciales. La protección de `main` se configura en GitHub.

## Entregables y planificación

- [Presentación del proyecto en Markdown](docs/Presentacion-del-proyecto.md)
- [Presentación publicada en la Wiki](https://github.com/PachVsus/PF-SIIEC/wiki)
- [GitHub Project Board](https://github.com/users/PachVsus/projects/3)
- [Plan de trabajo y criterios de aceptación](docs/Plan-del-proyecto.md)
- [Manual de desarrollo y operación](docs/Desarrollo.md)

## Estado

Primera implementación local. Aplicación, migraciones y contenedores disponibles. El tablero remoto conserva su estado anterior hasta revisar las evidencias e integrar los cambios. La aplicación es un laboratorio sin autenticación y escucha únicamente en localhost.
