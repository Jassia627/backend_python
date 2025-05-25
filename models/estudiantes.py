from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
from datetime import datetime

class EstudianteBase(BaseModel):
    """Modelo base para datos de estudiante."""
    documento: str
    tipo_documento: str
    nombres: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: str
    estrato: Optional[int] = None

class EstudianteCreate(EstudianteBase):
    """Modelo para crear un estudiante."""
    pass

class EstudianteUpdate(BaseModel):
    """Modelo para actualizar un estudiante."""
    documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: Optional[str] = None
    semestre: Optional[str] = None
    estrato: Optional[int] = None

class EstudianteResponse(EstudianteBase):
    """Modelo para respuesta de estudiante."""
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
