# Documentación de la Base de Datos

## Estructura de Tablas

El sistema utiliza una base de datos PostgreSQL en Supabase con las siguientes tablas principales:

### Tabla `estudiantes`

Almacena la información básica de los estudiantes.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| documento | VARCHAR | Número de documento del estudiante | NOT NULL |
| tipo_documento | VARCHAR | Tipo de documento (CC, TI, etc.) | NOT NULL |
| nombres | VARCHAR | Nombres del estudiante | NOT NULL |
| apellidos | VARCHAR | Apellidos del estudiante | NOT NULL |
| correo | VARCHAR | Correo electrónico | NOT NULL |
| telefono | VARCHAR | Número de teléfono | NULL |
| direccion | VARCHAR | Dirección de residencia | NULL |
| programa_academico | VARCHAR | Programa académico al que pertenece | NOT NULL |
| semestre | INTEGER | Semestre que cursa actualmente | NOT NULL |
| estrato | INTEGER | Estrato socioeconómico | NULL |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `povau`

Programa de Orientación Vocacional y Adaptación a la Universidad.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| tipo_participante | VARCHAR | Tipo de participante | NOT NULL |
| fecha_ingreso | DATE | Fecha de ingreso al programa | NULL |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `poa`

Plan Operativo Anual.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| ciclo_formacion | VARCHAR | Ciclo de formación | NOT NULL |
| nombre_asignatura | VARCHAR | Nombre de la asignatura | NULL |
| fecha | DATE | Fecha del registro | NULL |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `comedor_universitario`

Gestión del comedor universitario.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| condicion_socioeconomica | VARCHAR | Condición socioeconómica | NOT NULL |
| fecha_solicitud | DATE | Fecha de solicitud | NULL |
| aprobado | BOOLEAN | Estado de aprobación | DEFAULT FALSE |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `registro_beneficios`

Registro de beneficios otorgados a estudiantes.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| fecha_inscripcion | DATE | Fecha de inscripción | NOT NULL |
| estado_solicitud | BOOLEAN | Estado de la solicitud | DEFAULT FALSE |
| periodo_academico | VARCHAR | Periodo académico | NULL |
| fecha_inicio | DATE | Fecha de inicio del beneficio | NULL |
| fecha_finalizacion | DATE | Fecha de finalización del beneficio | NULL |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `solicitudes_atencion`

Solicitudes de atención individual.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| fecha_atencion | DATE | Fecha de atención | NOT NULL |
| motivo_atencion | VARCHAR | Motivo de la atención | DEFAULT 'general' |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `intervenciones_grupales`

Intervenciones grupales realizadas.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| fecha_solicitud | DATE | Fecha de solicitud | NOT NULL |
| fecha_recepcion | DATE | Fecha de recepción | NULL |
| estado | VARCHAR | Estado de la intervención | DEFAULT 'pendiente' |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `remisiones_psicologicas`

Remisiones psicológicas.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| fecha_remision | DATE | Fecha de remisión | NOT NULL |
| tipo_remision | VARCHAR | Tipo de remisión | DEFAULT 'general' |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `formatos_asistencia`

Formatos de asistencia a actividades.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| numero_asistencia | INTEGER | Número de asistencia | DEFAULT 1 |
| fecha | DATE | Fecha de asistencia | NULL |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `tutorias_academicas`

Tutorías académicas realizadas.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| estudiante_id | UUID | ID del estudiante | FOREIGN KEY |
| fecha_tutoria | DATE | Fecha de la tutoría | NOT NULL |
| asignatura | VARCHAR | Asignatura | NULL |
| tutor | VARCHAR | Nombre del tutor | NULL |
| observaciones | TEXT | Observaciones de la tutoría | NULL |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

### Tabla `permanencia`

Datos agregados para estadísticas de permanencia.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | UUID | Identificador único | PRIMARY KEY |
| servicio | VARCHAR | Servicio utilizado | NOT NULL |
| estrato | INTEGER | Estrato socioeconómico | NULL |
| inscritos | INTEGER | Número de inscritos | DEFAULT 0 |
| estudiante_programa_academico | VARCHAR | Programa académico | NULL |
| riesgo_desercion | VARCHAR | Nivel de riesgo de deserción | NULL |
| tipo_vulnerabilidad | VARCHAR | Tipo de vulnerabilidad | NULL |
| periodo | VARCHAR | Periodo académico | NULL |
| semestre | INTEGER | Semestre | NULL |
| matriculados | INTEGER | Número de matriculados | DEFAULT 0 |
| desertores | INTEGER | Número de desertores | DEFAULT 0 |
| graduados | INTEGER | Número de graduados | DEFAULT 0 |
| requiere_tutoria | VARCHAR | Indica si requiere tutoría | NULL |
| created_at | TIMESTAMP | Fecha de creación del registro | DEFAULT NOW() |
| updated_at | TIMESTAMP | Fecha de última actualización | DEFAULT NOW() |

## Proceso de Inserción de Datos

### Carga de CSV

Cuando se carga un archivo CSV a través del endpoint `/upload-csv`, el sistema realiza las siguientes operaciones en la base de datos:

1. **Estudiantes**:
   - Busca si el estudiante ya existe por número de documento
   - Si existe, utiliza su ID para las operaciones subsiguientes
   - Si no existe, crea un nuevo registro en la tabla `estudiantes`

2. **Servicios específicos**:
   - Si el CSV contiene datos de POVAU, crea registros en la tabla `povau`
   - Si el CSV contiene datos de POA, crea registros en la tabla `poa`
   - Si el CSV contiene datos de Comedor Universitario, crea registros en la tabla `comedor_universitario`
   - Si el CSV contiene datos de Beneficios, crea registros en la tabla `registro_beneficios`
   - Si el CSV contiene datos de Atención Individual, crea registros en la tabla `solicitudes_atencion`
   - Si el CSV contiene datos de Intervención Grupal, crea registros en la tabla `intervenciones_grupales`
   - Si el CSV contiene datos de Remisión Psicológica, crea registros en la tabla `remisiones_psicologicas`
   - Si el CSV contiene datos de Asistencia, crea registros en la tabla `formatos_asistencia`

3. **Estadísticas**:
   - Por cada estudiante procesado, crea un registro en la tabla `permanencia` con datos agregados
   - Estos datos se utilizan para alimentar los gráficos del dashboard

### Conversión de Datos

El sistema realiza las siguientes conversiones antes de insertar los datos:

- **Fechas**: Convierte fechas de formato DD-MM-YYYY a YYYY-MM-DD
- **Valores booleanos**: Convierte valores como "Si"/"No" o True/False a valores booleanos
- **Valores numéricos**: Asegura que los campos numéricos contengan valores válidos

### Manejo de Errores

Si ocurre un error durante la inserción:

1. El error se registra en el log del sistema
2. Se continúa con el procesamiento de los demás registros
3. Al final, se retorna un resumen con los registros procesados correctamente y los errores encontrados

## Relaciones entre Tablas

Todas las tablas secundarias (`povau`, `poa`, `comedor_universitario`, etc.) tienen una relación de clave foránea con la tabla `estudiantes` a través del campo `estudiante_id`. Estas relaciones están configuradas con la opción `ON DELETE CASCADE`, lo que significa que si se elimina un estudiante, todos sus registros relacionados también se eliminarán automáticamente.
