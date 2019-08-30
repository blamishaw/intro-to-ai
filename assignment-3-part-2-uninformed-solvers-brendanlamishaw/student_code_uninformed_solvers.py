from solver import *
import collections
import pdb

step = -1

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        curr = self.currentState
        # print(curr, end=" ")
        # print(curr.depth)
        self.visited[self.currentState] = True
        movables = self.gm.getMovables()

        if self.gm.getGameState() == self.victoryCondition:
            return True

        else:
            if movables and not self.currentState.children:
                for x in range(len(movables)):

                    self.gm.makeMove(movables[x])
                    node = GameState(self.gm.getGameState(), curr.depth+1, movables[x])
                    # self.gm.reverseMove(movables[x])
                    curr.children.append(node)
                    node.parent = curr
                    if node not in self.visited:
                        self.visited[node] = False
                        self.gm.reverseMove(movables[x])
                    else:
                        self.gm.reverseMove(movables[x])
            else:
                if curr.parent != None:
                    curr.depth -= 1
                    self.gm.reverseMove(curr.requiredMovable)

            for child in curr.children:
                if self.visited[child] is False:
                    self.currentState = child
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    break




class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        self.queue = collections.deque()
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        global step
        step += 1

        # if step == 10:
        #     breakpoint()

        # print(self.gm.getGameState(), self.currentState.depth, f"Step: {step}", end=" ")
        # print(f"\tParent: {self.currentState.parent}")


        if self.currentState and self.currentState not in self.queue:
            self.queue.append(self.currentState)

        if self.gm.getGameState() == self.victoryCondition:
            return True

        self.visited[self.currentState] = True
        self.populateChildren()

        for child in self.currentState.children:
            if not self.visited[child] and child not in self.queue:
                self.queue.append(child)

        self.queue.popleft()

        #Create List of movables
        moves = []
        node = self.queue[0]
        while node.parent is not None:
            moves.insert(0, node.requiredMovable)
            node = node.parent

        # Reversing moves
        while self.currentState.parent is not None:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        for move in moves:
            self.gm.makeMove(move)
        self.currentState = self.queue[0]

        return False


    def populateChildren(self):

        movables = self.gm.getMovables()

        if movables and not self.currentState.children:
            for x in range(len(movables)):
                self.gm.makeMove(movables[x])
                node = GameState(self.gm.getGameState(), self.currentState.depth + 1, movables[x])
                self.currentState.children.append(node)
                node.parent = self.currentState
                if node not in self.visited:
                    self.visited[node] = False
                    self.gm.reverseMove(movables[x])
                else:
                    self.gm.reverseMove(movables[x])
