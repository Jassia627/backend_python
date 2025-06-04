import re
from typing import Dict, Any
from services.validaciones import Validador

programas = [
    "ADMINISTRACIÓN DE EMPRESAS", "ADMINISTRACIÓN DE EMPRESAS TURÍSTICAS Y HOTELERAS", "COMERCIO INTERNACIONAL",
    "CONTADURÍA PÚBLICA", "DERECHO", "ECONOMÍA", "ENFERMERÍA", "INGENIERÍA AGROINDUSTRIAL",
    "INGENIERIA AMBIENTAL Y SANITARIA", "INGENIERÍA ELECTRÓNICA", "INGENIERÍA DE SISTEMAS",
    "INSTRUMENTACIÓN QUIRÚRGICA", "LICENCIATURA EN ARTE Y FOLCLOR", "LICENCIATURA EN CIENCIAS NATURALES Y EDUCACIÓN AMBIENTAL",
    "LICENCIATURA EN EDUCACIÓN FISICA, RECREACIÓN Y DEPORTES", "LICENCIATURA EN LENGUA CASTELLANA E INGLÉS", "LICENCIATURA EN MATEMÁTICAS",
    "MICROBIOLOGÍA", "SOCIOLOGÍA"
]

tipo_documento_opciones = ["CC", "TI", "CE", "Pasaporte"]
riesgo_opciones = ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"]
estrato_opciones = [1, 2, 3, 4, 5, 6]
estado_participacion_opciones = ["Activo", "Inactivo", "Finalizado"]
tipo_comida_opciones = ["Almuerzo"]
tipo_participante_opciones = ["Admitido", "Nuevo", "Media académica"]
nivel_riesgo_spadies_opciones = ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"]
motivo_intervencion_opciones = [
    "Problemas familiares", "Dificultades emocionales", "Estrés académico", "Ansiedad / depresión", "Problemas de adaptación", "Otros"
]
tipo_intervencion_opciones = ["Asesoría", "Taller", "Otro"]

def validar_campos_comunes(datos: Dict[str, Any]) -> Dict[str, str]:
    err = {}
    
    # Normalizar campos: si existen las versiones con sufijo '1', usarlas como versiones normales
    if "numero_documento1" in datos and "numero_documento" not in datos:
        datos["numero_documento"] = datos["numero_documento1"]
    
    if "correo1" in datos and "correo" not in datos:
        datos["correo"] = datos["correo1"]

    if not Validador.en_lista(datos.get("tipo_documento"), tipo_documento_opciones):
        err["tipo_documento"] = "Tipo de documento requerido o inválido"

    if not Validador.solo_numeros(datos.get("numero_documento", "")) or not (7 <= len(str(datos.get("numero_documento", ""))) <= 10):
        err["numero_documento"] = "Número de documento requerido (7-10 dígitos numéricos)"

    if not Validador.solo_letras(datos.get("nombres", "")) or not (2 <= len(datos["nombres"]) <= 50):
        err["nombres"] = "Nombres requeridos (solo letras y espacios)"

    if not Validador.solo_letras(datos.get("apellidos", "")) or not (2 <= len(datos["apellidos"]) <= 50):
        err["apellidos"] = "Apellidos requeridos (solo letras y espacios)"

    correo = datos.get("correo", "")
    if not Validador.es_texto(correo) or not re.match(r'^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$', correo):
        err["correo"] = "Correo requerido y válido"

    telefono = datos.get("telefono")
    if telefono not in (None, "") and not re.match(r'^3\d{9}$', str(telefono)):
        err["telefono"] = "Teléfono debe ser celular colombiano (3** *** ****)"

    direccion = datos.get("direccion", "")
    if direccion and not Validador.es_texto(direccion, 100):
        err["direccion"] = "Dirección máxima 100 caracteres"

    if not Validador.en_lista(datos.get("programa_academico"), programas):
        err["programa_academico"] = "Programa requerido y válido"

    if not isinstance(datos.get("semestre"), int) or datos["semestre"] < 1:
        err["semestre"] = "Semestre requerido y debe ser mayor o igual a 1"

    if not Validador.en_lista(datos.get("riesgo_desercion"), riesgo_opciones):
        err["riesgo_desercion"] = "Riesgo requerido y válido"

    if not isinstance(datos.get("estrato"), int) or datos["estrato"] not in estrato_opciones:
        err["estrato"] = "Estrato requerido (1-6)"

    return err

def validar_POA(datos: Dict[str, Any]) -> Dict[str, str]:
    """
    Valida los datos para POA según tabla oficial UPC.
    
    Campos obligatorios específicos de POA:
    - Nombre_apellido, Correo, Celular, Semestre, nivel_riesgo, requiere_tutoria
    - fecha, Docente_tutor, Facultad, Programa, Periodo_Académico, Ciclo_formacion
    - Nombre_asignatura, Tema, Objetivo, Metodologia, Logros, FIRMA_TUTOR
    """
    err = {}
    
    # No usar campos comunes ya que POA tiene sus propios campos específicos
    
    # === CAMPOS OBLIGATORIOS ESPECÍFICOS DE POA ===
    
    # Nombre_apellido (obligatorio)
    nombre_apellido = datos.get("Nombre_apellido", "").strip()
    if not nombre_apellido:
        err["Nombre_apellido"] = "Nombre y apellido son obligatorios"
    elif not Validador.solo_letras(nombre_apellido) or len(nombre_apellido) > 100:
        err["Nombre_apellido"] = "Nombre y apellido solo pueden contener letras y espacios (máximo 100 caracteres)"
    
    # Correo (obligatorio, institucional)
    correo = datos.get("Correo", "").strip()
    if not correo:
        err["Correo"] = "Correo institucional es obligatorio"
    elif not re.match(r'^[\w\-.]+@unicesar\.edu\.co$', correo):
        err["Correo"] = "Correo debe ser institucional (*@unicesar.edu.co)"
    
    # Celular (obligatorio)
    celular = datos.get("Celular", "")
    if not celular:
        err["Celular"] = "Número de celular es obligatorio"
    elif not re.match(r'^3\d{9}$', str(celular)):
        err["Celular"] = "Celular debe ser formato colombiano (3** *** ****)"
    
    # Semestre (obligatorio, 1-10)
    semestre = datos.get("Semestre")
    if not isinstance(semestre, int):
        err["Semestre"] = "Semestre es obligatorio y debe ser número entero"
    elif not (1 <= semestre <= 10):
        err["Semestre"] = "Semestre debe estar entre 1 y 10"
    
    # nivel_riesgo (obligatorio)
    if not Validador.en_lista(datos.get("nivel_riesgo"), nivel_riesgo_spadies_opciones):
        err["nivel_riesgo"] = "Nivel de riesgo obligatorio. Valores válidos: 'Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto'"
    
    # requiere_tutoria (obligatorio, booleano)
    if not Validador.es_booleano(datos.get("requiere_tutoria")):
        err["requiere_tutoria"] = "Campo 'requiere_tutoria' es obligatorio y debe ser booleano (true/false)"
    
    # fecha (obligatorio, dd-mm-yyyy)
    fecha = datos.get("fecha")
    if not fecha:
        err["fecha"] = "Fecha de registro es obligatoria"
    elif not Validador.es_fecha_valida(fecha):
        err["fecha"] = "Fecha debe tener formato válido (dd-mm-yyyy o yyyy-mm-dd)"
    
    # Docente_tutor (obligatorio)
    docente_tutor = datos.get("Docente_tutor", "").strip()
    if not docente_tutor:
        err["Docente_tutor"] = "Nombre del docente tutor es obligatorio"
    elif not Validador.solo_letras(docente_tutor) or len(docente_tutor) > 100:
        err["Docente_tutor"] = "Docente tutor solo puede contener letras y espacios (máximo 100 caracteres)"
    
    # Facultad (obligatorio, lista UPC)
    facultades_upc = [
        "FACULTAD DE CIENCIAS ADMINISTRATIVAS, CONTABLES Y ECONÓMICAS",
        "FACULTAD DE DERECHO, CIENCIAS POLÍTICAS Y SOCIALES", 
        "FACULTAD DE CIENCIAS DE LA SALUD",
        "FACULTAD DE INGENIERÍAS Y TECNOLOGÍAS",
        "FACULTAD DE EDUCACIÓN, CIENCIAS HUMANAS Y BELLAS ARTES"
    ]
    if not Validador.en_lista(datos.get("Facultad"), facultades_upc):
        err["Facultad"] = "Facultad es obligatoria y debe ser una de las facultades UPC válidas"
    
    # Programa (obligatorio, lista UPC)
    if not Validador.en_lista(datos.get("Programa"), programas):
        err["Programa"] = "Programa académico es obligatorio y debe ser uno de los programas UPC válidos"
    
    # Periodo_Académico (obligatorio, formato yyyy-S)
    periodo = datos.get("Periodo_Académico", "")
    if not periodo:
        err["Periodo_Académico"] = "Periodo académico es obligatorio"
    elif not re.match(r'^\d{4}-[12]$', str(periodo)):
        err["Periodo_Académico"] = "Periodo académico debe tener formato yyyy-S (ejemplo: 2024-1)"
    
    # Ciclo_formacion (obligatorio)
    ciclos_validos = ["pregrado", "postgrado"]
    ciclo = datos.get("Ciclo_formacion", "").lower()
    if not ciclo:
        err["Ciclo_formacion"] = "Ciclo de formación es obligatorio"
    elif ciclo not in ciclos_validos:
        err["Ciclo_formacion"] = "Ciclo de formación debe ser 'pregrado' o 'postgrado'"
    
    # Nombre_asignatura (obligatorio)
    asignatura = datos.get("Nombre_asignatura", "").strip()
    if not asignatura:
        err["Nombre_asignatura"] = "Nombre de asignatura es obligatorio"
    elif not re.match(r'^[a-zA-ZÀ-ÿ0-9\s]+$', asignatura) or len(asignatura) > 100:
        err["Nombre_asignatura"] = "Asignatura solo puede contener letras, números y espacios (máximo 100 caracteres)"
    
    # Tema (obligatorio)
    tema = datos.get("Tema", "").strip()
    if not tema:
        err["Tema"] = "Tema es obligatorio"
    elif not re.match(r'^[a-zA-ZÀ-ÿ0-9\s]+$', tema) or len(tema) > 150:
        err["Tema"] = "Tema solo puede contener letras, números y espacios (máximo 150 caracteres)"
    
    # Objetivo (obligatorio)
    objetivo = datos.get("Objetivo", "").strip()
    if not objetivo:
        err["Objetivo"] = "Objetivo es obligatorio"
    elif not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\.,;:¡!¿?\-()]+$', objetivo) or len(objetivo) > 300:
        err["Objetivo"] = "Objetivo puede contener letras, números, signos de puntuación y espacios (máximo 300 caracteres)"
    
    # Metodologia (obligatorio)
    metodologia = datos.get("Metodologia", "").strip()
    if not metodologia:
        err["Metodologia"] = "Metodología es obligatoria"
    elif not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\.,;:¡!¿?\-()]+$', metodologia) or len(metodologia) > 300:
        err["Metodologia"] = "Metodología puede contener letras, números, signos de puntuación y espacios (máximo 300 caracteres)"
    
    # Logros (obligatorio)
    logros = datos.get("Logros", "").strip()
    if not logros:
        err["Logros"] = "Logros son obligatorios"
    elif not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\.,;:¡!¿?\-()]+$', logros) or len(logros) > 300:
        err["Logros"] = "Logros pueden contener letras, números, signos de puntuación y espacios (máximo 300 caracteres)"
    
    # FIRMA_TUTOR (obligatorio)
    firma = datos.get("FIRMA_TUTOR", "").strip()
    if not firma:
        err["FIRMA_TUTOR"] = "Firma del tutor es obligatoria"
    elif not Validador.solo_letras(firma) or len(firma) > 100:
        err["FIRMA_TUTOR"] = "Firma del tutor solo puede contener letras y espacios (máximo 100 caracteres)"

    return err

def validar_pops(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.en_lista(datos.get("motivo_intervencion"), motivo_intervencion_opciones):
        err["motivo_intervencion"] = "Motivo de intervención requerido y válido"

    if not Validador.en_lista(datos.get("tipo_intervencion"), tipo_intervencion_opciones):
        err["tipo_intervencion"] = "Tipo de intervención requerido y válido"

    if not Validador.es_fecha_valida(datos.get("fecha_atencion", "")):
        err["fecha_atencion"] = "Fecha de atención requerida en formato YYYY-MM-DD"

    if datos.get("seguimiento") not in (None, "") and not Validador.es_texto(datos["seguimiento"], 255):
        err["seguimiento"] = "Seguimiento debe ser texto válido (máximo 255 caracteres)"

    return err

def validar_apoyo_socioeconomico(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.es_texto(datos.get("tipo_vulnerabilidad", ""), 100):
        err["tipo_vulnerabilidad"] = "Tipo de vulnerabilidad requerido y válido"

    if datos.get("observaciones") not in (None, "") and not Validador.es_texto(datos["observaciones"], 255):
        err["observaciones"] = "Observaciones deben ser texto válido (máximo 255 caracteres)"

    return err

def validar_povau(datos: Dict[str, Any]) -> Dict[str, str]:
    """
    Valida los datos para POVAU según tabla oficial UPC.
    
    Campos requeridos:
    - tipo_participante: ['Admitido', 'Nuevo', 'Media académica']
    - riesgo_spadies: ['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto']
    - fecha_ingreso_programa: formato dd-mm-yyyy
    
    Campos opcionales:
    - observaciones: máximo 255 caracteres
    """
    err = validar_campos_comunes(datos)

    # Validar tipo_participante (OBLIGATORIO)
    if not Validador.en_lista(datos.get("tipo_participante"), tipo_participante_opciones):
        err["tipo_participante"] = "Tipo de participante requerido. Valores válidos: 'Admitido', 'Nuevo', 'Media académica'"

    # Validar riesgo_spadies (OBLIGATORIO)
    if not Validador.en_lista(datos.get("riesgo_spadies"), nivel_riesgo_spadies_opciones):
        err["riesgo_spadies"] = "Nivel de riesgo SPADIES requerido. Valores válidos: 'Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto'"

    # Validar fecha_ingreso_programa (OBLIGATORIO)
    fecha_ingreso = datos.get("fecha_ingreso_programa")
    if not fecha_ingreso:
        err["fecha_ingreso_programa"] = "Fecha de ingreso al programa es obligatoria"
    elif not Validador.es_fecha_valida(fecha_ingreso):
        err["fecha_ingreso_programa"] = "Fecha de ingreso debe tener formato válido (dd-mm-yyyy o yyyy-mm-dd)"

    # Validar observaciones (OPCIONAL)
    observaciones = datos.get("observaciones")
    if observaciones is not None and observaciones != "":
        if not Validador.es_texto(observaciones, 255):
            err["observaciones"] = "Observaciones deben ser texto válido (máximo 255 caracteres)"

    return err

def validar_taller_habilidades(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.es_texto(datos.get("nombre_taller", ""), 100):
        err["nombre_taller"] = "Nombre del taller requerido y válido"

    if not Validador.es_fecha_valida(datos.get("fecha_taller", "")):
        err["fecha_taller"] = "Fecha requerida en formato YYYY-MM-DD"

    if datos.get("observaciones") not in (None, "") and not Validador.es_texto(datos["observaciones"], 255):
        err["observaciones"] = "Observaciones deben ser texto válido (máximo 255 caracteres)"

    return err

def validar_seguimiento_academico(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.en_lista(datos.get("estado_participacion"), estado_participacion_opciones):
        err["estado_participacion"] = "Estado de participación requerido y válido"

    if not Validador.es_texto(datos.get("observaciones_permanencia", ""), 255):
        err["observaciones_permanencia"] = "Observaciones requeridas y válidas"

    return err

def validar_comedor_universitario(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.es_texto(datos.get("condicion_socioeconomica", ""), 100):
        err["condicion_socioeconomica"] = "Condición socioeconómica requerida y válida"

    if not Validador.es_fecha_valida(datos.get("fecha_solicitud", "")):
        err["fecha_solicitud"] = "Fecha de solicitud requerida y válida"

    if "aprobado" in datos and not Validador.es_booleano(datos.get("aprobado")):
        err["aprobado"] = "Campo 'aprobado' debe ser booleano"

    tipo_comida = datos.get("tipo_comida", "Almuerzo")
    if tipo_comida and not Validador.en_lista(tipo_comida, tipo_comida_opciones):
        err["tipo_comida"] = "Tipo de comida requerido y válido"

    raciones = datos.get("raciones_asignadas", 1)
    if raciones is not None and not Validador.en_rango_numerico(raciones, 1, 100):
        err["raciones_asignadas"] = "Raciones asignadas debe ser un número entre 1 y 100"

    if datos.get("observaciones") not in (None, "") and not Validador.es_texto(datos["observaciones"], 255):
        err["observaciones"] = "Observaciones deben ser texto válido (máximo 255 caracteres)"

    return err
