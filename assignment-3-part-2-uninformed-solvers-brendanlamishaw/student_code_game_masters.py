from game_master import GameMaster
from read import *
from util import *
import pdb

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        PEG1 = self.kb.kb_ask(parse_input('fact: (on ?disk peg1)'))
        PEG2 = self.kb.kb_ask(parse_input('fact: (on ?disk peg2)'))
        PEG3 = self.kb.kb_ask(parse_input('fact: (on ?disk peg3)'))

        peg1 = []
        if PEG1:
            for x in PEG1:
                disk = int(str(x.bindings[0].constant)[-1])
                peg1.append(disk)
            peg1.sort()
            peg1 = tuple(peg1)
        else:
            peg1 = tuple()

        peg2 = []
        if PEG2:
            for x in PEG2:
                disk = int(str(x.bindings[0].constant)[-1])
                peg2.append(disk)
            peg2.sort()
            peg2 = tuple(peg2)
        else:
            peg2 = tuple()

        peg3 = []
        if PEG3:
            for x in PEG3:
                disk = int(str(x.bindings[0].constant)[-1])
                peg3.append(disk)
            peg3.sort()
            peg3 = tuple(peg3)
        else:
            peg3 = tuple()

        game = (peg1, peg2, peg3)

        return game
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        disk = movable_statement.terms[0]
        fPeg = movable_statement.terms[1]
        tPeg = movable_statement.terms[2]

        if self.isMovableLegal(movable_statement):
            # Update From-Peg
            query = self.kb.kb_ask(parse_input(f'fact: (onTopOf {str(disk)} ?d'))

            self.kb.kb_retract(parse_input(f'fact: (top {str(disk)} {str(fPeg)})'))
            self.kb.kb_retract(parse_input(f'fact: (on {str(disk)} {str(fPeg)})'))

            if query:
                underDisk = query[0].bindings[0].constant
                self.kb.kb_assert(parse_input(f'fact: (top {str(underDisk)} {str(fPeg)}'))
            else:
                self.kb.kb_assert(parse_input(f'fact: (empty {str(fPeg)})'))


            # Update To-Peg
            self.kb.kb_retract(parse_input(f'fact: (empty {str(tPeg)})'))
            top = self.kb.kb_ask(parse_input(f'fact: (top ?d {str(tPeg)})'))
            if top:
                topDisk = top[0].bindings[0].constant
                self.kb.kb_retract(parse_input(f'fact: (top {str(topDisk)} {str(tPeg)})'))

            self.kb.kb_assert(parse_input(f'fact: (on {str(disk)} {str(tPeg)})'))
            self.kb.kb_assert(parse_input(f'fact: (top {str(disk)} {str(tPeg)})'))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        ROW1 = self.kb.kb_ask(parse_input('fact: (row1 ?t)'))
        ROW2 = self.kb.kb_ask(parse_input('fact: (row2 ?t)'))
        ROW3 = self.kb.kb_ask(parse_input('fact: (row3 ?t)'))

        row1 = ['x', 'x', 'x']
        for x in ROW1:
            findXPosn = self.kb.kb_ask(parse_input(f'fact: (inst {str(x.bindings[0].constant)} ?posx ?posy)'))
            posn = int(str(findXPosn[0].bindings[0].constant)[-1])
            tile = x.bindings[0].constant
            if str(tile) == 'empty':
                tileNum = -1
            else:
                tileNum = int(str(tile)[-1])
            row1[posn-1] = tileNum
        row1 = [x for x in row1 if x != 'x']
        row1 = tuple(row1)

        row2 = ['x', 'x', 'x']
        for x in ROW2:
            findXPosn = self.kb.kb_ask(parse_input(f'fact: (inst {str(x.bindings[0].constant)} ?posx ?posy)'))
            posn = int(str(findXPosn[0].bindings[0].constant)[-1])
            tile = x.bindings[0].constant
            if str(tile) == 'empty':
                tileNum = -1
            else:
                tileNum = int(str(tile)[-1])
            row2[posn-1] = tileNum
        row2 = [x for x in row2 if x != 'x']
        row2 = tuple(row2)

        row3 = ['x', 'x', 'x']
        for x in ROW3:
            findXPosn = self.kb.kb_ask(parse_input(f'fact: (inst {str(x.bindings[0].constant)} ?posx ?posy)'))
            posn = int(str(findXPosn[0].bindings[0].constant)[-1])
            tile = x.bindings[0].constant
            if str(tile) == 'empty':
                tileNum = -1
            else:
                tileNum = int(str(tile)[-1])
            row3[posn-1] = tileNum
        row3 = [x for x in row3 if x != 'x']
        row3 = tuple(row3)

        game = (row1, row2, row3)



        return game

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = movable_statement.terms[0]
        fPosx = movable_statement.terms[1]
        fPosy = movable_statement.terms[2]
        tPosx = movable_statement.terms[3]
        tPosy = movable_statement.terms[4]

        if self.isMovableLegal(movable_statement):

            self.kb.kb_retract(parse_input(f'fact: (inst {str(tile)} {str(fPosx)} {str(fPosy)})'))
            self.kb.kb_retract(parse_input(f'fact: (inst empty {str(tPosx)} {str(tPosy)})'))

            self.kb.kb_assert(parse_input(f'fact: (inst {str(tile)} {str(tPosx)} {str(tPosy)})'))
            self.kb.kb_assert(parse_input(f'fact: (inst empty {str(fPosx)} {str(fPosy)})'))

            self.kb.kb_remove(parse_input(f'fact: (movable empty {str(fPosx)} {str(fPosy)} {str(fPosx)} {str(fPosy)})'))

        pass


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
