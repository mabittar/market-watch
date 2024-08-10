from abc import ABC, abstractmethod
from typing import Any


class BaseApplicatoin(ABC):
    @abstractmethod
    async def execute(self, input: Any):
        raise NotImplementedError
