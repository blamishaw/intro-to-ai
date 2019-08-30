# Assignment 3 Part 2: Game Masters and Uninformed Solvers

In this week's assignment, you will both bring the puzzle games to life and create automated players to solve them based on uninformed search algorithms.

Indeed, there are two tasks in this part of the assignment. 

First, you will utilize the world models that you built in Part 1 to create **two functional game masters**. This part is intended to get you writing code aimed at managing and mutating the state of a given world.

Second, you will develop **two game-independent solvers** that are capable of
brute-forcing the two puzzle games. For this part, you'll be implementing a solver that uses the **Depth-First Search algorithm**, and another that uses the **Breadth-First Search algorithm**.

## Starter Code

This starter code builds on top of Assignment 3 Part 1. `kb_and_inference_engine.py` contains the definition of a
KnowledgeBase (KB) and an InferenceEngine, similar to what you have implemented for Assignment 2. `game_master.py`
contains the GameMaster prototype. You will implement two subclasses of it in `student_code_game_masters.py`.
`solver.py` contains the UninformedSolver prototype, and a generic GameState class that is capable of representing
game states of either game. You will implement two subclasses of UninformedSolver in
`student_code_uninformed_solvers.py`.

As with Part 1, the `flatfiles` directory contains flat files. In this assignment, you will see two flatfiles
have been pre-filled with facts: `hanoi_all_forbidden.txt` and `puzzle8_all_forbidden.txt`. They contain all possible
movables one could expect in a game, and they are used in conjunction with desired game states to check whether
a game has reached the winning condition. Other flatfiles need to be filled to represent the game states,
as with Part 1.

Each test in `main.py` automatically loads one of the flat files that you wrote as the initial game state, set the
winning conditions, and test whether your code has met the required specifications.

## Your Tasks

In this assignment, you need to fill the empty flatfiles in the `flatfiles` directory with your game state
representations, and complete the code stubs in `student_code_game_masters.py` and `student_code_uninformed_solvers.py`.

In this assignment, the majority of the requirements and hints are written as method descriptions in the `*.py` files
rather than in `README.md`. Please read them before you proceed.

## Important Details

The search spaces of the games, Tower of Hanoi and 8 Puzzle, are vast and could take a long time for either of the two
algorithms to traverse. In our testing, the Depth-First Search and the Breadth-First Search algorithms could take
between 10s of seconds to 15 minutes to solve a game, depending on the initial and goal states.
To expedite your development, the provided Tower of Hanoi tests included in `main.py` only use 3 disks.
The tests used for grading will also run on the 5 disk version of Tower of Hanoi.

To ensure that your solvers behave in manner expected of the corresponding search algorithms, each solver will be
tested on whether they conform to a specific pattern of exploration, rather than whether it could solve the game.
Specifically, each solver will be asked to explore a game for a fixed number of steps, and we will compare the resulting
game state with the game state expected from a correctly implemented search algorithm. The grading tests will follow
a similar format.

Note that in this assignment, we define a **step** as reaching a new game state previously unexplored by the solver,
rather than making a move in the game. Reversing three moves -- backtracking through three previously reached
states -- therefore, does not contribute toward the step counts.

To guard against infinite loops, **the tests impose hard time limits**. The time limits adopted by the tests 
`main.py` are specified in the docstring of `runPlayXSteps` method and `runSolve` method. 
During grading, test cases involving larger search space, such as Tower of Hanoi with 5 disks, will be allowed to run 
for a longer period of time. 

## Preview: Part 3

In Part 3 of this assignment, released next week, you will build a third solver that adopts and informed search: A*
search algorithm.
