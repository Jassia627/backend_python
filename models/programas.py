from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
from datetime import datetime

class ProgramaBase(BaseModel):
    """Modelo base para datos de programa académico."""
    codigo: str
    nombre: str
    facultad: str
    nivel: str  # Pregrado, Posgrado, etc.
    modalidad: Optional[str] = None  # Presencial, Virtual, etc.
    estado: Optional[bool] = True

class ProgramaCreate(ProgramaBase):
    """Modelo para crear un programa académico."""
    pass

class ProgramaUpdate(BaseModel):
    """Modelo para actualizar un programa académico."""
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    facultad: Optional[str] = None
    nivel: Optional[str] = None
    modalidad: Optional[str] = None
    estado: Optional[bool] = None

class ProgramaResponse(ProgramaBase):
    """Modelo para respuesta de programa académico."""
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
