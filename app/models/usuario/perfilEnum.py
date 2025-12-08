import enum


class PerfilEnum(str, enum.Enum):
    ADMIN = "Admin"
    ANALISTA = "Analista"
    GESTOR = "Gestor"
    FORNECEDOR = "Fornecedor"