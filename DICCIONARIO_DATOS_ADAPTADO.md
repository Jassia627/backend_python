# 📚 DICCIONARIO DE DATOS ADAPTADO - SIUP
## Sistema de Información para la Unidad de Permanencia - Universidad Popular del Cesar (UPC)

### 🎯 **ADAPTACIÓN PARA PROYECTO EXISTENTE**
- **Mantiene**: Arquitectura relacional con Foreign Keys
- **Conserva**: UUIDs como Primary Keys (mejor para sistemas distribuidos)
- **Incorpora**: Campos y validaciones institucionales UPC
- **Mejora**: Normalización de datos sin duplicación

---

## 🎓 **1. TABLA PRINCIPAL DE ESTUDIANTES**

### `estudiantes`
**Descripción**: Tabla centralizada de estudiantes (mantiene diseño relacional superior).

| Campo | Tipo | Requerido | Longitud | Descripción | Validaciones UPC |
|-------|------|-----------|----------|-------------|------------------|
| `id` | UUID | ✅ | - | Identificador único (PK) | Auto-generado |
| `numero_documento` | VARCHAR | ✅ | 7-10 | Número de documento | Solo números, único |
| `tipo_documento` | VARCHAR | ✅ | 10 | Tipo de documento | ['CC', 'TI', 'CE', 'Pasaporte'] |
| `nombres` | VARCHAR | ✅ | 50 | Nombres del estudiante | Solo letras MAYÚSCULAS |
| `apellidos` | VARCHAR | ✅ | 50 | Apellidos del estudiante | Solo letras MAYÚSCULAS |
| `correo` | VARCHAR | ✅ | 100 | Correo institucional | @unicesar.edu.co |
| `telefono` | VARCHAR | ❌ | 10 | Número celular | 3xxxxxxxxx |
| `direccion` | VARCHAR | ❌ | 100 | Dirección residencia | Texto libre |
| `programa_academico` | VARCHAR | ✅ | 100 | Programa que cursa | Lista predefinida UPC |
| `semestre` | INTEGER | ✅ | 2 | Semestre actual | 1-10 |
| `riesgo_desercion` | VARCHAR | ✅ | 15 | Nivel riesgo SPADIES | ['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto'] |
| `estrato` | INTEGER | ✅ | 1 | Estrato socioeconómico | 1-6 |
| `tipo_vulnerabilidad` | VARCHAR | ❌ | 50 | Clasificación vulnerabilidad | ['Económica', 'Académica', 'Psicosocial', 'Múltiple'] |
| `created_at` | TIMESTAMP | ✅ | - | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | - | Fecha actualización | Auto-actualizado |

---

## 🛠️ **2. TABLA DE SERVICIOS DE PERMANENCIA**

### `servicios_permanencia`
**Descripción**: Tabla de relación estudiante-servicio (nueva según oficial).

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante | REFERENCES estudiantes(id) |
| `servicio` | VARCHAR | ✅ | Nombre del programa | ['POVAU', 'POA', 'POPS', 'Comedor'] |
| `fecha_registro` | DATE | ✅ | Fecha de ingreso | dd-mm-yyyy |
| `estado_participacion` | VARCHAR | ✅ | Estado actual | ['Activo', 'Inactivo', 'Finalizado'] |
| `observaciones` | TEXT | ❌ | Comentarios del proceso | ≤200 caracteres |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

---

## 📚 **3. SERVICIOS ESPECÍFICOS (Mantienen FK, agregan campos institucionales)**

### 3.1 `povau` (Programa de Orientación Vocacional)
**Descripción**: Actualizada con campos oficiales pero manteniendo relación.

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante | REFERENCES estudiantes(id) |
| `tipo_participante` | VARCHAR | ✅ | Tipo de participante | ['Admitido', 'Nuevo', 'Media académica'] |
| `riesgo_spadies` | VARCHAR | ✅ | Nivel riesgo SPADIES | ['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto'] |
| `fecha_ingreso_programa` | DATE | ✅ | Fecha inicio acompañamiento | dd-mm-yyyy |
| `observaciones` | VARCHAR | ❌ | Comentarios adicionales | ≤255 caracteres |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

### 3.2 `tutorias_academicas` (POA - Actualizada)
**Descripción**: Conserva FK, agrega campos institucionales específicos.

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante | REFERENCES estudiantes(id) |
| `docente_id` | UUID | ❌ | FK al docente tutor | REFERENCES docentes(id) |
| `semestre` | INTEGER | ✅ | Semestre actual | 1-10 |
| `nivel_riesgo` | VARCHAR | ✅ | Nivel riesgo deserción | ['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto'] |
| `requiere_tutoria` | BOOLEAN | ✅ | Indica si requiere tutorías | true/false |
| `fecha` | DATE | ✅ | Fecha registro información | dd-mm-yyyy |
| `docente_tutor` | VARCHAR | ✅ | Nombre completo tutor | Solo letras y espacios |
| `facultad` | VARCHAR | ✅ | Facultad inscrito | Lista facultades UPC |
| `programa` | VARCHAR | ✅ | Programa inscrito | Lista programas UPC |
| `periodo_academico` | VARCHAR | ✅ | Periodo académico actual | yyyy-S (ej: 2024-1) |
| `ciclo_formacion` | VARCHAR | ✅ | Nivel académico | ['Pregrado', 'Postgrado'] |
| `nombre_asignatura` | VARCHAR | ✅ | Asignatura cursada | Solo letras, números y espacios |
| `tema` | VARCHAR | ✅ | Tema trabajado | ≤150 caracteres |
| `objetivo` | VARCHAR | ✅ | Propósito acompañamiento | ≤300 caracteres |
| `metodologia` | VARCHAR | ✅ | Enfoque/técnicas aplicadas | ≤300 caracteres |
| `logros` | VARCHAR | ✅ | Avances alcanzados | ≤300 caracteres |
| `firma_tutor` | VARCHAR | ✅ | Firma del tutor | Solo letras y espacios |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

### 3.3 `asesorias_psicologicas` (POPS - Actualizada)
**Descripción**: Conserva FK, agrega campos demográficos institucionales.

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante | REFERENCES estudiantes(id) |
| `edad` | INTEGER | ✅ | Edad del estudiante | 1-99 |
| `estado_civil` | VARCHAR | ✅ | Estado civil actual | ['Soltero', 'Casado', 'Divorciado', 'Viudo', 'Unión libre'] |
| `motivo_remision` | VARCHAR | ✅ | Causa principal atención | ≤255 caracteres |
| `tipo_remision` | VARCHAR | ✅ | Tipo de apoyo ofrecido | ['Asesoría', 'Academica', 'Tutorias'] |
| `otros_ips` | VARCHAR | ❌ | Otros servicios IPS | ['Psicologia', 'Medico', 'Odontologia', 'PYP', 'Trabajo social'] |
| `fecha_remision` | DATE | ✅ | Fecha de remisión | dd-mm-yyyy (no futura) |
| `profesional_remite` | VARCHAR | ✅ | Nombre profesional remite | Solo letras y espacios |
| `tp` | VARCHAR | ✅ | Tarjeta profesional | Letras y números, sin espacios |
| `firma` | VARCHAR | ✅ | Firma profesional remite | Solo letras y espacios |
| `profesional_recibe` | VARCHAR | ✅ | Nombre profesional recibe | Solo letras y espacios |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

### 3.4 `comedor_universitario` (Actualizada)
**Descripción**: Conserva FK, agrega campos de registro de beneficios.

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante | REFERENCES estudiantes(id) |
| `condicion_socioeconomica` | VARCHAR | ✅ | Criterio vulnerabilidad | ≤100 caracteres |
| `fecha_solicitud` | DATE | ✅ | Fecha postulación | dd-mm-yyyy |
| `aprobado` | BOOLEAN | ✅ | Estado aprobación | true/false |
| `observaciones` | VARCHAR | ❌ | Comentarios adicionales | ≤255 caracteres |
| `fecha_inscripcion` | DATE | ✅ | Fecha registro oficial | dd-mm-yyyy |
| `estado_solicitud` | BOOLEAN | ✅ | Estado actual solicitud | true/false |
| `periodo_academico_beneficiado` | VARCHAR | ✅ | Periodo del beneficio | yyyy-S |
| `fecha_inicio_servicio` | DATE | ✅ | Inicio prestación | dd-mm-yyyy |
| `fecha_finalizacion_servicio` | DATE | ✅ | Fin del servicio | dd-mm-yyyy |
| `raciones_asignadas` | INTEGER | ✅ | Cantidad raciones | ≥1 |
| `servicio_semana` | VARCHAR | ❌ | Frecuencia semanal | ['Diaria', '3 veces por semana'] |
| `tipo_comida_recibida` | VARCHAR | ✅ | Tipo alimentación | ['Almuerzo', 'Cena'] |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

---

## 👨‍🏫 **4. NUEVA TABLA DE DOCENTES**

### `ficha_docentes`
**Descripción**: Tabla de docentes para relaciones (nueva según oficial).

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `fecha_registro` | DATE | ✅ | Fecha diligenciamiento | dd-mm-yyyy |
| `nombres` | VARCHAR | ✅ | Nombres del docente | Solo letras |
| `apellidos` | VARCHAR | ✅ | Apellidos del docente | Solo letras |
| `tipo_documento` | VARCHAR | ✅ | Tipo documento | ['CC', 'TI', 'CE', 'Pasaporte'] |
| `numero_documento` | VARCHAR | ✅ | Número documento | Solo dígitos |
| `fecha_nacimiento` | DATE | ✅ | Fecha nacimiento | dd-mm-yyyy |
| `lugar_nacimiento` | VARCHAR | ✅ | Lugar nacimiento | Ciudad, departamento |
| `direccion_residencia` | VARCHAR | ✅ | Dirección actual | ≤100 caracteres |
| `telefono` | VARCHAR | ❌ | Número contacto | Formato colombiano |
| `correo` | VARCHAR | ❌ | Correo institucional | @unicesar.edu.co |
| `estado_civil` | VARCHAR | ❌ | Estado civil | ['Soltero', 'Casado', 'Unión libre'] |
| `nacionalidad` | VARCHAR | ✅ | Nacionalidad | Solo letras |
| `rh` | VARCHAR | ❌ | Grupo sanguíneo | ['O+', 'A-', etc.] |
| `facultad` | VARCHAR | ✅ | Facultad | Lista facultades UPC |
| `programa` | VARCHAR | ✅ | Programa donde labora | Lista programas UPC |
| `nivel_formacion` | VARCHAR | ✅ | Nivel académico | ['Pregrado', 'Especialización', etc.] |
| `tipo_contrato` | VARCHAR | ✅ | Modalidad contratación | ['Catedrático', 'Tiempo completo'] |
| `dedicacion` | VARCHAR | ✅ | Dedicación laboral | ['TC', 'MT', 'HC'] |
| `area_conocimiento` | VARCHAR | ✅ | Área disciplinar | ≤100 caracteres |
| `anios_experiencia` | INTEGER | ✅ | Años experiencia | ≥0 |
| `materias_dictadas` | TEXT | ✅ | Asignaturas que imparte | Lista separada por comas |
| `observaciones` | TEXT | ❌ | Observaciones generales | ≤300 caracteres |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

---

## 📊 **5. NUEVAS TABLAS DE SEGUIMIENTO**

### 5.1 `seguimiento_observaciones`
**Descripción**: Seguimiento de cumplimiento y observaciones (nueva según oficial).

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante | REFERENCES estudiantes(id) |
| `cumplimiento_requisitos` | VARCHAR | ✅ | Estado cumplimiento | ['Cumple', 'No cumple', 'Parcial'] |
| `observaciones_permanencia` | VARCHAR | ✅ | Comentarios permanencia | ≤200 caracteres |
| `historial_renovaciones` | VARCHAR | ✅ | Historial renovaciones | Solo letras |
| `fecha_registro` | DATE | ✅ | Fecha del seguimiento | dd-mm-yyyy |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

### 5.2 `encuesta_satisfaccion`
**Descripción**: Evaluación de satisfacción de servicios (nueva según oficial).

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ❌ | FK al estudiante | REFERENCES estudiantes(id) |
| `fecha_aplicacion` | DATE | ✅ | Fecha aplicación encuesta | dd-mm-yyyy |
| `programa_usuario` | VARCHAR | ✅ | Programa del estudiante | Lista programas UPC |
| `tipo_atencion` | VARCHAR | ✅ | Modalidad atención | ['Individual', 'Grupal', 'Taller'] |
| `profesional_atendio` | VARCHAR | ✅ | Nombre profesional | Solo letras |
| `nombre_evento` | VARCHAR | ❌ | Nombre del evento | Texto libre |
| `tematica_evento` | VARCHAR | ❌ | Tema tratado | ≤255 caracteres |
| `puntualidad` | INTEGER | ✅ | Calificación puntualidad | 1-5 |
| `empatia` | INTEGER | ✅ | Calificación empatía | 1-5 |
| `claridad` | INTEGER | ✅ | Calificación claridad | 1-5 |
| `ambiente` | INTEGER | ✅ | Calificación ambiente | 1-5 |
| `utilidad_servicio` | INTEGER | ✅ | Calificación utilidad | 1-5 |
| `profundidad_tema` | INTEGER | ✅ | Calificación profundidad | 1-5 |
| `manejo_tema` | INTEGER | ✅ | Calificación manejo | 1-5 |
| `recomendaria_servicio` | BOOLEAN | ❌ | Recomendaría servicio | true/false |
| `recomendaciones` | TEXT | ❌ | Sugerencias específicas | ≤300 caracteres |
| `comentarios_adicionales` | TEXT | ❌ | Observaciones generales | ≤300 caracteres |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

### 5.3 `solicitud_atencion_individual`
**Descripción**: Registro de atención individual (nueva según oficial).

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante | REFERENCES estudiantes(id) |
| `codigo` | VARCHAR | ✅ | Código único estudiante | Alfanumérico |
| `ciclo_academico` | VARCHAR | ✅ | Ciclo académico | '2024-1', '2024-2' |
| `campus` | VARCHAR | ✅ | Campus del estudiante | Lista campus UPC |
| `edad` | INTEGER | ❌ | Edad del estudiante | 15-99 |
| `profesional_responsable` | VARCHAR | ✅ | Nombre profesional | Solo letras |
| `fecha_atencion` | DATE | ✅ | Fecha atención | dd-mm-yyyy |
| `hora_inicio` | TIME | ✅ | Hora inicio | hh:mm |
| `hora_finalizacion` | TIME | ✅ | Hora fin | hh:mm |
| `modalidad_atencion` | VARCHAR | ✅ | Modalidad atención | ['Individual', 'Taller grupal', 'Otro'] |
| `otro_modalidad` | VARCHAR | ❌ | Especificar modalidad | Texto libre |
| `motivo_atencion` | VARCHAR | ✅ | Motivo atención | ['Académico', 'Personal', 'Familiar', 'Otro'] |
| `otro_motivo` | VARCHAR | ❌ | Especificar motivo | Texto libre |
| `tematica_tratada` | TEXT | ✅ | Tema tratado | ≤200 caracteres |
| `observaciones` | TEXT | ❌ | Observaciones profesional | ≤300 caracteres |
| `nombre_firma_estudiante` | VARCHAR | ❌ | Nombre y firma estudiante | Texto libre |
| `doc_estudiante` | VARCHAR | ❌ | Documento estudiante | Solo números |
| `nombre_firma_profesional` | VARCHAR | ❌ | Nombre y firma profesional | Texto libre |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

---

## 📝 **6. TABLAS DE FORMATOS (Actualizadas)**

### 6.1 `intervenciones_grupales` (Actualizada)
**Descripción**: Conserva estructura actual, agrega campos institucionales.

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ❌ | FK al estudiante solicitante | REFERENCES estudiantes(id) |
| `fecha_solicitud` | DATE | ✅ | Fecha solicitud | dd-mm-yyyy |
| `fecha_recepcion` | DATE | ✅ | Fecha recepción formulario | dd-mm-yyyy |
| `docente_permanencia` | VARCHAR | ✅ | Nombre docente solicitante | Solo letras |
| `celular_permanencia` | VARCHAR | ✅ | Celular docente permanencia | Solo números |
| `correo_permanencia` | VARCHAR | ✅ | Correo docente permanencia | Formato válido |
| `programa_permanencia` | VARCHAR | ✅ | Programa docente solicitante | Lista programas UPC |
| `tipo_poblacion` | VARCHAR | ✅ | Tipo población beneficiaria | ['a', 'b', 'c', 'd', 'e', 'f', 'g'] |
| `docente_titular` | VARCHAR | ✅ | Nombre docente titular | Solo letras |
| `celular_titular` | VARCHAR | ✅ | Celular docente titular | Solo números |
| `correo_titular` | VARCHAR | ✅ | Correo docente titular | Formato válido |
| `programa_titular` | VARCHAR | ✅ | Programa docente titular | Lista programas UPC |
| `asignatura` | VARCHAR | ✅ | Nombre asignatura | Texto libre |
| `grupo` | VARCHAR | ✅ | Código grupo | Alfanumérico |
| `semestre` | VARCHAR | ✅ | Semestre académico | Números o texto |
| `numero_estudiantes` | INTEGER | ✅ | Total estudiantes grupo | Entero positivo |
| `tematica_sugerida` | VARCHAR | ❌ | Tema a intervenir | ≤255 caracteres |
| `programacion_intervencion` | JSON | ❌ | Horarios y espacios | Lunes-viernes, hora, aula, bloque, sede |
| `estado_solicitud` | VARCHAR | ❌ | Estado intervención | ['Sí', 'No'] |
| `motivo_no_intervencion` | VARCHAR | ❌ | Motivo no realización | ≤255 caracteres |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

### 6.2 `remisiones_psicologicas` (Actualizada)
**Descripción**: Conserva estructura, agrega campos específicos institucionales.

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante | REFERENCES estudiantes(id) |
| `edad` | INTEGER | ✅ | Edad del estudiante | ≥0 y <100 |
| `fecha_remision` | DATE | ✅ | Fecha de remisión | dd-mm-yyyy |
| `estado_civil` | VARCHAR | ❌ | Estado civil | ['Soltero', 'Casado', etc.] |
| `direccion_residencia` | VARCHAR | ❌ | Dirección estudiante | ≤150 caracteres |
| `tipo_remision` | VARCHAR | ✅ | Tipo general remisión | ['Académica', 'Tutorías', 'Asesorías'] |
| `ips_psicologia` | BOOLEAN | ❌ | Remisión a Psicología | true/false |
| `ips_medico` | BOOLEAN | ❌ | Remisión a Medicina | true/false |
| `ips_odontologia` | BOOLEAN | ❌ | Remisión a Odontología | true/false |
| `ips_pyp` | BOOLEAN | ❌ | Remisión a PyP | true/false |
| `ips_trabajo_social` | BOOLEAN | ❌ | Remisión a Trabajo Social | true/false |
| `motivo_remision` | VARCHAR | ✅ | Descripción del motivo | ≥10 caracteres |
| `profesional_remite` | VARCHAR | ✅ | Nombre profesional remite | Solo letras y espacios |
| `tp_remite` | VARCHAR | ❌ | Tarjeta profesional remite | Formato: TP123456 |
| `firma_remite` | VARCHAR | ❌ | Firma digital/nombre | Archivo o URL |
| `profesional_recibe` | VARCHAR | ❌ | Nombre profesional recibe | Solo letras y espacios |
| `tp_recibe` | VARCHAR | ❌ | Tarjeta profesional recibe | Formato: TP987654 |
| `firma_recibe` | VARCHAR | ❌ | Firma digital/nombre | Archivo o URL |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

### 6.3 `formato_asistencia` (Actualizada)
**Descripción**: Registro de asistencia a actividades (actualizada según oficial).

| Campo | Tipo | Requerido | Descripción | Validaciones |
|-------|------|-----------|-------------|--------------|
| `id` | UUID | ✅ | Identificador único (PK) | Auto-generado |
| `estudiante_id` | UUID | ✅ | FK al estudiante asistente | REFERENCES estudiantes(id) |
| `nombre_responsable` | VARCHAR | ✅ | Nombre responsable actividad | Solo letras MAYÚSCULAS |
| `actividad` | VARCHAR | ✅ | Nombre/tipo actividad | ≤150 caracteres |
| `tema` | VARCHAR | ✅ | Tema principal | ≤150 caracteres |
| `objetivo` | VARCHAR | ❌ | Objetivo actividad | ≥10 caracteres |
| `fecha` | DATE | ✅ | Fecha actividad | dd-mm-yyyy |
| `lugar` | VARCHAR | ✅ | Lugar actividad | Ej: UPC |
| `salon` | VARCHAR | ❌ | Salón específico | Alfanumérico (205-A) |
| `programa_general` | VARCHAR | ✅ | Programa general actividad | Lista programas UPC |
| `asignatura` | VARCHAR | ❌ | Asignatura asociada | Lista asignaturas UPC |
| `articulacion` | BOOLEAN | ✅ | Articula con líneas | true/false |
| `lineas_articuladas` | VARCHAR | ❌ | Líneas que articula | ≤200 caracteres |
| `created_at` | TIMESTAMP | ✅ | Fecha creación | Auto-generado |
| `updated_at` | TIMESTAMP | ✅ | Fecha actualización | Auto-actualizado |

---

## 🔗 **7. RELACIONES MEJORADAS**

### **Diagrama de Relaciones Actualizado**
```
estudiantes (1) ←→ (N) servicios_permanencia
estudiantes (1) ←→ (N) povau
estudiantes (1) ←→ (N) tutorias_academicas
estudiantes (1) ←→ (N) asesorias_psicologicas
estudiantes (1) ←→ (N) comedor_universitario
estudiantes (1) ←→ (N) seguimiento_observaciones
estudiantes (1) ←→ (N) solicitud_atencion_individual
estudiantes (1) ←→ (N) remisiones_psicologicas
estudiantes (1) ←→ (N) formato_asistencia
docentes (1) ←→ (N) tutorias_academicas
```

### **Foreign Keys Actualizadas**
```sql
-- Relaciones principales (mantener)
servicios_permanencia.estudiante_id → estudiantes.id
povau.estudiante_id → estudiantes.id
tutorias_academicas.estudiante_id → estudiantes.id
asesorias_psicologicas.estudiante_id → estudiantes.id
comedor_universitario.estudiante_id → estudiantes.id

-- Nuevas relaciones
tutorias_academicas.docente_id → docentes.id
seguimiento_observaciones.estudiante_id → estudiantes.id
encuesta_satisfaccion.estudiante_id → estudiantes.id
solicitud_atencion_individual.estudiante_id → estudiantes.id
remisiones_psicologicas.estudiante_id → estudiantes.id
formato_asistencia.estudiante_id → estudiantes.id
```

---

## 📋 **8. VARIABLES CLAVE PARA ANÁLISIS**

### **Ejes Principales de Análisis (Conservados)**
| Variable | Tabla Origen | Descripción |
|----------|--------------|-------------|
| `programa_academico` | estudiantes | Programa académico del estudiante |
| `semestre` | estudiantes | Nivel académico actual |
| `riesgo_desercion` | estudiantes | Nivel de riesgo SPADIES |
| `estrato` | estudiantes | Nivel socioeconómico |
| `tipo_vulnerabilidad` | estudiantes | Clasificación vulnerabilidad |
| `servicio` | servicios_permanencia | Programa de permanencia |
| `estado_participacion` | servicios_permanencia | Estado en el servicio |
| `fecha_registro` | servicios_permanencia | Fecha acceso al servicio |

---

## 📚 **9. PROGRAMAS ACADÉMICOS UPC**

### **Lista de Programas Válidos**
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

### **Facultades UPC**
```
• Facultad Ciencias Administrativas contables y económicas
• Facultad de bellas artes
• Facultad de derecho, ciencias políticas y sociales
• Facultad DE Ciencias Básicas
• Facultad ingenierías y tecnologías
• Facultad Ciencias de la salud
• Facultad DE Educación
```

---

## ✅ **10. VENTAJAS DEL DISEÑO ADAPTADO**

### **Mantiene Fortalezas del Proyecto Actual**
- ✅ **Normalización**: Datos del estudiante centralizados
- ✅ **Integridad referencial**: Foreign keys con CASCADE
- ✅ **UUIDs**: Mejor para sistemas distribuidos
- ✅ **Eficiencia**: JOINs optimizados

### **Incorpora Requerimientos Institucionales**
- ✅ **Campos específicos**: Todos los campos del diccionario oficial
- ✅ **Validaciones UPC**: Correos @unicesar.edu.co, formatos específicos
- ✅ **Nuevas tablas**: Docentes, encuestas, seguimientos
- ✅ **Compatibilidad**: Mantiene funcionalidad existente

---

## 🚀 **11. PLAN DE MIGRACIÓN RECOMENDADO**

### **Fase 1: Actualizar Tablas Existentes**
1. Agregar campos faltantes a `estudiantes`
2. Actualizar validaciones de campos existentes
3. Agregar campos específicos a servicios

### **Fase 2: Crear Nuevas Tablas**
1. Crear tabla `docentes`
2. Crear tabla `servicios_permanencia`
3. Crear tablas de seguimiento

### **Fase 3: Establecer Nuevas Relaciones**
1. Agregar FK `docente_id` a `tutorias_academicas`
2. Crear relaciones con nuevas tablas
3. Migrar datos existentes

### **Fase 4: Actualizar Aplicación**
1. Actualizar modelos Pydantic
2. Actualizar validaciones
3. Actualizar endpoints API

Este diccionario adaptado **preserva tu arquitectura superior** mientras **cumple con los requerimientos institucionales**, ofreciendo lo mejor de ambos mundos. 