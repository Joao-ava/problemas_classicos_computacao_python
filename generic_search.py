from __future__ import annotations
from typing import (
    TypeVar,
    Iterable,
    Sequence,
    Generic,
    List,
    Callable,
    Set,
    Deque,
    Dict,
    Any,
    Optional,
    Protocol,
)
from heapq import heappush, heappop

T = TypeVar('T')


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for i in iterable:
        if i == key:
            return True

    return False


C = TypeVar('C', bound="Comparable")


class Comparable(Protocol):
    def __eq__(self, other: Any):
        ...

    def __lt__(self, other: C):
        ...

    def __gt__(self, other: C):
        return (not self < other) and self != other

    def __le__(self, other: C):
        return self < other or self == other

    def __ge__(self, other: C):
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1

    while low <= high:
        mid: int = (low + high) // 2

        if sequence[mid] < key:
            low = mid + 1

        elif sequence[mid] > key:
            high = mid - 1

        else:
            return True

    return False


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self):
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node],
                 cost: float = 0.0, heuristic: float = 0.0
                 ) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node):
        return (self.cost + self.heuristic) < (other.cost + self.heuristic)


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier correspondea os lugares que ainda não visitamos
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))

    # explored corresponte locais em que já estivemos
    explored: Set[T] = {initial}

    # continua enquanto houver mais lugares para explorar
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        # se encontramos o objetivo, terminamos
        if goal_test(current_state):
            return current_node

        # verifica para onde podemos ir em seguida e que ainda não tenha sido explorado
        for child in successors(current_state):
            if child in explored:  # ignora os filhos que já tenham sido explorados
                continue

            # adiciona aos locais explorados
            explored.add(child)
            # adiciona local a ir
            frontier.push(Node(child, current_node))

    return None  # passamos por todos os lugares e não atingimos o objetivo


def node_to_path(node: Node[T]) -> List:
    path: List[T] = [node.state]

    # trabalha no sentido inverso, do final para o inicio
    while node.parent is not None:
        node = node.parent
        path.append(node.state)

    path.reverse()

    return path


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self):
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()

    def __repr__(self) -> str:
        return repr(self._container)


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))

    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            if child in explored:
                continue

            explored.add(child)
            frontier.push(Node(child, current_node))

    return None


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)

    def pop(self) -> T:
        return heappop(self._container)

    def __repr__(self) -> str:
        return repr(self._container)


def astar(initial: T, goal_test: Callable[[T], bool],
          successors: Callable[[T], List[T]], heuristic: Callable[[T], float]
          ) -> Optional[T]:
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))

    explored: Dict[T, float] = {initial: 0.0}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            new_coast: float = current_node.cost + 1

            if child not in explored or explored[child] > new_coast:
                explored[child] = new_coast
                frontier.push(Node(child, current_node,
                                   new_coast, heuristic(child)))

    return None
