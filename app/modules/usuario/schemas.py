from pydantic import BaseModel, EmailStr
from app.modules.usuario.enums import PerfilEnum

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    perfil: PerfilEnum

class UsuarioCreate(UsuarioBase):
    senha: str # Senha pura que será convertida em hash

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    perfil: str
    nome: str