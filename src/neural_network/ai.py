from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class AbstractNeuralNetwork(ABC):
    @abstractmethod
    async def execute(self, frame: Any) -> Dict[str, Tuple[int, int]]:
        """
        Реализация обработки кадра нейронкой

        :param frame: Кадр от aiortc
        :return:
        """

        raise NotImplemented
