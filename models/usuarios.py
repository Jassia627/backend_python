from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
import uuid
from datetime import datetime

class UsuarioBase(BaseModel):
    """Modelo base para datos de usuario."""
    nombre: str
    apellido: str
    email: EmailStr
    rol: str  # Admin, Docente, Estudiante, etc.
    estado: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    """Modelo para crear un usuario."""
    password: str

class UsuarioUpdate(BaseModel):
    """Modelo para actualizar un usuario."""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[str] = None
    estado: Optional[bool] = None
    password: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    """Modelo para respuesta de usuario."""
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UsuarioLogin(BaseModel):
    """Modelo para login de usuario."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Modelo para token de autenticación."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Modelo para datos del token."""
    email: Optional[str] = None
    id: Optional[str] = None
    rol: Optional[str] = None
