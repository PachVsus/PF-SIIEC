# Desarrollo y operación

## Inicio en Windows

Desde PowerShell en `C:\PF-SIIEC`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Copia la clave generada en `SECRET_KEY` dentro de `.env`. Para PostgreSQL, genera otro valor hexadecimal y colócalo en `POSTGRES_PASSWORD`. No compartas ni subas `.env`.

```powershell
.\.venv\Scripts\python.exe run.py
```

Abre <http://127.0.0.1:8000>. Este modo usa SQLite en `instance/inventory.db` si no defines `DATABASE_URL`. Crea el esquema con Alembic y conserva los datos entre ejecuciones. Para detenerlo, presiona Ctrl+C. El catálogo comienza vacío.

## PostgreSQL con Docker

Inicia Docker Desktop y usa contenedores Linux. Configura `.env` como se indica arriba; usa una contraseña hexadecimal para evitar caracteres reservados en la URL de conexión.

```powershell
docker compose up --build -d --wait
docker compose ps
docker compose logs web
```

La aplicación usa PostgreSQL y se abre en la misma dirección local. El servicio `migrate` aplica migraciones antes de iniciar `web`. `db` no publica puertos al host. No ejecutes ambos modos a la vez: comparten el puerto 8000.

```powershell
docker compose down
```

Esto conserva el volumen `postgres_data`. No añadas `-v` a este comando si necesitas conservar el inventario. SQLite y PostgreSQL tienen bases independientes; cambiar de modo no copia datos.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Por defecto, cada prueba usa una base SQLite temporal. CI ejecuta las mismas pruebas contra PostgreSQL. Para probar PostgreSQL manualmente, define `TEST_DATABASE_URL` apuntando exclusivamente a una base desechable: las pruebas eliminan productos y movimientos de esa base.

Las pruebas comprueban código único, entradas/salidas, rechazo sin cambios, desactivación, concurrencia, persistencia, CSRF y salud. `/health` devuelve 503 si la conexión o la tabla principal no están disponibles.

## Modelo de datos

`products`: código único normalizado a mayúsculas, nombre, stock entero no negativo y estado activo. El código no se modifica después del alta. Las existencias solo cambian mediante movimientos.

`movements`: producto, entrada o salida, cantidad positiva, nota y fecha UTC. Stock e historial se actualizan en una misma transacción. Una actualización condicional en SQL evita salidas que consuman existencias ya utilizadas por otra solicitud.

## Flujo de colaboración

Crear una rama por tarea y un pull request hacia `main`. Revisar pruebas y construcción antes de integrar. En GitHub, configurar controles requeridos `test` y `build` en la protección de `main`; el archivo de CI por sí solo no bloquea integraciones.

El workflow valida pull requests y cambios en `main`. Publica en GHCR únicamente después de que las pruebas y el build pasen en un push a `main`. La etiqueta es el SHA del commit, nunca una etiqueta flotante de producción. La ejecución remota y publicación se verificarán cuando se suban los cambios.

## Despliegue y recuperación

Pendiente definir servidor Linux, acceso y política de aprobación. La entrega automática a ese servidor aún no está conectada. En el servidor se necesitarán Docker, Compose, `.env`, este archivo Compose y credenciales de lectura si el paquete GHCR es privado.

Para desplegar una imagen ya publicada, establecer `APP_IMAGE=ghcr.io/pachvsus/pf-siiec:<sha>` en `.env`, descargarla con `docker compose pull web migrate`, ejecutar `docker compose run --rm migrate` y después `docker compose up -d --no-build --force-recreate web --wait`. Revisar `/health` y probar un movimiento.

Antes de migraciones que cambien datos, crear y verificar un respaldo PostgreSQL. Conservar el SHA anterior. Si la nueva versión falla, restaurar `APP_IMAGE` al SHA anterior y recrear `web` con `--no-deps --no-build --force-recreate`, sin ejecutar migraciones antiguas. Solo es válido si el esquema sigue siendo compatible. Una imagen anterior no deshace cambios en datos o esquema.

## Límites actuales

La aplicación es un laboratorio sin autenticación y está enlazada a localhost. Antes de publicarla para varios usuarios se requiere definir control de acceso y HTTPS. No hay borrado de productos ni edición del historial. Fechas y responsables del plan siguen por definir. No se han marcado tareas remotas como terminadas.

## Referencias técnicas

- [Instalación y entornos virtuales de Flask](https://flask.palletsprojects.com/en/stable/installation/).
- [Actualizaciones condicionales con SQLAlchemy](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html).
