import enum


class StatusContratoEnum(str, enum.Enum):
    RASCUNHO = "Rascunho"
    ATIVO = "Ativo"
    VENCIDO = "Vencido"
    CANCELADO = "Cancelado"