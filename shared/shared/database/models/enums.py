from enum import StrEnum


class AssetKind(StrEnum):
    STOCK = "stock"
    CRYPTO = "crypto"
    CUSTOM_CRYPTO = "custom_crypto"


class TradeOperation(StrEnum):
    BUY = "buy"
    SELL = "sell"


class SeasonStatus(StrEnum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    ENDED = "ended"
