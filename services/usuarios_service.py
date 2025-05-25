from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid
import hashlib
import jwt

from data.usuarios_data import UsuariosData
from models.usuarios import UsuarioCreate, UsuarioResponse, UsuarioUpdate, Token

class UsuariosService:
    """Servicio para la gestión de usuarios."""
    
    def __init__(self):
        """Inicializa el servicio con acceso a datos de usuarios."""
        self.data = UsuariosData()
        # Clave secreta para JWT (en una implementación real, debería estar en variables de entorno)
        self.SECRET_KEY = "clave_secreta_para_jwt"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    def get_all_usuarios(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los usuarios.
        
        Returns:
            Lista de usuarios
        """
        return self.data.get_all()
    
    def get_usuario_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            id: ID del usuario
            
        Returns:
            Usuario encontrado o None si no existe
        """
        return self.data.get_by_id(id)
    
    def get_usuario_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario
            
        Returns:
            Usuario encontrado o None si no existe
        """
        return self.data.get_by_email(email)
    
    def get_usuarios_by_rol(self, rol: str) -> List[Dict[str, Any]]:
        """
        Obtiene usuarios por rol.
        
        Args:
            rol: Rol del usuario (Admin, Docente, etc.)
            
        Returns:
            Lista de usuarios con el rol especificado
        """
        return self.data.get_by_rol(rol)
    
    def get_usuarios_activos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los usuarios activos.
        
        Returns:
            Lista de usuarios activos
        """
        return self.data.get_activos()
    
    def _hash_password(self, password: str) -> str:
        """
        Genera un hash para la contraseña.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        # En una implementación real, se debería usar un algoritmo más seguro
        # como bcrypt o Argon2
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_usuario(self, usuario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo usuario.
        
        Args:
            usuario_data: Datos del usuario
            
        Returns:
            Usuario creado
        """
        # Verificar si ya existe un usuario con el mismo email
        existing = self.data.get_by_email(usuario_data.get("email"))
        if existing:
            raise ValueError(f"Ya existe un usuario con el email {usuario_data.get('email')}")
        
        # Hashear la contraseña
        if "password" in usuario_data:
            usuario_data["password"] = self._hash_password(usuario_data["password"])
        
        return self.data.create(usuario_data)
    
    def update_usuario(self, id: str, usuario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un usuario existente.
        
        Args:
            id: ID del usuario
            usuario_data: Datos a actualizar
            
        Returns:
            Usuario actualizado
        """
        # Verificar si el usuario existe
        existing = self.data.get_by_id(id)
        if not existing:
            raise ValueError(f"No existe un usuario con el ID {id}")
        
        # Si se está actualizando el email, verificar que no exista otro usuario con ese email
        if "email" in usuario_data and usuario_data["email"] != existing["email"]:
            email_check = self.data.get_by_email(usuario_data["email"])
            if email_check and email_check["id"] != id:
                raise ValueError(f"Ya existe otro usuario con el email {usuario_data['email']}")
        
        # Hashear la contraseña si se está actualizando
        if "password" in usuario_data:
            usuario_data["password"] = self._hash_password(usuario_data["password"])
        
        return self.data.update(id, usuario_data)
    
    def delete_usuario(self, id: str) -> bool:
        """
        Elimina un usuario.
        
        Args:
            id: ID del usuario
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        # Verificar si el usuario existe
        existing = self.data.get_by_id(id)
        if not existing:
            raise ValueError(f"No existe un usuario con el ID {id}")
        
        return self.data.delete(id)
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario por email y contraseña.
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            Usuario autenticado o None si la autenticación falla
        """
        user = self.data.get_by_email(email)
        if not user:
            return None
        
        password_hash = self._hash_password(password)
        if user["password"] != password_hash:
            return None
        
        return user
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Crea un token de acceso JWT.
        
        Args:
            data: Datos a incluir en el token
            expires_delta: Tiempo de expiración del token
            
        Returns:
            Token de acceso
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def login(self, email: str, password: str) -> Optional[Token]:
        """
        Inicia sesión de un usuario.
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            Token de acceso o None si la autenticación falla
        """
        user = self.authenticate_user(email, password)
        if not user:
            return None
        
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user["email"], "id": str(user["id"]), "rol": user["rol"]},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
