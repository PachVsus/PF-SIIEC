# Verificación local — PF-SIIEC

Fecha: 7 de noviembre de 2026.

Implementación guardada en `C:\PF-SIIEC`.

## Resultados

| Comprobación | Resultado |
|---|---|
| Pruebas SQLite con Python 3.14 | 15 aprobadas |
| Pruebas PostgreSQL 17 en base temporal separada | 15 aprobadas |
| Construcción Docker con Python 3.13 | Correcta |
| Migración inicial Alembic | Aplicada en PostgreSQL |
| Docker Compose | Configuración válida; db y web saludables |
| GET / | HTTP 200; formulario con CSRF |
| GET /health | HTTP 200, status ok, version local |
| Git diff --check | Sin errores de espacios |

Las pruebas cubren productos duplicados, búsqueda, movimientos válidos e inválidos, desactivación/reactivación, salidas concurrentes, persistencia entre instancias, CSRF y salud sin esquema. La base temporal de pruebas fue retirada. La base de la aplicación permanece en el volumen Docker, con el catálogo vacío para comenzar.

## Uso

Abre [la aplicación local](http://127.0.0.1:8000). Docker Desktop debe permanecer iniciado. Desde `C:\PF-SIIEC`, usa `docker compose down` para detener y `docker compose up -d --wait` para volver a iniciar. No añadas `-v` si necesitas conservar los datos.

El manual está en `C:\PF-SIIEC\docs\Desarrollo.md`. La configuración local `.env` contiene claves generadas y está excluida de Git.

## Pendiente de integración

Los cambios permanecen locales sin commit ni push. El workflow de GitHub Actions está escrito, pero no se ha ejecutado en GitHub ni publicado una imagen GHCR. Falta definir el servidor Linux, acceso, protección de main y despliegue automático remoto. El tablero de GitHub no se modificó en esta etapa.

