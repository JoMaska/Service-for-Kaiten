import enum


class CardType(str, enum.Enum):
    BUG = "bug"
    CARD = "card"