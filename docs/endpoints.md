# Documentación de Endpoints de la API

## Índice
- [Introducción](#introducción)
- [Estudiantes](#estudiantes)
- [Programas](#programas)
- [Servicios](#servicios)
- [Intervenciones Grupales](#intervenciones-grupales)
- [Permanencia](#permanencia)
- [Actas](#actas)
- [Estadísticas](#estadísticas)
- [Importación de Datos](#importación-de-datos)

## Introducción

La API del Sistema de Permanencia de la Universidad Popular del Cesar proporciona acceso a todas las funcionalidades del sistema a través de endpoints RESTful. Todos los endpoints comienzan con el prefijo `/api`.

## Estudiantes

### GET `/api/estudiantes`
- **Descripción**: Obtiene la lista de todos los estudiantes.
- **Respuesta**: Array de objetos estudiante.
- **Filtros**: Soporta filtrado por programa académico, semestre y otros campos.

### GET `/api/estudiantes/{id}`
- **Descripción**: Obtiene un estudiante específico por su ID.
- **Parámetros**: `id` (UUID) - ID del estudiante.
- **Respuesta**: Objeto estudiante.

### POST `/api/estudiantes`
- **Descripción**: Crea un nuevo estudiante.
- **Cuerpo**: Datos del estudiante (documento, nombres, apellidos, correo, programa_academico, semestre, etc.).
- **Respuesta**: Objeto estudiante creado.
- **Validaciones**: Verifica que los campos obligatorios estén presentes y sean válidos.

### PUT `/api/estudiantes/{id}`
- **Descripción**: Actualiza los datos de un estudiante existente.
- **Parámetros**: `id` (UUID) - ID del estudiante.
- **Cuerpo**: Datos a actualizar.
- **Respuesta**: Objeto estudiante actualizado.

### DELETE `/api/estudiantes/{id}`
- **Descripción**: Elimina un estudiante.
- **Parámetros**: `id` (UUID) - ID del estudiante.
- **Respuesta**: Confirmación de eliminación.

## Programas

### GET `/api/programas`
- **Descripción**: Obtiene la lista de todos los programas académicos.
- **Respuesta**: Array de objetos programa.
- **Filtros**: Soporta filtrado por facultad y nivel.

### GET `/api/programas/{id}`
- **Descripción**: Obtiene un programa específico por su ID.
- **Parámetros**: `id` (UUID) - ID del programa.
- **Respuesta**: Objeto programa.

### POST `/api/programas`
- **Descripción**: Crea un nuevo programa académico.
- **Cuerpo**: Datos del programa (nombre, facultad, nivel, etc.).
- **Respuesta**: Objeto programa creado.
- **Validaciones**: Verifica que los campos obligatorios estén presentes y sean válidos.

### PUT `/api/programas/{id}`
- **Descripción**: Actualiza los datos de un programa existente.
- **Parámetros**: `id` (UUID) - ID del programa.
- **Cuerpo**: Datos a actualizar.
- **Respuesta**: Objeto programa actualizado.

### DELETE `/api/programas/{id}`
- **Descripción**: Elimina un programa.
- **Parámetros**: `id` (UUID) - ID del programa.
- **Respuesta**: Confirmación de eliminación.

## Servicios

### GET `/api/servicios`
- **Descripción**: Obtiene la lista de todos los servicios disponibles.
- **Respuesta**: Array de objetos servicio.
- **Filtros**: Soporta filtrado por tipo de servicio y facultad.

### GET `/api/servicios/{id}`
- **Descripción**: Obtiene un servicio específico por su ID.
- **Parámetros**: `id` (UUID) - ID del servicio.
- **Respuesta**: Objeto servicio.

### POST `/api/servicios`
- **Descripción**: Crea un nuevo servicio.
- **Cuerpo**: Datos del servicio (código, nombre, descripción, etc.).
- **Respuesta**: Objeto servicio creado.
- **Validaciones**: Verifica que los campos obligatorios estén presentes y sean válidos.

### PUT `/api/servicios/{id}`
- **Descripción**: Actualiza los datos de un servicio existente.
- **Parámetros**: `id` (UUID) - ID del servicio.
- **Cuerpo**: Datos a actualizar.
- **Respuesta**: Objeto servicio actualizado.

### DELETE `/api/servicios/{id}`
- **Descripción**: Elimina un servicio.
- **Parámetros**: `id` (UUID) - ID del servicio.
- **Respuesta**: Confirmación de eliminación.

### GET `/api/servicios/asistencias`
- **Descripción**: Obtiene todas las asistencias a servicios.
- **Respuesta**: Array de objetos asistencia.
- **Filtros**: Soporta filtrado por servicio, fecha y estudiante.

### POST `/api/servicios/asistencias`
- **Descripción**: Registra una nueva asistencia a un servicio.
- **Cuerpo**: Datos de la asistencia (estudiante_id, servicio_id, fecha, etc.).
- **Respuesta**: Objeto asistencia creado.

### GET `/api/software-solicitudes`
- **Descripción**: Obtiene todas las solicitudes de software.
- **Respuesta**: Array de objetos solicitud de software.

### GET `/api/software-solicitudes/{id}`
- **Descripción**: Obtiene una solicitud de software específica.
- **Parámetros**: `id` (UUID) - ID de la solicitud.
- **Respuesta**: Objeto solicitud de software.

### POST `/api/software-solicitudes`
- **Descripción**: Crea una nueva solicitud de software.
- **Cuerpo**: Datos de la solicitud.
- **Respuesta**: Objeto solicitud creado.

### PUT `/api/software-solicitudes/{id}`
- **Descripción**: Actualiza una solicitud de software existente.
- **Parámetros**: `id` (UUID) - ID de la solicitud.
- **Cuerpo**: Datos a actualizar.
- **Respuesta**: Objeto solicitud actualizado.

### DELETE `/api/software-solicitudes/{id}`
- **Descripción**: Elimina una solicitud de software.
- **Parámetros**: `id` (UUID) - ID de la solicitud.
- **Respuesta**: Confirmación de eliminación.

### GET `/api/asistencias-actividades`
- **Descripción**: Obtiene todas las asistencias a actividades.
- **Respuesta**: Array de objetos asistencia a actividad.

### POST `/api/asistencias-actividades`
- **Descripción**: Registra una nueva asistencia a una actividad.
- **Cuerpo**: Datos de la asistencia.
- **Respuesta**: Objeto asistencia creado.
- **Validaciones**: Incluye validaciones para campos como nombres, números de documento, semestre, etc.

## Intervenciones Grupales

### GET `/api/intervenciones-grupales`
- **Descripción**: Obtiene todas las intervenciones grupales.
- **Respuesta**: Array de objetos intervención grupal.
- **Filtros**: Soporta filtrado por estado, fecha y programa académico.

### GET `/api/intervenciones-grupales/{id}`
- **Descripción**: Obtiene una intervención grupal específica.
- **Parámetros**: `id` (UUID) - ID de la intervención.
- **Respuesta**: Objeto intervención grupal.

### POST `/api/intervenciones-grupales`
- **Descripción**: Crea una nueva intervención grupal.
- **Cuerpo**: Datos de la intervención (estudiante_id, fecha_solicitud, nombre_docente_permanencia, etc.).
- **Respuesta**: Objeto intervención creado.
- **Validaciones**: Verifica que los campos obligatorios estén presentes y sean válidos.

### PUT `/api/intervenciones-grupales/{id}`
- **Descripción**: Actualiza una intervención grupal existente.
- **Parámetros**: `id` (UUID) - ID de la intervención.
- **Cuerpo**: Datos a actualizar.
- **Respuesta**: Objeto intervención actualizado.

### DELETE `/api/intervenciones-grupales/{id}`
- **Descripción**: Elimina una intervención grupal.
- **Parámetros**: `id` (UUID) - ID de la intervención.
- **Respuesta**: Confirmación de eliminación.

## Permanencia

### GET `/api/permanencia`
- **Descripción**: Obtiene todos los registros de permanencia.
- **Respuesta**: Array de objetos permanencia.
- **Filtros**: Soporta filtrado por servicio, periodo, programa académico y riesgo de deserción.

### GET `/api/permanencia/{id}`
- **Descripción**: Obtiene un registro de permanencia específico.
- **Parámetros**: `id` (UUID) - ID del registro.
- **Respuesta**: Objeto permanencia.

### POST `/api/permanencia`
- **Descripción**: Crea un nuevo registro de permanencia.
- **Cuerpo**: Datos del registro (estudiante_id, servicio, estrato, riesgo_desercion, etc.).
- **Respuesta**: Objeto permanencia creado.

### PUT `/api/permanencia/{id}`
- **Descripción**: Actualiza un registro de permanencia existente.
- **Parámetros**: `id` (UUID) - ID del registro.
- **Cuerpo**: Datos a actualizar.
- **Respuesta**: Objeto permanencia actualizado.

### DELETE `/api/permanencia/{id}`
- **Descripción**: Elimina un registro de permanencia.
- **Parámetros**: `id` (UUID) - ID del registro.
- **Respuesta**: Confirmación de eliminación.

## Actas

### GET `/api/actas`
- **Descripción**: Obtiene todas las actas.
- **Respuesta**: Array de objetos acta.
- **Filtros**: Soporta filtrado por tipo, fecha y estado.

### GET `/api/actas/{id}`
- **Descripción**: Obtiene un acta específica.
- **Parámetros**: `id` (UUID) - ID del acta.
- **Respuesta**: Objeto acta.

### POST `/api/actas`
- **Descripción**: Crea una nueva acta.
- **Cuerpo**: Datos del acta (tipo, fecha, descripción, etc.).
- **Respuesta**: Objeto acta creado.

### PUT `/api/actas/{id}`
- **Descripción**: Actualiza un acta existente.
- **Parámetros**: `id` (UUID) - ID del acta.
- **Cuerpo**: Datos a actualizar.
- **Respuesta**: Objeto acta actualizado.

### DELETE `/api/actas/{id}`
- **Descripción**: Elimina un acta.
- **Parámetros**: `id` (UUID) - ID del acta.
- **Respuesta**: Confirmación de eliminación.

## Estadísticas

### GET `/api/datos-permanencia`
- **Descripción**: Obtiene datos para el gráfico de estrato por servicio.
- **Respuesta**: Array de objetos con datos para el componente EstratoServicioChart.jsx.

### GET `/api/programas-distribucion`
- **Descripción**: Obtiene datos para el gráfico de distribución por programa académico.
- **Respuesta**: Datos para el componente PieChartProgramas.jsx.

### GET `/api/riesgo-desercion`
- **Descripción**: Obtiene datos para el gráfico de riesgo de deserción.
- **Respuesta**: Datos para el componente RiesgoDesercionChart.jsx.

## Importación de Datos

### POST `/api/upload-csv`
- **Descripción**: Importa datos desde un archivo CSV.
- **Parámetros**: 
  - `file` (File) - Archivo CSV a importar.
  - `tipo` (String) - Tipo de datos a importar (estudiantes, programas, servicios, etc.).
- **Respuesta**: Resumen de la importación (registros creados, actualizados, errores).
- **Procesamiento**: 
  - Valida el formato del CSV.
  - Procesa cada fila según el tipo de datos.
  - Maneja valores faltantes con valores por defecto.
  - Crea o actualiza registros en la base de datos.

### POST `/api/importar-intervenciones`
- **Descripción**: Importa intervenciones grupales desde un archivo CSV.
- **Parámetros**: 
  - `file` (File) - Archivo CSV a importar.
- **Respuesta**: Resumen de la importación (intervenciones creadas, errores).
- **Procesamiento**: 
  - Procesa cada fila para crear intervenciones grupales.
  - Valida y transforma los datos según sea necesario.
  - Maneja valores faltantes con valores por defecto.
