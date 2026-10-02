# Plan de proyecto — PF-SIIEC

**Tablero:** [GitHub Projects](https://github.com/users/PachVsus/projects/3)  
**Wiki:** [Presentación del proyecto](https://github.com/PachVsus/PF-SIIEC/wiki)  
**Duración propuesta:** cuatro semanas; fechas y responsables por definir.

## Flujo de trabajo

Pendiente → En progreso → En revisión → Terminado.

Todas las tareas comienzan en Pendiente. Para mover una tarea a Terminado, verificar sus criterios y enlazar evidencia. Las tareas opcionales se agregarán después de completar el alcance mínimo.

## Tareas

| Tarea | Semana | Dependencias |
|---|---|---|
| [T01 · Definir requisitos y arquitectura](https://github.com/PachVsus/PF-SIIEC/issues/1) | 1 | Ninguna |
| [T02 · Preparar repositorio y flujo de colaboración](https://github.com/PachVsus/PF-SIIEC/issues/2) | 1 | T01 |
| [T03 · Diseñar modelo de datos y migraciones](https://github.com/PachVsus/PF-SIIEC/issues/3) | 1 | T01 |
| [T04 · Implementar gestión de productos](https://github.com/PachVsus/PF-SIIEC/issues/4) | 1 | T02, T03 |
| [T05 · Implementar entradas, salidas e historial](https://github.com/PachVsus/PF-SIIEC/issues/5) | 2 | T03, T04 |
| [T06 · Agregar pruebas automatizadas](https://github.com/PachVsus/PF-SIIEC/issues/6) | 2 | T04, T05 |
| [T07 · Contenerizar aplicación y PostgreSQL](https://github.com/PachVsus/PF-SIIEC/issues/7) | 2 | T04, T05 |
| [T08 · Configurar CI y controles de integración](https://github.com/PachVsus/PF-SIIEC/issues/8) | 3 | T06, T07 |
| [T09 · Publicar imágenes versionadas en GHCR](https://github.com/PachVsus/PF-SIIEC/issues/9) | 3 | T08 |
| [T10 · Automatizar despliegue en Linux](https://github.com/PachVsus/PF-SIIEC/issues/10) | 3 | T07, T09 |
| [T11 · Verificar salud, persistencia y recuperación](https://github.com/PachVsus/PF-SIIEC/issues/11) | 4 | T10 |
| [T12 · Documentar operación y reunir evidencias](https://github.com/PachVsus/PF-SIIEC/issues/12) | 4 | T08, T10, T11 |
| [T13 · Preparar demostración y entrega final](https://github.com/PachVsus/PF-SIIEC/issues/13) | 4 | T12 |

## Criterios de aceptación

### T01 · Definir requisitos y arquitectura

Documentar alcance, reglas del inventario y arquitectura; definir servidor, recursos y versiones.

- [ ] Requisitos y exclusiones documentados
- [ ] Diagrama de arquitectura disponible
- [ ] Ambiente de despliegue definido

### T02 · Preparar repositorio y flujo de colaboración

Establecer estructura, convenciones de ramas, pull requests y configuración de ejemplo sin secretos.

- [ ] Estructura y README definidos
- [ ] .gitignore y .env.example disponibles
- [ ] Flujo de colaboración documentado

### T03 · Diseñar modelo de datos y migraciones

Modelar productos y movimientos en PostgreSQL; definir código único, cantidades y consistencia transaccional.

- [ ] Modelo documentado
- [ ] Migraciones reproducibles
- [ ] Restricciones de integridad definidas

### T04 · Implementar gestión de productos

Crear interfaz Flask para alta, consulta, edición y desactivación de productos.

- [ ] CRUD funcional
- [ ] Código duplicado rechazado
- [ ] Productos desactivados conservan historial

### T05 · Implementar entradas, salidas e historial

Registrar movimientos y consultar existencias; impedir stock negativo y cantidades no positivas.

- [ ] Entradas y salidas actualizan stock
- [ ] Salida excesiva rechazada sin modificar datos
- [ ] Historial consultable
- [ ] Operación transaccional consistente

### T06 · Agregar pruebas automatizadas

Validar catálogo y movimientos con pruebas aisladas y reproducibles.

- [ ] Pruebas de entradas y salidas válidas pasan
- [ ] Stock insuficiente y cantidades inválidas probados
- [ ] Datos aislados entre pruebas
- [ ] Comando de pruebas documentado

### T07 · Contenerizar aplicación y PostgreSQL

Crear Dockerfile y Docker Compose con volumen persistente y configuración externa.

- [ ] Entorno inicia desde un clon limpio
- [ ] Base de datos usa volumen persistente
- [ ] Secretos excluidos de la imagen y del repositorio
- [ ] Servicios se comunican correctamente

### T08 · Configurar CI y controles de integración

Ejecutar pruebas y construcción en pull requests; configurar controles requeridos de main.

- [ ] Pipeline ejecuta pruebas y build
- [ ] Cambio defectuoso produce fallo
- [ ] Protección de main exige verificaciones
- [ ] PR no usa secretos de despliegue

### T09 · Publicar imágenes versionadas en GHCR

Publicar al integrar en main y etiquetar imágenes con el identificador del commit.

- [ ] Imagen publicada en GHCR
- [ ] Etiqueta identifica commit
- [ ] Permisos del workflow limitados
- [ ] Versión recuperable documentada

### T10 · Automatizar despliegue en Linux

Preparar servidor y desplegar la imagen versionada desde GitHub Actions con credenciales protegidas.

- [ ] Servidor ejecuta Compose
- [ ] Pipeline despliega imagen correcta
- [ ] Credenciales fuera del repositorio
- [ ] Actualización conserva volumen

### T11 · Verificar salud, persistencia y recuperación

Agregar verificación de salud, probar actualización y ensayar recuperación a imagen anterior compatible.

- [ ] Endpoint de salud verificado
- [ ] Datos conservados entre versiones
- [ ] Recuperación ensayada
- [ ] Límites de migración y respaldo documentados

### T12 · Documentar operación y reunir evidencias

Completar manual de instalación, despliegue, secretos, recuperación y evidencias del pipeline.

- [ ] Manual permite reproducir entorno
- [ ] Evidencia de fallo y éxito disponible
- [ ] Evidencia de persistencia disponible
- [ ] Wiki enlaza documentación

### T13 · Preparar demostración y entrega final

Ensayar demostración: inventario, PR fallido, corrección, despliegue y persistencia; revisar PDF, MD y tablero.

- [ ] Guion ensayado
- [ ] PDF y MD revisados
- [ ] Tablero refleja progreso real
- [ ] Repositorio y entregables enlazados
