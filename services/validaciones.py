import re
from datetime import datetime

class Validador:

    @staticmethod
    def es_fecha_valida(fecha, formato='%Y-%m-%d'):
        try:
            d = datetime.strptime(fecha, formato)
            return d.strftime(formato) == fecha
        except ValueError:
            return False

    @staticmethod
    def es_texto(texto, maximo=255):
        return isinstance(texto, str) and len(texto.strip()) <= maximo

    @staticmethod
    def solo_letras(texto: str) -> bool:
        return bool(re.fullmatch(r'^[\w\s]+$', texto, re.UNICODE))

    @staticmethod
    def solo_numeros(valor):
        return bool(re.fullmatch(r'^\d+$', str(valor)))

    @staticmethod
    def en_rango_numerico(numero, minimo, maximo):
        try:
            num = float(numero)
            return minimo <= num <= maximo
        except (ValueError, TypeError):
            return False

    @staticmethod
    def en_lista(valor, lista):
        return valor in lista

    @staticmethod
    def arreglo_con_valores_validos(arreglo, claves_esperadas, valores_validos):
        for clave in claves_esperadas:
            if clave not in arreglo or arreglo[clave] not in valores_validos:
                return False
        return True

    @staticmethod
    def validar_disponibilidad(disponibilidad, dias, turnos):
        if not isinstance(disponibilidad, dict):
            return False

        for dia in dias:
            if dia not in disponibilidad:
                continue

            for turno in turnos:
                if turno in disponibilidad[dia]:
                    valor = str(disponibilidad[dia][turno]).strip()
                    if valor and not Validador.es_texto(valor, 20):
                        return False
        return True

    @staticmethod
    def es_booleano(valor):
        return isinstance(valor, bool) or valor in ['true', 'false', 1, 0, '1', '0']

    @staticmethod
    def es_alfanumerico(texto: str) -> bool:
        return bool(re.fullmatch(r'^[a-zA-Z0-9]+$', texto))

    @staticmethod
    def es_ciclo_academico(ciclo: str) -> bool:
        return bool(re.fullmatch(r'^\d{4}-(1|2)$', ciclo))

    @staticmethod
    def es_hora_valida(hora: str) -> bool:
        return bool(re.fullmatch(r'^(?:[01]\d|2[0-3]):[0-5]\d$', hora))
