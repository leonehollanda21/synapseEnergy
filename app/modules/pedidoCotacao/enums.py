import enum


class StatusRFQEnum(str, enum.Enum):
    ABERTA = "Aberta"
    FECHADA = "Fechada"
    CANCELADA = "Cancelada"