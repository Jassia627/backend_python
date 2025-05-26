# Estructura de la Base de Datos

## Índice
- [Visión General](#visión-general)
- [Tablas Principales](#tablas-principales)
- [Relaciones](#relaciones)
- [Índices y Restricciones](#índices-y-restricciones)
- [Valores por Defecto](#valores-por-defecto)
- [Extensiones](#extensiones)
- [Diagrama Entidad-Relación](#diagrama-entidad-relación)

## Visión General

El Sistema de Permanencia utiliza Supabase como base de datos, que está construido sobre PostgreSQL. La base de datos almacena información sobre estudiantes, programas académicos, servicios de permanencia, intervenciones grupales y estadísticas relacionadas.

## Tablas Principales

### 1. `estudiantes`

Almacena información de los estudiantes registrados en el sistema.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| documento | varchar | NOT NULL | Número de documento de identidad |
| tipo_documento | varchar | NOT NULL | Tipo de documento (CC, TI, etc.) |
| nombres | varchar | NOT NULL | Nombres del estudiante |
| apellidos | varchar | NOT NULL | Apellidos del estudiante |
| correo | varchar | NOT NULL | Correo electrónico |
| telefono | varchar | | Número de teléfono |
| direccion | varchar | | Dirección de residencia |
| programa_academico | varchar | NOT NULL | Programa académico al que pertenece |
| semestre | varchar | NOT NULL | Semestre que cursa |
| estrato | integer | | Estrato socioeconómico |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

### 2. `programas`

Almacena información de los programas académicos.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| nombre | varchar | NOT NULL | Nombre del programa |
| facultad | varchar | NOT NULL | Facultad a la que pertenece |
| nivel | varchar | NOT NULL, DEFAULT 'Pregrado' | Nivel académico (Pregrado, Postgrado, Híbrido) |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

### 3. `servicios`

Almacena información de los servicios ofrecidos.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| codigo | varchar | NOT NULL | Código del servicio |
| nombre | varchar | NOT NULL | Nombre del servicio |
| descripcion | text | | Descripción del servicio |
| facultad | varchar | NOT NULL | Facultad asociada |
| tipo | varchar | | Tipo de servicio |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

### 4. `intervenciones_grupales`

Almacena información de las intervenciones grupales realizadas.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| estudiante_id | uuid | REFERENCES estudiantes(id) | ID del estudiante solicitante |
| fecha_solicitud | date | NOT NULL | Fecha de solicitud |
| fecha_recepcion | date | | Fecha de recepción |
| nombre_docente_permanencia | varchar | NOT NULL | Nombre del docente de permanencia |
| celular_permanencia | varchar | NOT NULL | Celular del docente de permanencia |
| correo_permanencia | varchar | NOT NULL | Correo del docente de permanencia |
| estudiante_programa_academico_permanencia | varchar | NOT NULL | Programa académico del docente de permanencia |
| tipo_poblacion | varchar | NOT NULL | Tipo de población |
| nombre_docente_asignatura | varchar | NOT NULL | Nombre del docente de asignatura |
| celular_docente_asignatura | varchar | NOT NULL | Celular del docente de asignatura |
| correo_docente_asignatura | varchar | NOT NULL | Correo del docente de asignatura |
| estudiante_programa_academico_docente_asignatura | varchar | NOT NULL | Programa académico del docente de asignatura |
| asignatura_intervenir | varchar | NOT NULL | Asignatura a intervenir |
| grupo | varchar | NOT NULL | Grupo |
| semestre | varchar | NOT NULL | Semestre |
| numero_estudiantes | varchar | NOT NULL | Número de estudiantes |
| tematica_sugerida | text | | Temática sugerida |
| fecha_estudiante_programa_academicoda | date | NOT NULL | Fecha programada |
| hora | time | NOT NULL | Hora programada |
| aula | varchar | NOT NULL | Aula |
| bloque | varchar | NOT NULL | Bloque |
| sede | varchar | NOT NULL | Sede |
| estado | varchar | NOT NULL | Estado de la intervención |
| motivo | text | | Motivo de la intervención |
| efectividad | varchar | DEFAULT 'Pendiente evaluación' | Efectividad de la intervención |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

### 5. `permanencia`

Almacena información de los registros de permanencia.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| estudiante_id | uuid | REFERENCES estudiantes(id) | ID del estudiante |
| servicio | varchar | NOT NULL | Servicio utilizado |
| estrato | integer | | Estrato socioeconómico |
| inscritos | integer | | Número de inscritos |
| estudiante_programa_academico | varchar | | Programa académico |
| riesgo_desercion | varchar | | Nivel de riesgo de deserción |
| tipo_vulnerabilidad | varchar | | Tipo de vulnerabilidad |
| periodo | varchar | | Periodo académico |
| semestre | integer | | Semestre |
| matriculados | integer | | Número de matriculados |
| desertores | integer | | Número de desertores |
| graduados | integer | | Número de graduados |
| requiere_tutoria | varchar | | Si requiere tutoría |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

### 6. `asistencias`

Almacena las asistencias a los servicios.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| estudiante_id | uuid | REFERENCES estudiantes(id) | ID del estudiante |
| servicio_id | uuid | REFERENCES servicios(id) | ID del servicio |
| fecha | date | NOT NULL | Fecha de asistencia |
| numero_asistencia | integer | DEFAULT 1 | Número de asistencia |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

### 7. `actas`

Almacena información de las actas generadas.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| tipo | varchar | NOT NULL | Tipo de acta |
| fecha | date | NOT NULL | Fecha del acta |
| descripcion | text | | Descripción del acta |
| estado | varchar | DEFAULT 'Pendiente' | Estado del acta |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

### 8. `software_solicitudes`

Almacena solicitudes relacionadas con software.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| nombre_solicitante | varchar | NOT NULL | Nombre del solicitante |
| correo_solicitante | varchar | NOT NULL | Correo del solicitante |
| telefono_solicitante | varchar | | Teléfono del solicitante |
| programa_academico | varchar | NOT NULL | Programa académico |
| nombre_software | varchar | NOT NULL | Nombre del software |
| version | varchar | | Versión del software |
| justificacion | text | NOT NULL | Justificación de la solicitud |
| estado | varchar | DEFAULT 'Pendiente' | Estado de la solicitud |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

### 9. `asistencias_actividades`

Almacena asistencias a actividades.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | uuid | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único |
| estudiante_id | uuid | REFERENCES estudiantes(id) | ID del estudiante |
| nombre_estudiante | varchar | | Nombre del estudiante |
| numero_documento | varchar | | Número de documento |
| estudiante_programa_academico | varchar | | Programa académico |
| semestre | varchar | | Semestre |
| nombre_actividad | varchar | NOT NULL | Nombre de la actividad |
| modalidad | varchar | | Modalidad (Virtual, Presencial, Híbrida) |
| tipo_actividad | varchar | | Tipo de actividad |
| fecha_actividad | varchar | | Fecha de la actividad |
| hora_inicio | varchar | | Hora de inicio |
| hora_fin | varchar | | Hora de fin |
| modalidad_registro | varchar | | Modalidad de registro (Manual, Digital) |
| observaciones | text | | Observaciones |
| created_at | timestamp with time zone | DEFAULT NOW() | Fecha de creación |
| updated_at | timestamp with time zone | DEFAULT NOW() | Fecha de actualización |

## Relaciones

1. **Estudiantes - Intervenciones Grupales**: Un estudiante puede tener múltiples intervenciones grupales (relación 1:N).
   ```sql
   estudiante_id uuid REFERENCES estudiantes(id) ON DELETE SET NULL
   ```

2. **Estudiantes - Permanencia**: Un estudiante puede tener múltiples registros de permanencia (relación 1:N).
   ```sql
   estudiante_id uuid REFERENCES estudiantes(id) ON DELETE SET NULL
   ```

3. **Estudiantes - Asistencias**: Un estudiante puede tener múltiples asistencias a servicios (relación 1:N).
   ```sql
   estudiante_id uuid REFERENCES estudiantes(id) ON DELETE SET NULL
   ```

4. **Servicios - Asistencias**: Un servicio puede tener múltiples asistencias (relación 1:N).
   ```sql
   servicio_id uuid REFERENCES servicios(id) ON DELETE SET NULL
   ```

5. **Estudiantes - Asistencias Actividades**: Un estudiante puede tener múltiples asistencias a actividades (relación 1:N).
   ```sql
   estudiante_id uuid REFERENCES estudiantes(id) ON DELETE SET NULL
   ```

## Índices y Restricciones

- **Claves Primarias**: Todas las tablas tienen una clave primaria `id` de tipo UUID.
- **Claves Foráneas**: Se utilizan para mantener la integridad referencial entre tablas.
- **Restricciones NOT NULL**: Aplicadas a campos obligatorios como nombres, documentos, etc.
- **Valores por Defecto**: Aplicados a campos como `created_at`, `updated_at`, `estado`, etc.

## Valores por Defecto

- **UUIDs**: Generados automáticamente usando `uuid_generate_v4()`.
- **Timestamps**: `created_at` y `updated_at` se establecen automáticamente a `NOW()`.
- **Estados**: Valores por defecto como 'Pendiente' para estados y 'Pendiente evaluación' para efectividad.
- **Nivel de Programa**: 'Pregrado' como valor por defecto para el nivel de programas académicos.

## Extensiones

- **uuid-ossp**: Utilizada para generar UUIDs automáticamente.
  ```sql
  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
  ```

## Diagrama Entidad-Relación

A continuación se muestra una representación simplificada de las relaciones entre las principales entidades:

```
+-------------+       +--------------------+       +------------+
| estudiantes |------>| intervenciones_grupales |   | programas  |
+-------------+       +--------------------+       +------------+
      |                                                  
      |                +------------+                     
      +--------------->| permanencia|                     
      |                +------------+                     
      |                                                  
      |                +------------+       +------------+
      +--------------->| asistencias|------>| servicios  |
      |                +------------+       +------------+
      |                                                  
      |                +----------------------+           
      +--------------->| asistencias_actividades|         
                       +----------------------+           
```

Este diagrama muestra que:
- Un estudiante puede tener múltiples intervenciones grupales, registros de permanencia, asistencias a servicios y asistencias a actividades.
- Un servicio puede tener múltiples asistencias.
- Los programas académicos son entidades independientes pero relacionadas con estudiantes a través de campos de texto.
