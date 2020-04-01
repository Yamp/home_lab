import inspect
from abc import abstractmethod
from dataclasses import dataclass

from optimization.min_cost_flow.models.problem import FlowProblem


@dataclass
class BaseTransformer:
    """
    Базовый класс для трансформеров — штуковин, которые преобразуют задачу,
    а потом преобзаруют обратно ответ, получая ответ на оригинальную задачу.

    С помощью них мы можем сводить одни задачи к другим
    """

    @abstractmethod
    def transform(self, p: FlowProblem):
        pass

    @abstractmethod
    def restore(self, p: FlowProblem):
        pass
