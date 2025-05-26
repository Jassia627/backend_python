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
nivel_riesgo_spadies_opciones = ["Bajo", "Medio", "Alto"]
motivo_intervencion_opciones = [
    "Problemas familiares", "Dificultades emocionales", "Estrés académico", "Ansiedad / depresión", "Problemas de adaptación", "Otros"
]
tipo_intervencion_opciones = ["Asesoría", "Taller", "Otro"]

def validar_campos_comunes(datos: Dict[str, Any]) -> Dict[str, str]:
    err = {}

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

<<<<<<< HEAD
    telefono = datos.get("telefono")
    if telefono not in (None, "") and not re.match(r'^3\d{9}$', str(telefono)):
        err["telefono"] = "Teléfono debe ser celular colombiano (3** *** ****)"

    direccion = datos.get("direccion", "")
    if direccion and not Validador.es_texto(direccion, 100):
=======
    if datos.get("telefono") and not re.match(r'^3\d{9}$', str(datos["telefono"])):
        err["telefono"] = "Teléfono debe ser celular colombiano (3** *** ****)"

    if datos.get("direccion") and not Validador.es_texto(datos["direccion"], 100):
>>>>>>> 7d306b56a16be3d40704e76a6e7ec2bdd04cf0fd
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
    err = validar_campos_comunes(datos)

    if not Validador.en_lista(datos.get("nivel_riesgo"), nivel_riesgo_spadies_opciones):
        err["nivel_riesgo"] = "Nivel de riesgo requerido y válido"

    if not Validador.es_booleano(datos.get("requiere_tutoria")):
        err["requiere_tutoria"] = "Campo 'requiere_tutoria' es obligatorio y debe ser booleano"

    if not Validador.es_fecha_valida(datos.get("fecha_asignacion", "")):
        err["fecha_asignacion"] = "Fecha de asignación requerida en formato YYYY-MM-DD"

<<<<<<< HEAD
    if datos.get("acciones_apoyo") not in (None, "") and not Validador.es_texto(datos["acciones_apoyo"], 255):
        err["acciones_apoyo"] = "Campo 'acciones_apoyo' debe ser texto válido (máximo 255 caracteres)"

=======
    if not Validador.es_texto(datos.get("acciones_apoyo", ""), 255):
        err["acciones_apoyo"] = "Campo 'acciones_apoyo' es obligatorio y debe ser texto válido"
>>>>>>> 7d306b56a16be3d40704e76a6e7ec2bdd04cf0fd

    return err

def validar_pops(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.en_lista(datos.get("motivo_intervencion"), motivo_intervencion_opciones):
        err["motivo_intervencion"] = "Motivo de intervención requerido y válido"

    if not Validador.en_lista(datos.get("tipo_intervencion"), tipo_intervencion_opciones):
        err["tipo_intervencion"] = "Tipo de intervención requerido y válido"

    if not Validador.es_fecha_valida(datos.get("fecha_atencion", "")):
        err["fecha_atencion"] = "Fecha de atención requerida en formato YYYY-MM-DD"

<<<<<<< HEAD
    if datos.get("seguimiento") not in (None, "") and not Validador.es_texto(datos["seguimiento"], 255):
        err["seguimiento"] = "Seguimiento debe ser texto válido (máximo 255 caracteres)"
=======
    if not Validador.es_texto(datos.get("seguimiento", ""), 255):
        err["seguimiento"] = "Seguimiento requerido y válido"
>>>>>>> 7d306b56a16be3d40704e76a6e7ec2bdd04cf0fd

    return err

def validar_apoyo_socioeconomico(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.es_texto(datos.get("tipo_vulnerabilidad", ""), 100):
        err["tipo_vulnerabilidad"] = "Tipo de vulnerabilidad requerido y válido"

<<<<<<< HEAD
    if datos.get("observaciones") not in (None, "") and not Validador.es_texto(datos["observaciones"], 255):
        err["observaciones"] = "Observaciones deben ser texto válido (máximo 255 caracteres)"
=======
    if not Validador.es_texto(datos.get("observaciones", ""), 255):
        err["observaciones"] = "Observaciones requeridas y válidas"
>>>>>>> 7d306b56a16be3d40704e76a6e7ec2bdd04cf0fd

    return err

def validar_povau(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.en_lista(datos.get("tipo_participante"), tipo_participante_opciones):
        err["tipo_participante"] = "Tipo de participante requerido y válido"

    if not Validador.en_lista(datos.get("riesgo_spadies"), nivel_riesgo_spadies_opciones):
        err["riesgo_spadies"] = "Nivel de riesgo SPADIES requerido y válido"

    if not Validador.es_fecha_valida(datos.get("fecha_ingreso_programa", "")):
        err["fecha_ingreso_programa"] = "Fecha de ingreso requerida y válida"

<<<<<<< HEAD
    if datos.get("observaciones") not in (None, "") and not Validador.es_texto(datos["observaciones"], 255):
        err["observaciones"] = "Observaciones deben ser texto válido (máximo 255 caracteres)"
=======
    if not Validador.es_texto(datos.get("observaciones", ""), 255):
        err["observaciones"] = "Observaciones requeridas y válidas"
>>>>>>> 7d306b56a16be3d40704e76a6e7ec2bdd04cf0fd

    return err

def validar_taller_habilidades(datos: Dict[str, Any]) -> Dict[str, str]:
    err = validar_campos_comunes(datos)

    if not Validador.es_texto(datos.get("nombre_taller", ""), 100):
        err["nombre_taller"] = "Nombre del taller requerido y válido"

    if not Validador.es_fecha_valida(datos.get("fecha_taller", "")):
        err["fecha_taller"] = "Fecha requerida en formato YYYY-MM-DD"

<<<<<<< HEAD
    if datos.get("observaciones") not in (None, "") and not Validador.es_texto(datos["observaciones"], 255):
        err["observaciones"] = "Observaciones deben ser texto válido (máximo 255 caracteres)"
=======
    if not Validador.es_texto(datos.get("observaciones", ""), 255):
        err["observaciones"] = "Observaciones requeridas y válidas"
>>>>>>> 7d306b56a16be3d40704e76a6e7ec2bdd04cf0fd

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

    if not Validador.es_booleano(datos.get("aprobado")):
        err["aprobado"] = "Campo 'aprobado' debe ser booleano"

    if not Validador.en_lista(datos.get("tipo_comida"), tipo_comida_opciones):
        err["tipo_comida"] = "Tipo de comida requerido y válido"

    if not Validador.en_rango_numerico(datos.get("raciones_asignadas", 0), 1, 100):
        err["raciones_asignadas"] = "Raciones asignadas debe ser un número entre 1 y 100"

<<<<<<< HEAD
    if datos.get("observaciones") not in (None, "") and not Validador.es_texto(datos["observaciones"], 255):
        err["observaciones"] = "Observaciones deben ser texto válido (máximo 255 caracteres)"
=======
    if not Validador.es_texto(datos.get("observaciones", ""), 255):
        err["observaciones"] = "Observaciones requeridas y válidas"
>>>>>>> 7d306b56a16be3d40704e76a6e7ec2bdd04cf0fd

    return err
