# 📚 DICCIONARIO DE DATOS COMPLETO
## Sistema de Información para la Unidad de Permanencia - Universidad Popular del Cesar (UPC)

### 🎯 **INFORMACIÓN GENERAL**
- **Sistema**: Sistema de Información para la Unidad de Permanencia (SIUP)
- **Universidad**: Universidad Popular del Cesar (UPC)
- **Tecnología Backend**: FastAPI + Python 3.9+
- **Base de Datos**: Supabase (PostgreSQL)
- **Frontend**: React + TypeScript
- **Propósito**: Gestión integral de la permanencia estudiantil universitaria

---

## 📋 **ÍNDICE DE CONTENIDO**
1. [Tabla de Estudiantes](#estudiantes)
2. [Servicios de Permanencia](#servicios-permanencia)
3. [Programas Académicos](#programas)
4. [Tablas de Servicios](#tablas-servicios)
5. [Tablas de Control](#tablas-control)
6. [Enumeraciones y Valores Válidos](#enumeraciones)
7. [Relaciones entre Tablas](#relaciones)
8. [Validaciones del Sistema](#validaciones)

---

## 🎓 **1. TABLA DE ESTUDIANTES** {#estudiantes}

### `estudiantes`
**Descripción**: Tabla principal que almacena información básica de todos los estudiantes.

| Campo | Tipo | Requerido | Longitud | Descripción | Valores Válidos |
|-------|------|-----------|----------|-------------|-----------------|
| `id` | UUID | ✅ | - | Identificador único (PK) | Auto-generado |
| `documento` | TEXT | ✅ | 7-10 | Número de documento de identidad | Solo números |
| `tipo_documento` | TEXT | ✅ | - | Tipo de documento | CC, TI, CE, Pasaporte |
| `nombres` | TEXT | ✅ | 2-50 | Nombres del estudiante | Solo letras y espacios |
| `apellidos` | TEXT | ✅ | 2-50 | Apellidos del estudiante | Solo letras y espacios |
| `correo` | TEXT | ✅ | - | Correo electrónico | Formato email válido |
| `telefono` | TEXT | ❌ | 10 | Número de teléfono celular | 3xxxxxxxxx (Colombia) |
| `direccion` | TEXT | ❌ | ≤100 | Dirección de residencia | Texto libre |
| `programa_academico` | TEXT | ✅ | - | Programa que cursa | Ver lista de programas |
| `semestre` | INTEGER | ✅ | - | Semestre actual | 1-12 |
| `estrato` | INTEGER | ❌ | - | Estrato socioeconómico | 1-6 |
| `riesgo_desercion` | TEXT | ❌ | - | Nivel de riesgo de deserción | Muy bajo, Bajo, Medio, Alto, Muy alto |
| `created_at` | TIMESTAMP | ✅ | - | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | - | Fecha de actualización | Auto-actualizado |

**Índices**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `documento`

---

## 🛠️ **2. SERVICIOS DE PERMANENCIA** {#servicios-permanencia}

### 2.1 `tutorias_academicas` (POA - Programa de Orientación Académica)
**Descripción**: Registro de tutorías y acompañamiento académico.

| Campo | Tipo | Requerido | Descripción | Valores Válidos |
|-------|------|-----------|-------------|-----------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | Referencia al estudiante (FK) | `estudiantes.id` |
| `asignatura` | VARCHAR(100) | ❌ | Materia de la tutoría | Texto libre |
| `fecha_tutoria` | DATE | ❌ | Fecha de la tutoría | YYYY-MM-DD |
| `fecha_asignacion` | DATE | ❌ | Fecha de asignación | YYYY-MM-DD |
| `hora_inicio` | TIME | ❌ | Hora de inicio | HH:MM |
| `hora_fin` | TIME | ❌ | Hora de finalización | HH:MM |
| `tutor` | VARCHAR(200) | ❌ | Nombre del tutor | Texto libre |
| `acciones_apoyo` | TEXT | ❌ | Acciones de apoyo realizadas | Texto libre |
| `nivel_riesgo` | VARCHAR(50) | ❌ | Nivel de riesgo académico | Bajo, Medio, Alto |
| `requiere_tutoria` | BOOLEAN | ❌ | Si requiere tutoría | true/false |
| `created_at` | TIMESTAMP | ✅ | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha de actualización | Auto-actualizado |

### 2.2 `asesorias_psicologicas` (POPS - Programa de Orientación Psicosocial)
**Descripción**: Registro de atención y seguimiento psicosocial.

| Campo | Tipo | Requerido | Descripción | Valores Válidos |
|-------|------|-----------|-------------|-----------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | Referencia al estudiante (FK) | `estudiantes.id` |
| `motivo_consulta` | TEXT | ❌ | Motivo de la consulta | Texto libre |
| `motivo_intervencion` | TEXT | ❌ | Motivo de intervención | Ver enumeraciones |
| `tipo_intervencion` | VARCHAR(100) | ❌ | Tipo de intervención | Asesoría, Taller, Otro |
| `fecha` | DATE | ✅ | Fecha de la asesoría | YYYY-MM-DD |
| `fecha_atencion` | DATE | ❌ | Fecha de atención | YYYY-MM-DD |
| `psicologo` | VARCHAR(200) | ❌ | Nombre del psicólogo | Texto libre |
| `seguimiento` | TEXT | ❌ | Observaciones de seguimiento | Texto libre |
| `created_at` | TIMESTAMP | ✅ | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha de actualización | Auto-actualizado |

### 2.3 `orientaciones_vocacionales` (POVAU - Programa de Orientación Vocacional)
**Descripción**: Registro de orientación vocacional y seguimiento.

| Campo | Tipo | Requerido | Descripción | Valores Válidos |
|-------|------|-----------|-------------|-----------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | Referencia al estudiante (FK) | `estudiantes.id` |
| `fecha_orientacion` | DATE | ❌ | Fecha de orientación | YYYY-MM-DD |
| `fecha_ingreso_programa` | DATE | ❌ | Fecha de ingreso al programa | YYYY-MM-DD |
| `tipo_participante` | VARCHAR(100) | ❌ | Tipo de participante | Admitido, Nuevo, Media académica |
| `area_interes` | VARCHAR(100) | ❌ | Área de interés | Texto libre |
| `resultado` | TEXT | ❌ | Resultado de la orientación | Texto libre |
| `orientador` | VARCHAR(200) | ❌ | Nombre del orientador | Texto libre |
| `observaciones` | TEXT | ❌ | Observaciones adicionales | Texto libre |
| `riesgo_spadies` | VARCHAR(50) | ❌ | Nivel de riesgo SPADIES | Bajo, Medio, Alto |
| `created_at` | TIMESTAMP | ✅ | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha de actualización | Auto-actualizado |

### 2.4 `comedor_universitario` (Apoyo Alimentario)
**Descripción**: Registro de beneficiarios del comedor universitario.

| Campo | Tipo | Requerido | Descripción | Valores Válidos |
|-------|------|-----------|-------------|-----------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | Referencia al estudiante (FK) | `estudiantes.id` |
| `condicion_socioeconomica` | VARCHAR(50) | ✅ | Condición socioeconómica | Texto libre |
| `fecha_solicitud` | DATE | ❌ | Fecha de solicitud | YYYY-MM-DD |
| `aprobado` | BOOLEAN | ❌ | Si fue aprobado | true/false |
| `tipo_comida` | VARCHAR(50) | ❌ | Tipo de comida | Almuerzo |
| `raciones_asignadas` | INTEGER | ❌ | Número de raciones | 1-100 |
| `observaciones` | TEXT | ❌ | Observaciones | ≤255 caracteres |
| `tipo_subsidio` | VARCHAR(100) | ❌ | Tipo de subsidio | Completo, Parcial, Regular |
| `periodo_academico` | VARCHAR(50) | ❌ | Periodo académico | YYYY-N |
| `estrato` | INTEGER | ❌ | Estrato del estudiante | 1-6 |
| `created_at` | TIMESTAMP | ✅ | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha de actualización | Auto-actualizado |

### 2.5 `apoyos_socioeconomicos` (Apoyo Socioeconómico)
**Descripción**: Registro de apoyos económicos y becas.

| Campo | Tipo | Requerido | Descripción | Valores Válidos |
|-------|------|-----------|-------------|-----------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | Referencia al estudiante (FK) | `estudiantes.id` |
| `tipo_apoyo` | VARCHAR(100) | ❌ | Tipo de apoyo económico | Texto libre |
| `monto` | DECIMAL(10,2) | ❌ | Monto del apoyo | Valor monetario |
| `fecha_otorgamiento` | DATE | ❌ | Fecha de otorgamiento | YYYY-MM-DD |
| `fecha_finalizacion` | DATE | ❌ | Fecha de finalización | YYYY-MM-DD |
| `estado` | VARCHAR(50) | ❌ | Estado del apoyo | activo, inactivo, finalizado |
| `tipo_vulnerabilidad` | VARCHAR(100) | ❌ | Tipo de vulnerabilidad | Ver enumeraciones |
| `observaciones` | TEXT | ❌ | Observaciones | Texto libre |
| `created_at` | TIMESTAMP | ✅ | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha de actualización | Auto-actualizado |

### 2.6 `talleres_habilidades` (Talleres de Habilidades)
**Descripción**: Registro de talleres y capacitaciones.

| Campo | Tipo | Requerido | Descripción | Valores Válidos |
|-------|------|-----------|-------------|-----------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | Referencia al estudiante (FK) | `estudiantes.id` |
| `nombre_taller` | VARCHAR(200) | ✅ | Nombre del taller | Texto libre |
| `fecha_inicio` | DATE | ✅ | Fecha de inicio | YYYY-MM-DD |
| `fecha_fin` | DATE | ❌ | Fecha de finalización | YYYY-MM-DD |
| `fecha_taller` | DATE | ❌ | Fecha del taller | YYYY-MM-DD |
| `horas_completadas` | INTEGER | ❌ | Horas completadas | ≥0 |
| `certificado` | BOOLEAN | ❌ | Si obtuvo certificado | true/false |
| `facilitador` | VARCHAR(200) | ❌ | Nombre del facilitador | Texto libre |
| `created_at` | TIMESTAMP | ✅ | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha de actualización | Auto-actualizado |

### 2.7 `seguimientos_academicos` (Seguimientos Académicos)
**Descripción**: Registro de seguimiento académico de estudiantes.

| Campo | Tipo | Requerido | Descripción | Valores Válidos |
|-------|------|-----------|-------------|-----------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | Referencia al estudiante (FK) | `estudiantes.id` |
| `fecha_seguimiento` | DATE | ❌ | Fecha del seguimiento | YYYY-MM-DD |
| `periodo_academico` | VARCHAR(20) | ❌ | Periodo académico | YYYY-N |
| `promedio_actual` | DECIMAL(3,2) | ❌ | Promedio académico | 0.00-5.00 |
| `materias_perdidas` | INTEGER | ❌ | Materias perdidas | ≥0 |
| `materias_cursadas` | INTEGER | ❌ | Materias cursadas | ≥0 |
| `observaciones` | TEXT | ❌ | Observaciones generales | Texto libre |
| `observaciones_permanencia` | TEXT | ❌ | Observaciones de permanencia | Texto libre |
| `requiere_tutoria` | BOOLEAN | ❌ | Si requiere tutoría | true/false |
| `estado_participacion` | VARCHAR(50) | ❌ | Estado de participación | Activo, Inactivo, Finalizado |
| `created_at` | TIMESTAMP | ✅ | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha de actualización | Auto-actualizado |

---

## 🏫 **3. PROGRAMAS ACADÉMICOS** {#programas}

### `programas`
**Descripción**: Catálogo de programas académicos de la universidad.

| Campo | Tipo | Requerido | Descripción | Valores Válidos |
|-------|------|-----------|-------------|-----------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `codigo` | VARCHAR(20) | ✅ | Código del programa | Formato ABC-123 |
| `nombre` | VARCHAR(200) | ✅ | Nombre del programa | Ver lista de programas |
| `facultad` | VARCHAR(100) | ✅ | Facultad a la que pertenece | Ver facultades UPC |
| `nivel` | VARCHAR(50) | ✅ | Nivel académico | Pregrado, Postgrado |
| `modalidad` | VARCHAR(50) | ❌ | Modalidad de estudio | Presencial, Virtual, Híbrido |
| `estado` | BOOLEAN | ❌ | Estado del programa | true (Activo), false (Inactivo) |
| `created_at` | TIMESTAMP | ✅ | Fecha de creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha de actualización | Auto-actualizado |

**Índices**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `codigo`

---

## 🗂️ **4. TABLAS DE SERVICIOS ADICIONALES** {#tablas-servicios}

### 4.1 `remisiones_psicologicas`
**Descripción**: Registro de remisiones para atención psicológica.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | UUID | ✅ | Identificador único (PK) |
| `estudiante_id` | UUID | ❌ | Referencia al estudiante (FK) |
| `nombre_estudiante` | VARCHAR(100) | ✅ | Nombre completo |
| `numero_documento` | VARCHAR(20) | ✅ | Número de documento |
| `programa_academico` | VARCHAR(100) | ✅ | Programa que cursa |
| `semestre` | VARCHAR(10) | ✅ | Semestre |
| `motivo_remision` | TEXT | ✅ | Motivo de la remisión |
| `docente_remite` | VARCHAR(100) | ✅ | Docente que remite |
| `correo_docente` | VARCHAR(100) | ✅ | Correo del docente |
| `telefono_docente` | VARCHAR(20) | ✅ | Teléfono del docente |
| `fecha` | DATE | ✅ | Fecha de la remisión |
| `hora` | TIME | ✅ | Hora de la remisión |
| `tipo_remision` | VARCHAR(50) | ✅ | Tipo de remisión |
| `observaciones` | TEXT | ❌ | Observaciones |

### 4.2 `intervenciones_grupales`
**Descripción**: Registro de intervenciones grupales programadas.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | UUID | ✅ | Identificador único (PK) |
| `estudiante_id` | UUID | ❌ | Referencia al estudiante (FK) |
| `fecha_solicitud` | DATE | ✅ | Fecha de solicitud |
| `fecha_recepcion` | DATE | ❌ | Fecha de recepción |
| `nombre_docente_permanencia` | VARCHAR(200) | ✅ | Docente de permanencia |
| `asignatura_intervenir` | VARCHAR(200) | ✅ | Asignatura a intervenir |
| `grupo` | VARCHAR(20) | ✅ | Grupo |
| `tematica_sugerida` | TEXT | ❌ | Temática sugerida |
| `fecha_estudiante_programa_academicoda` | DATE | ✅ | Fecha programada |
| `hora` | TIME | ✅ | Hora |
| `aula` | VARCHAR(50) | ✅ | Aula |
| `estado` | VARCHAR(50) | ✅ | Estado |

### 4.3 `software_solicitudes`
**Descripción**: Solicitudes de software especializado.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | UUID | ✅ | Identificador único (PK) |
| `estudiante_id` | UUID | ❌ | Referencia al estudiante (FK) |
| `nombre_solicitante` | VARCHAR(100) | ✅ | Nombre del solicitante |
| `correo_solicitante` | VARCHAR(100) | ✅ | Correo del solicitante |
| `telefono_solicitante` | VARCHAR(20) | ❌ | Teléfono del solicitante |
| `programa_academico` | VARCHAR(100) | ✅ | Programa académico |
| `nombre_software` | VARCHAR(100) | ✅ | Nombre del software |
| `version` | VARCHAR(50) | ❌ | Versión del software |
| `justificacion` | TEXT | ✅ | Justificación de la solicitud |
| `estado` | VARCHAR(50) | ❌ | Estado (default: 'Pendiente') |

### 4.4 `actas_negacion`
**Descripción**: Actas de negación de servicios.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | UUID | ✅ | Identificador único (PK) |
| `estudiante_id` | UUID | ❌ | Referencia al estudiante (FK) |
| `nombre_estudiante` | VARCHAR(100) | ✅ | Nombre completo |
| `documento_tipo` | VARCHAR(50) | ✅ | Tipo de documento |
| `documento_numero` | VARCHAR(50) | ✅ | Número de documento |
| `documento_expedido_en` | VARCHAR(100) | ✅ | Lugar de expedición |
| `fecha_firma_dia` | VARCHAR(10) | ✅ | Día de firma |
| `fecha_firma_mes` | VARCHAR(10) | ✅ | Mes de firma |
| `fecha_firma_anio` | VARCHAR(10) | ✅ | Año de firma |
| `firma_estudiante` | VARCHAR(100) | ✅ | Firma del estudiante |
| `docente_permanencia` | VARCHAR(100) | ✅ | Docente de permanencia |

---

## 📊 **5. TABLAS DE CONTROL** {#tablas-control}

### 5.1 `permanencia`
**Descripción**: Tabla para estadísticas y control de permanencia.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | UUID | ✅ | Identificador único (PK) |
| `servicio` | VARCHAR(100) | ✅ | Tipo de servicio |
| `estrato` | INTEGER | ❌ | Estrato socioeconómico |
| `inscritos` | INTEGER | ❌ | Cantidad de inscritos |
| `estudiante_programa_academico` | VARCHAR(200) | ❌ | Programa académico |
| `riesgo_desercion` | VARCHAR(50) | ❌ | Nivel de riesgo |
| `tipo_vulnerabilidad` | VARCHAR(100) | ❌ | Tipo de vulnerabilidad |
| `periodo` | VARCHAR(20) | ❌ | Periodo académico |
| `semestre` | INTEGER | ❌ | Semestre |
| `matriculados` | INTEGER | ❌ | Estudiantes matriculados |
| `desertores` | INTEGER | ❌ | Estudiantes desertores |
| `graduados` | INTEGER | ❌ | Estudiantes graduados |
| `requiere_tutoria` | VARCHAR(2) | ❌ | Requiere tutoría (Sí/No) |

### 5.2 `servicios`
**Descripción**: Catálogo de servicios disponibles.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | UUID | ✅ | Identificador único (PK) |
| `codigo` | VARCHAR(20) | ✅ | Código del servicio |
| `nombre` | VARCHAR(200) | ✅ | Nombre del servicio |
| `descripcion` | TEXT | ❌ | Descripción del servicio |
| `tipo` | VARCHAR(100) | ❌ | Tipo de servicio |
| `estado` | BOOLEAN | ❌ | Estado del servicio |

### 5.3 `asistencias`
**Descripción**: Control de asistencias a actividades.

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | UUID | ✅ | Identificador único (PK) |
| `estudiante_id` | UUID | ✅ | Referencia al estudiante (FK) |
| `servicio_id` | UUID | ✅ | Referencia al servicio (FK) |
| `actividad` | VARCHAR(200) | ✅ | Nombre de la actividad |
| `fecha` | DATE | ✅ | Fecha de la actividad |
| `hora_inicio` | TIME | ❌ | Hora de inicio |
| `hora_fin` | TIME | ❌ | Hora de finalización |
| `asistio` | BOOLEAN | ❌ | Si asistió (default: true) |
| `observaciones` | TEXT | ❌ | Observaciones |

---

## 📋 **6. ENUMERACIONES Y VALORES VÁLIDOS** {#enumeraciones}

### 6.1 **Programas Académicos**
```
• ADMINISTRACIÓN DE EMPRESAS
• ADMINISTRACIÓN DE EMPRESAS TURÍSTICAS Y HOTELERAS
• COMERCIO INTERNACIONAL
• CONTADURÍA PÚBLICA
• DERECHO
• ECONOMÍA
• ENFERMERÍA
• INGENIERÍA AGROINDUSTRIAL
• INGENIERÍA AMBIENTAL Y SANITARIA
• INGENIERÍA ELECTRÓNICA
• INGENIERÍA DE SISTEMAS
• INSTRUMENTACIÓN QUIRÚRGICA
• LICENCIATURA EN ARTE Y FOLCLOR
• LICENCIATURA EN CIENCIAS NATURALES Y EDUCACIÓN AMBIENTAL
• LICENCIATURA EN EDUCACIÓN FÍSICA, RECREACIÓN Y DEPORTES
• LICENCIATURA EN LENGUA CASTELLANA E INGLÉS
• LICENCIATURA EN MATEMÁTICAS
• MICROBIOLOGÍA
• SOCIOLOGÍA
```

### 6.2 **Facultades UPC**
```
• Facultad Ciencias Administrativas contables y económicas
• Facultad de bellas artes
• Facultad de derecho, ciencias políticas y sociales
• Facultad DE Ciencias Básicas
• Facultad ingenierías y tecnologías
• Facultad Ciencias de la salud
• Facultad DE Educación
```

### 6.3 **Tipos de Documento**
```
• CC (Cédula de Ciudadanía)
• TI (Tarjeta de Identidad)
• CE (Cédula de Extranjería)
• Pasaporte
```

### 6.4 **Niveles de Riesgo de Deserción**
```
• Muy bajo
• Bajo
• Medio
• Alto
• Muy alto
```

### 6.5 **Estratos Socioeconómicos**
```
• 1, 2, 3, 4, 5, 6
```

### 6.6 **Estados de Participación**
```
• Activo
• Inactivo
• Finalizado
```

### 6.7 **Tipos de Comida**
```
• Almuerzo
```

### 6.8 **Tipos de Participante (POVAU)**
```
• Admitido
• Nuevo
• Media académica
```

### 6.9 **Niveles de Riesgo SPADIES**
```
• Bajo
• Medio
• Alto
```

### 6.10 **Motivos de Intervención Psicológica**
```
• Problemas familiares
• Dificultades emocionales
• Estrés académico
• Ansiedad / depresión
• Problemas de adaptación
• Otros
```

### 6.11 **Tipos de Intervención**
```
• Asesoría
• Taller
• Otro
```

### 6.12 **Tipos de Vulnerabilidad**
```
• Académica
• Psicológica
• Económica
• Social
```

### 6.13 **Tipos de Subsidio (Comedor)**
```
• Completo
• Parcial
• Regular
```

---

## 🔗 **7. RELACIONES ENTRE TABLAS** {#relaciones}

### **Diagrama de Relaciones Principal**
```
estudiantes (1) ←→ (N) tutorias_academicas
estudiantes (1) ←→ (N) asesorias_psicologicas
estudiantes (1) ←→ (N) orientaciones_vocacionales
estudiantes (1) ←→ (N) comedor_universitario
estudiantes (1) ←→ (N) apoyos_socioeconomicos
estudiantes (1) ←→ (N) talleres_habilidades
estudiantes (1) ←→ (N) seguimientos_academicos
estudiantes (1) ←→ (N) asistencias
servicios (1) ←→ (N) asistencias
```

### **Claves Foráneas (Foreign Keys)**
- `tutorias_academicas.estudiante_id` → `estudiantes.id`
- `asesorias_psicologicas.estudiante_id` → `estudiantes.id`
- `orientaciones_vocacionales.estudiante_id` → `estudiantes.id`
- `comedor_universitario.estudiante_id` → `estudiantes.id`
- `apoyos_socioeconomicos.estudiante_id` → `estudiantes.id`
- `talleres_habilidades.estudiante_id` → `estudiantes.id`
- `seguimientos_academicos.estudiante_id` → `estudiantes.id`
- `asistencias.estudiante_id` → `estudiantes.id`
- `asistencias.servicio_id` → `servicios.id`
- `remisiones_psicologicas.estudiante_id` → `estudiantes.id` (NULLABLE)
- `intervenciones_grupales.estudiante_id` → `estudiantes.id` (NULLABLE)
- `software_solicitudes.estudiante_id` → `estudiantes.id` (NULLABLE)
- `actas_negacion.estudiante_id` → `estudiantes.id` (NULLABLE)

### **Acciones en Cascada**
- **ON DELETE CASCADE**: Al eliminar un estudiante, se eliminan todos sus registros relacionados
- **ON DELETE SET NULL**: Para tablas con referencia opcional, se establece NULL

---

## ✅ **8. VALIDACIONES DEL SISTEMA** {#validaciones}

### 8.1 **Validaciones de Estudiantes**
- **Documento**: Solo números, 7-10 dígitos, único
- **Nombres/Apellidos**: Solo letras y espacios, 2-50 caracteres
- **Correo**: Formato email válido, único
- **Teléfono**: Celular colombiano (3xxxxxxxxx) o vacío
- **Programa**: Debe existir en la lista de programas válidos
- **Semestre**: Entero entre 1 y 12
- **Estrato**: Entero entre 1 y 6

### 8.2 **Validaciones de Fechas**
- **Formato**: YYYY-MM-DD
- **Rango**: No fechas futuras para registros históricos
- **Consistencia**: fecha_fin >= fecha_inicio

### 8.3 **Validaciones de Tiempo**
- **Formato**: HH:MM (24 horas)
- **Consistencia**: hora_fin > hora_inicio

### 8.4 **Validaciones de Campos Numéricos**
- **Promedio académico**: 0.00 - 5.00
- **Raciones comedor**: 1 - 100
- **Horas completadas**: >= 0
- **Materias**: >= 0

### 8.5 **Validaciones de Texto**
- **Longitudes máximas**: Respetadas según especificación
- **Caracteres especiales**: Controlados según contexto
- **Campos requeridos**: No nulos ni vacíos

---

## 🔐 **NOTAS DE SEGURIDAD Y RENDIMIENTO**

### **Índices Creados**
- Índices en todas las claves foráneas
- Índices únicos en campos identificadores
- Índices de búsqueda en campos frecuentemente consultados

### **Restricciones de Integridad**
- Claves primarias UUID auto-generadas
- Claves foráneas con restricciones de integridad referencial
- Campos NOT NULL donde es requerido
- Valores por defecto establecidos

### **Auditoría**
- Campos `created_at` y `updated_at` en todas las tablas
- Timestamps automáticos
- Preservación de datos históricos

---

## 📝 **CHANGELOG Y VERSIONES**

### **Versión 1.0** (Actual)
- ✅ Implementación completa del sistema base
- ✅ Todos los servicios de permanencia operativos
- ✅ Validaciones y restricciones implementadas
- ✅ API REST completamente funcional
- ✅ Frontend React integrado

---

**Última actualización**: 06 de Junio de 2025
**Versión del documento**: 1.0
**Responsable**: Sistema SIUP - UPC 