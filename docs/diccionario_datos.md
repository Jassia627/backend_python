# Diccionario de Datos - Sistema de Permanencia Universitaria

## Visión General

El Sistema de Permanencia Universitaria utiliza Supabase como base de datos, construido sobre PostgreSQL. El sistema está diseñado para gestionar información sobre estudiantes, programas académicos, servicios de permanencia, intervenciones grupales y estadísticas relacionadas con la permanencia estudiantil.

## Tablas Principales

### 1. `estudiantes`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del estudiante |
| documento | TEXT | NOT NULL | Número de documento de identidad |
| tipo_documento | TEXT | NOT NULL | Tipo de documento (CC, TI, etc.) |
| nombres | TEXT | NOT NULL | Nombres del estudiante |
| apellidos | TEXT | NOT NULL | Apellidos del estudiante |
| correo | TEXT | NOT NULL | Correo electrónico institucional |
| telefono | TEXT | NULL | Número de teléfono |
| direccion | TEXT | NULL | Dirección de residencia |
| programa_academico | TEXT | NOT NULL | Programa académico al que pertenece |
| semestre | TEXT | NOT NULL | Semestre que cursa el estudiante |
| estrato | INTEGER | NULL | Estrato socioeconómico (1-6) |
| riesgo_desercion | TEXT | NULL | Nivel de riesgo (muy bajo, bajo, medio, alto, muy alto) |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 2. `programas`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del programa |
| codigo | TEXT | NOT NULL | Código del programa académico |
| nombre | TEXT | NOT NULL | Nombre del programa académico |
| facultad | TEXT | NOT NULL | Facultad a la que pertenece el programa |
| nivel | TEXT | NOT NULL, DEFAULT 'Pregrado' | Nivel académico (Pregrado, Posgrado, etc.) |
| modalidad | TEXT | NULL | Modalidad (Presencial, Virtual, etc.) |
| estado | BOOLEAN | DEFAULT TRUE | Estado activo/inactivo del programa |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 3. `usuarios`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del usuario |
| nombre | TEXT | NOT NULL | Nombre del usuario |
| apellido | TEXT | NOT NULL | Apellido del usuario |
| email | TEXT | NOT NULL | Correo electrónico |
| password | TEXT | NOT NULL | Contraseña (hash) |
| rol | TEXT | NOT NULL | Rol del usuario (Admin, Docente, Estudiante, etc.) |
| estado | BOOLEAN | DEFAULT TRUE | Estado activo/inactivo del usuario |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 4. `servicios`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del servicio |
| codigo | TEXT | NOT NULL | Código del servicio |
| nombre | TEXT | NOT NULL | Nombre del servicio |
| descripcion | TEXT | NULL | Descripción del servicio |
| facultad | TEXT | NOT NULL | Facultad asociada |
| tipo | TEXT | NULL | Tipo de servicio (Psicología, Tutoría, etc.) |
| estado | BOOLEAN | DEFAULT TRUE | Estado activo/inactivo del servicio |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

## Servicios de Permanencia

### 5.1. `tutorias_academicas` (POA)

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la tutoría |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| nivel_riesgo | TEXT | NOT NULL | Nivel de riesgo académico |
| requiere_tutoria | BOOLEAN | DEFAULT FALSE | Indica si requiere tutoría |
| fecha_asignacion | TEXT | NOT NULL | Fecha de asignación de la tutoría |
| acciones_apoyo | TEXT | NULL | Acciones de apoyo recomendadas |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 5.2. `asesorias_psicologicas` (POPS)

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la asesoría |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| motivo_intervencion | TEXT | NOT NULL | Motivo de la intervención psicológica |
| tipo_intervencion | TEXT | NOT NULL | Tipo de intervención |
| fecha_atencion | TEXT | NOT NULL | Fecha de atención |
| seguimiento | TEXT | NULL | Observaciones de seguimiento |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 5.3. `orientaciones_vocacionales` (POVAU)

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la orientación |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| tipo_participante | TEXT | NOT NULL | Tipo de participante |
| riesgo_spadies | TEXT | NOT NULL | Nivel de riesgo según SPADIES |
| fecha_ingreso_programa | TEXT | NOT NULL | Fecha de ingreso al programa |
| observaciones | TEXT | NULL | Observaciones adicionales |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 5.4. `comedores_universitarios`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del registro |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| condicion_socioeconomica | TEXT | NOT NULL | Condición socioeconómica |
| fecha_solicitud | TEXT | NOT NULL | Fecha de solicitud |
| aprobado | BOOLEAN | DEFAULT FALSE | Estado de aprobación |
| tipo_comida | TEXT | NOT NULL | Tipo de comida (Almuerzo, etc.) |
| raciones_asignadas | INTEGER | NOT NULL | Número de raciones asignadas |
| observaciones | TEXT | NULL | Observaciones adicionales |
| tipo_subsidio | TEXT | NULL | Tipo de subsidio (Completo, Parcial, Regular) |
| periodo_academico | TEXT | NULL | Periodo académico |
| estrato | INTEGER | NULL | Estrato socioeconómico |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 5.5. `apoyos_socioeconomicos`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del apoyo |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| tipo_vulnerabilidad | TEXT | NULL | Tipo de vulnerabilidad |
| observaciones | TEXT | NULL | Observaciones adicionales |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 5.6. `talleres_habilidades`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del taller |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| nombre_taller | TEXT | NOT NULL | Nombre del taller |
| fecha_taller | TEXT | NOT NULL | Fecha del taller |
| observaciones | TEXT | NULL | Observaciones adicionales |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 5.7. `seguimientos_academicos`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del seguimiento |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| estado_participacion | TEXT | NOT NULL | Estado de participación |
| observaciones_permanencia | TEXT | NOT NULL | Observaciones de permanencia |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

## Tablas de Gestión

### 6.1. `remisiones_psicologicas`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la remisión |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| nombre_estudiante | TEXT | NOT NULL | Nombre completo del estudiante |
| numero_documento | TEXT | NOT NULL | Número de documento |
| programa_academico | TEXT | NOT NULL | Programa académico |
| semestre | TEXT | NOT NULL | Semestre que cursa |
| motivo_remision | TEXT | NOT NULL | Motivo de la remisión |
| docente_remite | TEXT | NOT NULL | Nombre del docente que remite |
| correo_docente | TEXT | NOT NULL | Correo del docente |
| telefono_docente | TEXT | NOT NULL | Teléfono del docente |
| fecha | TEXT | NOT NULL | Fecha de la remisión |
| hora | TEXT | NOT NULL | Hora de la remisión |
| tipo_remision | TEXT | NOT NULL | Tipo de remisión |
| fecha_remision | TEXT | NOT NULL | Fecha de remisión |
| observaciones | TEXT | NULL | Observaciones adicionales |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.2. `intervenciones_grupales`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la intervención |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| fecha_solicitud | TEXT | NOT NULL | Fecha de solicitud |
| fecha_recepcion | TEXT | NULL | Fecha de recepción |
| nombre_docente_permanencia | TEXT | NOT NULL | Nombre del docente de permanencia |
| celular_permanencia | TEXT | NOT NULL | Celular de contacto de permanencia |
| correo_permanencia | TEXT | NOT NULL | Correo de permanencia |
| estudiante_programa_academico_permanencia | TEXT | NOT NULL | Programa académico |
| tipo_poblacion | TEXT | NOT NULL | Tipo de población |
| nombre_docente_asignatura | TEXT | NOT NULL | Nombre del docente de asignatura |
| celular_docente_asignatura | TEXT | NOT NULL | Celular del docente |
| correo_docente_asignatura | TEXT | NOT NULL | Correo del docente |
| estudiante_programa_academico_docente_asignatura | TEXT | NOT NULL | Programa del docente |
| asignatura_intervenir | TEXT | NOT NULL | Asignatura a intervenir |
| grupo | TEXT | NOT NULL | Grupo |
| semestre | TEXT | NOT NULL | Semestre |
| numero_estudiantes | TEXT | NOT NULL | Número de estudiantes |
| tematica_sugerida | TEXT | NULL | Temática sugerida |
| fecha_estudiante_programa_academicoda | TEXT | NOT NULL | Fecha programada |
| hora | TEXT | NOT NULL | Hora |
| aula | TEXT | NOT NULL | Aula |
| bloque | TEXT | NOT NULL | Bloque |
| sede | TEXT | NOT NULL | Sede |
| estado | TEXT | NOT NULL | Estado de la intervención |
| motivo | TEXT | NULL | Motivo |
| efectividad | TEXT | DEFAULT 'Pendiente evaluación' | Efectividad de la intervención |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.3. `registro_beneficios`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del registro |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| fecha_inscripcion | TEXT | NOT NULL | Fecha de inscripción |
| estado_solicitud | BOOLEAN | NOT NULL | Estado de la solicitud |
| periodo_academico | TEXT | NULL | Periodo académico |
| fecha_inicio | TEXT | NULL | Fecha de inicio del servicio |
| fecha_finalizacion | TEXT | NULL | Fecha de finalización del servicio |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.4. `solicitudes_atencion`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la solicitud |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| fecha_atencion | TEXT | NOT NULL | Fecha de atención |
| motivo_atencion | TEXT | NOT NULL | Motivo de la atención |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.5. `formatos_asistencia`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del formato |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| numero_asistencia | INTEGER | NOT NULL | Número de asistencia |
| fecha | TEXT | NULL | Fecha de asistencia |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.6. `permanencia`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del registro |
| servicio | TEXT | NOT NULL | Tipo de servicio |
| estrato | INTEGER | NOT NULL | Estrato socioeconómico |
| inscritos | INTEGER | NOT NULL | Número de inscritos |
| estudiante_programa_academico | TEXT | NOT NULL | Programa académico |
| riesgo_desercion | TEXT | NOT NULL | Nivel de riesgo de deserción |
| tipo_vulnerabilidad | TEXT | NOT NULL | Tipo de vulnerabilidad |
| periodo | TEXT | NOT NULL | Periodo académico |
| semestre | INTEGER | NOT NULL | Semestre |
| matriculados | INTEGER | NOT NULL | Número de matriculados |
| desertores | INTEGER | NOT NULL | Número de desertores |
| graduados | INTEGER | NOT NULL | Número de graduados |
| requiere_tutoria | TEXT | NOT NULL | Indica si requiere tutoría |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.7. `asistencias`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la asistencia |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| servicio_id | UUID | FOREIGN KEY | ID del servicio |
| fecha | TIMESTAMP | NOT NULL | Fecha y hora de la asistencia |
| numero_asistencia | INTEGER | DEFAULT 1 | Número de asistencia |
| observaciones | TEXT | NULL | Observaciones adicionales |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.8. `asistencias_actividades`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la asistencia a actividad |
| estudiante_id | UUID | FOREIGN KEY | ID del estudiante |
| actividad_id | UUID | FOREIGN KEY | ID de la actividad |
| fecha | TIMESTAMP | NOT NULL | Fecha y hora de la asistencia |
| observaciones | TEXT | NULL | Observaciones adicionales |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.9. `actas`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único del acta |
| titulo | TEXT | NOT NULL | Título del acta |
| descripcion | TEXT | NOT NULL | Descripción del acta |
| fecha | TIMESTAMP | NOT NULL | Fecha del acta |
| responsable | TEXT | NOT NULL | Responsable del acta |
| estado | TEXT | DEFAULT 'Pendiente' | Estado del acta (Pendiente, Aprobada, Rechazada) |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

### 6.10. `software_solicitudes`

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único de la solicitud |
| titulo | TEXT | NOT NULL | Título de la solicitud |
| descripcion | TEXT | NOT NULL | Descripción de la solicitud |
| solicitante | TEXT | NOT NULL | Nombre del solicitante |
| correo_solicitante | TEXT | NOT NULL | Correo del solicitante |
| fecha_solicitud | TIMESTAMP | NOT NULL | Fecha de la solicitud |
| estado | TEXT | DEFAULT 'Pendiente' | Estado de la solicitud (Pendiente, En proceso, Completada, Rechazada) |
| prioridad | TEXT | DEFAULT 'Media' | Prioridad de la solicitud (Baja, Media, Alta, Urgente) |
| created_at | TIMESTAMP | DEFAULT NOW() | Fecha de creación del registro |
| updated_at | TIMESTAMP | DEFAULT NOW() | Fecha de última actualización |

## Estructura de Importación CSV

El sistema permite importar datos desde archivos CSV con la siguiente estructura:

### Datos del estudiante:

- `estudiante_numero_documento`: Documento de identidad del estudiante
- `estudiante_tipo_documento`: Tipo de documento (CC, TI, etc.)
- `estudiante_nombres`: Nombres del estudiante
- `estudiante_apellidos`: Apellidos del estudiante
- `estudiante_correo`: Correo electrónico institucional
- `estudiante_telefono`: Número de teléfono
- `estudiante_direccion`: Dirección de residencia
- `estudiante_programa_academico`: Programa académico al que pertenece
- `estudiante_semestre`: Semestre que cursa (1-12)
- `estudiante_riesgo_desercion`: Nivel de riesgo (Muy bajo, Bajo, Medio, Alto, Muy Alto)
- `estudiante_estrato`: Estrato socioeconómico (1-6)
- `estudiante_tipo_vulnerabilidad`: Tipo de vulnerabilidad (Académica, Psicológica, Económica, Social)

### Servicios disponibles para importación:

1. **Comedor Universitario** (prefijo `ComedorUniversitario_`)
   - `ComedorUniversitario_condicion_socioeconomica`: Condición socioeconómica
   - `ComedorUniversitario_fecha_solicitud`: Fecha de solicitud
   - `ComedorUniversitario_aprobado`: Estado de aprobación (true/false)
   - `ComedorUniversitario_tipo_comida`: Tipo de comida
   - `ComedorUniversitario_raciones_asignadas`: Número de raciones
   - `ComedorUniversitario_tipo_subsidio`: Tipo de subsidio
   - `ComedorUniversitario_periodo_academico`: Periodo académico

2. **Remisiones Psicológicas** (prefijo `RemisionPsicologica_`)
   - `RemisionPsicologica_motivo_remision`: Motivo de la remisión
   - `RemisionPsicologica_docente_remite`: Nombre del docente
   - `RemisionPsicologica_correo_docente`: Correo del docente
   - `RemisionPsicologica_telefono_docente`: Teléfono del docente
   - `RemisionPsicologica_fecha`: Fecha de la remisión
   - `RemisionPsicologica_hora`: Hora de la remisión
   - `RemisionPsicologica_tipo_remision`: Tipo de remisión

3. **Intervenciones Grupales** (prefijo `IntervencionGrupal_`)
   - `IntervencionGrupal_fecha_solicitud`: Fecha de solicitud
   - `IntervencionGrupal_nombre_docente`: Nombre del docente
   - `IntervencionGrupal_asignatura`: Asignatura a intervenir
   - `IntervencionGrupal_grupo`: Grupo
   - `IntervencionGrupal_tematica`: Temática sugerida
   - `IntervencionGrupal_fecha_programada`: Fecha programada
   - `IntervencionGrupal_estado`: Estado de la intervención

4. **POVAU - Programa de orientación vocacional** (prefijo `POVAU_`)
   - `POVAU_tipo_participante`: Tipo de participante
   - `POVAU_riesgo_spadies`: Nivel de riesgo según SPADIES
   - `POVAU_fecha_ingreso_programa`: Fecha de ingreso al programa
   - `POVAU_observaciones`: Observaciones adicionales

5. **POA - Plan operativo anual** (prefijo `POA_`)
   - `POA_nivel_riesgo`: Nivel de riesgo académico
   - `POA_requiere_tutoria`: Indica si requiere tutoría (true/false)
   - `POA_fecha_asignacion`: Fecha de asignación
   - `POA_acciones_apoyo`: Acciones de apoyo recomendadas

6. **Registro de Beneficios** (prefijo `RegistroBeneficio_`)
   - `RegistroBeneficio_fecha_inscripcion`: Fecha de inscripción
   - `RegistroBeneficio_estado_solicitud`: Estado de la solicitud (true/false)
   - `RegistroBeneficio_periodo_academico`: Periodo académico
   - `RegistroBeneficio_fecha_inicio`: Fecha de inicio
   - `RegistroBeneficio_fecha_finalizacion`: Fecha de finalización

7. **Solicitudes de Atención Individual** (prefijo `SolicitudAtencionIndividual_`)
   - `SolicitudAtencionIndividual_fecha_atencion`: Fecha de atención
   - `SolicitudAtencionIndividual_motivo_atencion`: Motivo de la atención

8. **Formatos de Asistencia** (prefijo `FormatoAsistencia_`)
   - `FormatoAsistencia_numero_asistencia`: Número de asistencia
   - `FormatoAsistencia_fecha`: Fecha de asistencia

## Endpoints de Estadísticas

El sistema proporciona los siguientes endpoints para obtener datos estadísticos:

1. `/api/datos-permanencia`: Devuelve datos de estrato por servicio para el componente EstratoServicioChart.jsx.
2. `/api/programas-distribucion`: Devuelve datos para el gráfico de distribución por programa académico (PieChartProgramas.jsx).
3. `/api/riesgo-desercion`: Devuelve datos para el gráfico de riesgo de deserción (RiesgoDesercionChart.jsx).

## Relaciones entre Tablas

1. **Estudiantes - Servicios de Permanencia**: Un estudiante puede estar vinculado a múltiples servicios de permanencia (relación 1:N).
2. **Estudiantes - Intervenciones Grupales**: Un estudiante puede tener múltiples intervenciones grupales (relación 1:N).
3. **Estudiantes - Asistencias**: Un estudiante puede tener múltiples asistencias a servicios (relación 1:N).
4. **Servicios - Asistencias**: Un servicio puede tener múltiples asistencias (relación 1:N).
5. **Estudiantes - Remisiones Psicológicas**: Un estudiante puede tener múltiples remisiones psicológicas (relación 1:N).
6. **Estudiantes - Comedores Universitarios**: Un estudiante puede tener múltiples registros de comedor universitario (relación 1:N).
7. **Estudiantes - Solicitudes de Atención**: Un estudiante puede realizar múltiples solicitudes de atención (relación 1:N).
8. **Estudiantes - Formatos de Asistencia**: Un estudiante puede tener múltiples formatos de asistencia (relación 1:N).
9. **Estudiantes - Asistencias Actividades**: Un estudiante puede tener múltiples asistencias a actividades (relación 1:N).
10. **Programas - Estudiantes**: Un programa académico puede tener múltiples estudiantes (relación 1:N).

## Consideraciones de Implementación

1. **Claves Primarias**: Todas las tablas utilizan UUID como clave primaria para garantizar unicidad global.
2. **Marcas de Tiempo**: Todas las tablas incluyen campos `created_at` y `updated_at` con valores predeterminados NOW() para seguimiento de auditoría.
3. **Integridad Referencial**: Las relaciones entre tablas se mantienen mediante restricciones de clave foránea (FOREIGN KEY).
4. **Importación de Datos**: El sistema utiliza prefijos estandarizados en los archivos CSV para identificar a qué tabla pertenece cada campo.
5. **Estadísticas**: Los datos agregados para los gráficos del dashboard se obtienen principalmente de la tabla `permanencia`.

## Conexión a la Base de Datos

El sistema utiliza Supabase como servicio de base de datos, y requiere las siguientes variables de entorno:

- `SUPABASE_URL`: URL del proyecto Supabase
- `SUPABASE_KEY`: Clave de API para acceder a Supabase

La conexión se establece en el archivo `config/database.py`.
