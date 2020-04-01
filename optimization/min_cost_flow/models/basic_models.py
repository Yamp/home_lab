from dataclasses import dataclass


@dataclass
class Node:
    """ Вершина, которая содержит количество потока рождаемого или требуемого в данной точке """
    _id: object  # любой объект может быть ключом
    supply: float

    def __init__(self, id: object, supply: float):
        self._id = id
        self.supply = supply

    def __hash__(self):
        return hash((self.__class__, self.id))

    def __eq__(self, other):
        return self.id == other.id

    @property
    def id(self):
        return self._id


@dataclass
class RestrictedNode(Node):
    """ Вершина, которая дополнитеьно имеет ограничение по количеству потока по проходящего по ней """
    capacity: float

    def __init__(self, id: object, supply: float, capacity: float):
        super().__init__(id, supply)
        self.capacity = capacity


@dataclass
class Edge:
    """ Ребро графа. Flow не задается и появляется после решения солвером таски """
    start: Node
    end: Node

    capacity: float
    cost: float
    flow: float = None

    def __hash__(self):
        return hash((self.__class__.__name__, self.start, self.end))

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __str__(self):
        return f'({self.start}->{self.end}) flow={self.flow}/{self.capacity} unit_cost={self.cost}'

    def clip_flow(self):
        self.flow = min(self.flow, self.capacity)
