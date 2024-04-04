from abc import ABC, abstractmethod, abstractproperty
import numpy as np

from ..schemas.symbol_params_schema import SymbolParams

class ExchangeApiAdapter(ABC):

    @abstractproperty
    def exchange_name(self) -> str:
        raise NotImplementedError
    

    @abstractmethod
    async def get_symbol_params(self, symbol: str) -> SymbolParams:
        raise NotImplementedError
    

    @abstractmethod
    async def fetch_ohlcv(self, symbol: str, interval: str, start_timestamp: int, end_timestamp: int) -> np.ndarray:
        raise NotImplementedError