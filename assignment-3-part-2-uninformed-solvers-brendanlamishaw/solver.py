import collections

class UninformedSolver(object):

    """
    Abstract parent class of uninformed solvers. Must not be instantiated directly.

    An uninformed solver systematically explore all reachable game states,
    until all possible game states had been explored, or a specific (winning) game state
    has been reached.

    Attributes:
        gm (GameMaster): the GameMaster to interact with
        visited (dict): a Dictionary to keep track of which GameState has been visited
        currentState (GameState): the GameState object to hold the current game state.
        victoryCondition (object): the game state to search for
    """

    def __init__(self, gameMaster, victoryCondition):
        self.gm = gameMaster
        self.visited = dict()
        self.currentState = GameState(self.gm.getGameState(), 0, None)
        self.visited[self.currentState] = True
        self.victoryCondition = victoryCondition


    def solveOneStep(self):
        """
        Go to the next state that has not been explored.

        Must be overridden by each non-abstract children classes.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        raise NotImplementedError('Subclasses must override solveOneStep(..) to make the next move in searching for the solution')

    def solve(self):
        """
        Run the solver until the winning state is reached, or all viable
        moves have been tried.

        Returns:
            True if the winning state has been reached; False if the game is not won but viable moves have been depleted
        """
        if self.currentState.state == self.victoryCondition:
            return True
        while not self.solveOneStep():
            pass
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False


class GameState(object):

    """
    A generic data structure capable of holding a representation of a game state.

    Multiple GameState objects could be organized into a tree (or graph),
    where the nodes are GameState objects, and the edges are references stored in
    the list, self.children.

    Attributes:
        children (list of GameState): GameState nodes expandable from the the current GameState node
        nextChildToVisit (int): index of the next GameState node in 'children' list of expand
        parent (GameState): reference to the GameState object from which the current one is generated
        requiredMovable (Statement): the MOVABLE Statement which enables the transition from the
                                    parent GameState to this GameState
        state (object): a hashable object that denotes a specific game state, such as a Tuple of Tuples
        depth (int): the depth of the current GameState -- the number of moves that had been made to reach the
                        current game state
    """

    FIRST_CHILD_INDEX = 0

    def __init__(self, state, depth, movableToReachThisState):
        self.children = []
        self.nextChildToVisit = GameState.FIRST_CHILD_INDEX
        self.parent = None
        self.requiredMovable = movableToReachThisState
        self.state = state
        self.depth = depth

    def __eq__(self, other):
        return self.state == other.state

    def __ne__(self, other):
        return not self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return str(self.state)
