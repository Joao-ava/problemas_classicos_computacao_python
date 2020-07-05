from __future__ import annotations
from typing import List, Optional
from generic_search import bfs, Node, node_to_path


MAX_NUM: int = 3


class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries  # missionarios a oeste
        self.wc: int = cannibals  # canibais a oeste
        self.em: int = MAX_NUM - self.wm  # missionarios a leste
        self.ec: int = MAX_NUM - self.wc  # canibais a leste
        self.boat: bool = boat


    def goal_test(self) -> bool:
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM


    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm > 0:
            return False

        if self.em < self.ec and self.em > 0:
            return False

        return True

    def successors(self) -> List[MCState]:
        sucs: List[MCState] = []

        if self.boat:  # Barco indo para a direita
            if self.wm > 1:
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wc > 0) and (self.wm > 0):
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))

        else:
            if self.em > 1:
                sucs.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:
                sucs.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:
                sucs.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:
                sucs.append(MCState(self.wm, self.wc + 1, not self.boat))
            if (self.ec > 0) and (self.em > 0):
                sucs.append(MCState(self.wm + 1, self.wc + 1, not self.boat))

        return [x for x in sucs if x.is_legal]


    def __str__(self) -> str:
        return f"""
			{self.em} missionarios a leste
			{self.ec} canibais a leste
			{self.wm} missionarios a oeste
			{self.wc} canibais a oeste
		"""


def display_solution(path: List[MCState]) -> None:
    if len(path) == 0:
        return

    old_state: MCState = path[0]
    print(old_state)

    for current_state in path[1:]:
        if current_state.boat:
            print(f"{old_state.em - current_state.em} missionarios e {old_state.ec - current_state.ec} canibais se moveram do oeste ao leste")

        else:
            print(f"{old_state.wm - current_state.wm} missionarios e {old_state.wc - current_state.wc} canibais se moveram do leste ao oeste")

        print(current_state)
        old_state = current_state


if __name__ == "__main__":
    start: MCState = MCState(MAX_NUM, MAX_NUM, True)
    solution: Optional[Node[MCState]] = bfs(
        start, MCState.goal_test, MCState.successors)

    if solution is None:
        print("Não a solução")

    else:
        path: List[MCState] = node_to_path(solution)
        display_solution(path)
