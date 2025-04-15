from abc import ABC, abstractmethod
from typing import Optional


class ParserPort(ABC):
    @abstractmethod
    async def parser(self, config: dict) -> Optional[dict]:
        pass
