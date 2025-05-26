# Documentación de Endpoints

## Endpoints de Carga de Datos

### POST `/upload-csv`

Este endpoint permite cargar datos masivamente desde un archivo CSV para diferentes entidades del sistema.

**Parámetros:**
- `file`: Archivo CSV a cargar (obligatorio)
- `tipo`: Tipo de datos a cargar (opcional)

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "documento": "123456789",
      "programa": "INGENIERÍA DE SISTEMAS",
      "estudiante_id": "uuid-del-estudiante",
      "procesado": true
    }
  ],
  "inserted": 10,
  "errors": [],
  "message": "Se procesaron 10 registros correctamente."
}
```

**Proceso:**
1. Recibe un archivo CSV
2. Procesa cada fila del CSV
3. Crea o actualiza registros de estudiantes
4. Crea registros en tablas relacionadas (POVAU, POA, etc.)
5. Genera estadísticas en la tabla de permanencia
6. Retorna un resumen del proceso

## Endpoints de Estadísticas

### GET `/api/datos-permanencia`

Proporciona datos para el gráfico de estrato por servicio (EstratoServicioChart.jsx).

**Respuesta:**
```json
[
  {
    "servicio": "POA",
    "estrato_1": 10,
    "estrato_2": 15,
    "estrato_3": 20,
    "estrato_4": 12,
    "estrato_5": 8,
    "estrato_6": 5
  },
  {
    "servicio": "POVAU",
    "estrato_1": 8,
    "estrato_2": 12,
    "estrato_3": 18,
    "estrato_4": 10,
    "estrato_5": 6,
    "estrato_6": 3
  }
]
```

### GET `/api/programas-distribucion`

Proporciona datos para el gráfico de distribución por programa académico (PieChartProgramas.jsx).

**Respuesta:**
```json
[
  {
    "programa": "INGENIERÍA DE SISTEMAS",
    "cantidad": 50
  },
  {
    "programa": "MEDICINA",
    "cantidad": 75
  },
  {
    "programa": "DERECHO",
    "cantidad": 60
  }
]
```

### GET `/api/riesgo-desercion`

Proporciona datos para el gráfico de riesgo de deserción (RiesgoDesercionChart.jsx).

**Respuesta:**
```json
[
  {
    "riesgo": "bajo",
    "cantidad": 200
  },
  {
    "riesgo": "medio",
    "cantidad": 150
  },
  {
    "riesgo": "alto",
    "cantidad": 100
  },
  {
    "riesgo": "muy alto",
    "cantidad": 50
  }
]
```

## Endpoints de Estudiantes

### GET `/estudiantes`

Obtiene la lista de todos los estudiantes.

**Parámetros de consulta:**
- `limit`: Número máximo de resultados (opcional, por defecto 100)
- `offset`: Número de resultados a omitir (opcional, por defecto 0)
- `programa`: Filtrar por programa académico (opcional)

**Respuesta:**
```json
{
  "data": [
    {
      "id": "uuid-del-estudiante",
      "documento": "123456789",
      "nombres": "Nombre Estudiante",
      "apellidos": "Apellido Estudiante",
      "programa_academico": "INGENIERÍA DE SISTEMAS",
      "semestre": 5,
      "estrato": 3
    }
  ],
  "count": 1,
  "total": 500
}
```

### GET `/estudiantes/{id}`

Obtiene los detalles de un estudiante específico.

**Parámetros:**
- `id`: ID del estudiante (UUID)

**Respuesta:**
```json
{
  "id": "uuid-del-estudiante",
  "documento": "123456789",
  "nombres": "Nombre Estudiante",
  "apellidos": "Apellido Estudiante",
  "programa_academico": "INGENIERÍA DE SISTEMAS",
  "semestre": 5,
  "estrato": 3,
  "correo": "estudiante@ejemplo.com",
  "telefono": "1234567890",
  "direccion": "Dirección del estudiante"
}
```

## Endpoints de Tutorías Académicas

### GET `/tutorias`

Obtiene la lista de tutorías académicas.

**Parámetros de consulta:**
- `estudiante_id`: Filtrar por ID de estudiante (opcional)
- `fecha_inicio`: Filtrar por fecha de inicio (opcional)
- `fecha_fin`: Filtrar por fecha de fin (opcional)

**Respuesta:**
```json
{
  "data": [
    {
      "id": "uuid-de-tutoria",
      "estudiante_id": "uuid-del-estudiante",
      "fecha_tutoria": "2023-09-25",
      "asignatura": "Cálculo Diferencial",
      "tutor": "Nombre del Tutor",
      "observaciones": "Observaciones de la tutoría"
    }
  ],
  "count": 1
}
```
