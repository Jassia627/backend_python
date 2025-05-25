from typing import Dict, List, Any, Optional
from .base_data import BaseData
from config import supabase

class UsuariosData(BaseData):
    """Clase para el acceso a datos de usuarios."""
    
    def __init__(self):
        """Inicializa el acceso a datos para la tabla de usuarios."""
        super().__init__("usuarios")
    
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario
            
        Returns:
            Usuario encontrado o None si no existe
        """
        response = supabase.table(self.table_name).select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    
    def get_by_rol(self, rol: str) -> List[Dict[str, Any]]:
        """
        Obtiene usuarios por rol.
        
        Args:
            rol: Rol del usuario (Admin, Docente, etc.)
            
        Returns:
            Lista de usuarios con el rol especificado
        """
        response = supabase.table(self.table_name).select("*").eq("rol", rol).execute()
        return response.data
    
    def get_activos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los usuarios activos.
        
        Returns:
            Lista de usuarios activos
        """
        response = supabase.table(self.table_name).select("*").eq("estado", True).execute()
        return response.data
    
    def authenticate(self, email: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario por email y contraseña hasheada.
        
        Args:
            email: Email del usuario
            password_hash: Hash de la contraseña
            
        Returns:
            Usuario autenticado o None si la autenticación falla
        """
        # Nota: En una implementación real, se debería usar un método más seguro
        # para autenticar usuarios, como JWT o OAuth
        user = self.get_by_email(email)
        if user and user.get("password") == password_hash:
            return user
        return None
