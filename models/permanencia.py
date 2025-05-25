from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, date

class TutoriaAcademicaBase(BaseModel):
    """Modelo base para el servicio de Tutoría Académica (POA)."""
    nivel_riesgo: str
    requiere_tutoria: bool = False
    fecha_asignacion: date
    acciones_apoyo: Optional[str] = None

class TutoriaAcademicaCreate(TutoriaAcademicaBase):
    """Modelo para crear una tutoría académica."""
    # Datos del estudiante
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class TutoriaAcademicaResponse(TutoriaAcademicaBase):
    """Modelo para respuesta de tutoría académica."""
    id: uuid.UUID
    estudiante_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    estudiante: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class AsesoriaPsicologicaBase(BaseModel):
    """Modelo base para el servicio de Asesoría Psicológica (POPS)."""
    motivo_intervencion: str
    tipo_intervencion: str
    fecha_atencion: date
    seguimiento: Optional[str] = None

class AsesoriaPsicologicaCreate(AsesoriaPsicologicaBase):
    """Modelo para crear una asesoría psicológica."""
    # Datos del estudiante
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class AsesoriaPsicologicaResponse(AsesoriaPsicologicaBase):
    """Modelo para respuesta de asesoría psicológica."""
    id: uuid.UUID
    estudiante_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    estudiante: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class OrientacionVocacionalBase(BaseModel):
    """Modelo base para el servicio de Orientación Vocacional (POVAU)."""
    tipo_participante: str
    riesgo_spadies: str
    fecha_ingreso_programa: date
    observaciones: Optional[str] = None

class OrientacionVocacionalCreate(OrientacionVocacionalBase):
    """Modelo para crear una orientación vocacional."""
    # Datos del estudiante
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class OrientacionVocacionalResponse(OrientacionVocacionalBase):
    """Modelo para respuesta de orientación vocacional."""
    id: uuid.UUID
    estudiante_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    estudiante: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class ComedorUniversitarioBase(BaseModel):
    """Modelo base para el servicio de Comedor Universitario."""
    condicion_socioeconomica: str
    fecha_solicitud: date
    aprobado: bool = False
    tipo_comida: str
    raciones_asignadas: int
    observaciones: Optional[str] = None

class ComedorUniversitarioCreate(ComedorUniversitarioBase):
    """Modelo para crear un registro de comedor universitario."""
    # Datos del estudiante
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class ComedorUniversitarioResponse(ComedorUniversitarioBase):
    """Modelo para respuesta de comedor universitario."""
    id: uuid.UUID
    estudiante_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    estudiante: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class ApoyoSocioeconomicoBase(BaseModel):
    """Modelo base para el servicio de Apoyo Socioeconómico."""
    tipo_vulnerabilidad: str
    observaciones: Optional[str] = None

class ApoyoSocioeconomicoCreate(ApoyoSocioeconomicoBase):
    """Modelo para crear un apoyo socioeconómico."""
    # Datos del estudiante
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class ApoyoSocioeconomicoResponse(ApoyoSocioeconomicoBase):
    """Modelo para respuesta de apoyo socioeconómico."""
    id: uuid.UUID
    estudiante_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    estudiante: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class TallerHabilidadesBase(BaseModel):
    """Modelo base para el servicio de Talleres de Habilidades."""
    nombre_taller: str
    fecha_taller: date
    observaciones: Optional[str] = None

class TallerHabilidadesCreate(TallerHabilidadesBase):
    """Modelo para crear un taller de habilidades."""
    # Datos del estudiante
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class TallerHabilidadesResponse(TallerHabilidadesBase):
    """Modelo para respuesta de taller de habilidades."""
    id: uuid.UUID
    estudiante_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    estudiante: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class SeguimientoAcademicoBase(BaseModel):
    """Modelo base para el servicio de Seguimiento Académico."""
    estado_participacion: str
    observaciones_permanencia: str

class SeguimientoAcademicoCreate(SeguimientoAcademicoBase):
    """Modelo para crear un seguimiento académico."""
    # Datos del estudiante
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class SeguimientoAcademicoResponse(SeguimientoAcademicoBase):
    """Modelo para respuesta de seguimiento académico."""
    id: uuid.UUID
    estudiante_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    estudiante: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True
