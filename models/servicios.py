from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

class ServicioBase(BaseModel):
    """Modelo base para datos de servicio."""
    nombre: str
    descripcion: str
    tipo: str  # Psicología, Tutoría, etc.
    estado: Optional[bool] = True

class ServicioCreate(ServicioBase):
    """Modelo para crear un servicio."""
    pass

class ServicioUpdate(BaseModel):
    """Modelo para actualizar un servicio."""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    estado: Optional[bool] = None

class ServicioResponse(ServicioBase):
    """Modelo para respuesta de servicio."""
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Modelos para asistencias a servicios
class AsistenciaBase(BaseModel):
    """Modelo base para datos de asistencia a servicio."""
    estudiante_id: uuid.UUID
    servicio_id: uuid.UUID
    fecha: datetime
    observaciones: Optional[str] = None

class AsistenciaCreate(AsistenciaBase):
    """Modelo para crear una asistencia."""
    pass

class AsistenciaUpdate(BaseModel):
    """Modelo para actualizar una asistencia."""
    estudiante_id: Optional[uuid.UUID] = None
    servicio_id: Optional[uuid.UUID] = None
    fecha: Optional[datetime] = None
    observaciones: Optional[str] = None

class AsistenciaResponse(AsistenciaBase):
    """Modelo para respuesta de asistencia."""
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
