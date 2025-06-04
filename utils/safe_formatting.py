"""
Utilidades para formatear datos de forma segura para React.
"""

def safe_str(value, default="N/A"):
    """Convierte cualquier valor a string de forma segura."""
    if value is None:
        return default
    if isinstance(value, (dict, list, tuple)):
        return default
    try:
        return str(value).strip() if str(value).strip() else default
    except:
        return default

def safe_int(value, default=0):
    """Convierte cualquier valor a entero de forma segura."""
    if value is None:
        return default
    try:
        return int(value)
    except:
        return default

def safe_bool(value, default=False):
    """Convierte cualquier valor a booleano de forma segura."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    try:
        return bool(value)
    except:
        return default

def safe_float(value, default=0.0):
    """Convierte cualquier valor a float de forma segura."""
    if value is None:
        return default
    try:
        return float(value)
    except:
        return default 