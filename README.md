# didactic-umbrella

## Introduction
This is an ongoing project to implement the game "Rush Hour" in Python, where the player tries to resolve a traffic jam by moving cars on a grid, with the objective of getting a specific car to the exit. 

The code currently uses a naive BFS search, treating each board state as a node in a graph, to find a solution. Although this algorithm guarantees that the shortest possible solution is found, the computational demand is rather high and thus the computer can not quickly solve harder or larger puzzles. On the "expert" levels provided by the manufacturer, the program currently experiences runtimes from 1s to 4s.

## Test Case Format
In the real-life game, puzzles are given as a diagram of initial cars on a grid. To translate this, our code takes in a test case of the following format. The first two lines contain positive integers $N$ and $K,$ detailing the size of the grid (we'll just work with square grids) and the number of cars, respectively. Then, the next $3K$ lines contain information about the cars -- for each car, the first line contains two integers, representing the x and y location of its upperleft-most square. Coordinates are indexed from 1 and increase downwards and to the right. The second line for each car contains an integer $L,$ the length of the car, and finally the third line for each car contains an integer detailing its orientation, 1 for a horizontal car (left-right movement) and 2 for a vertical car (up-down movement).

## TO-DO
- Reduce runtime of current algorithm through improvements in code and implementation
- Employ and explore heuristics (A*) to increase efficiency in a more global manner
- Write code to generate difficult test-cases that can evaluate effect of various heuristics
  - Current generator code has multiple major bugs and usually produces trivial puzzles
- Implement graphics
