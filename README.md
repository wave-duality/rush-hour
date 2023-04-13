# didactic-umbrella

## Introduction
This is a project to implement the game "Rush Hour" in Python, where the player tries to resolve a traffic jam by moving cars on a grid, with the objective of getting a specific car to the exit. 

The code currently uses a naive BFS search, treating each board state as a node in a graph, to find a solution. Although this algorithm guarantees that the shortest possible solution is found, the computational demand is rather high and thus the computer can not quickly solve harder or larger puzzles. On the "expert" levels provided by the manufacturer, the program currently experiences runtimes from 1s to 4s.

Then, we tried using an A* algorithm, with a heuristic measured by the number of cars in between the target car and the exit, which is then added onto the current amount of moves in a given state to rank board states into a priority queue. Further improvements that could be made include increasing the recursion depth of the heuristic, or finding a more effective heuristic overall.

## Test Case Format
In the real-life game, puzzles are given as a diagram of initial cars on a grid. To translate this, our code takes in a test case of the following format. The first two lines contain positive integers $N$ and $K,$ detailing the size of the grid (we'll just work with square grids) and the number of cars, respectively. Then, the next $3K$ lines contain information about the cars -- for each car, the first line contains two integers, representing the x and y location of its upperleft-most square. Coordinates are indexed from 1 and increase downwards and to the right. The second line for each car contains an integer $L,$ the length of the car, and finally the third line for each car contains an integer detailing its orientation, 1 for a horizontal car (left-right movement) and 2 for a vertical car (up-down movement).

## Data and Analysis
The game only provided 40 cards, and I didn't think it would be very effective to manually input the data, so I wrote my own code to generate test cases. Due to the nature of input parameters, most of these testcases had 9 to 10 move solutions, yet shared the property that many possible states existed (increasing the nodes that the BFS algorithm had to traverse). Thus, these 250 test cases (under the folder puzzles (1)) exemplify the differences in the naive BFS search and the blocking A* heuristic search in the most "extreme" of puzzles.

Note that the A* algorithm optimizes for speed, coming at the tradeoff that it usually won't find the shortest (optimal) solution. Although if you formulate the heuristic valuation correctly, it shouldn't be too far from the actual shortest solution.

Of course, the blocking heuristic can be taken a step further. We then played with the Two-Blocking-Heuristic, where the heuristic is the number of cars that are blocking the cars that are blocking the target car, in addition to the blocking cars themselves, without repeat. Then this can be further recursed to get the Three-Blocking-Heuristic, etc.

Over all 250 test cases:


|    | Avg Nodes Visited ($\mu$) | Avg Length of Solution ($\mu$) |
|--- | --- | --- |
|Zero-Heuristic (Naive BFS) | 2294.8 | 9.952 |
|One-Blocking-Heuristic | 1148.2 | 9.96 |
|Two-Blocking-Heuristic | 477.7 | 10.14 |
|Three-Blocking-Heuristic | 465.9 | 10.13 |

The difference in the heuristics (and the choice to use a heuristic) is much more massive in these 250 generated test cases than the 40 in-game ones, due to the nature of BFS. The in-game puzzles are mostly rigid; at any given state, there are very few cars that can be moved, meaning that the BFS priority_queue expands at a slow rate. On the other hand, in these 250 generated puzzles, there are often many cars that can be moved in a given state, meaning that the BFS node list is massive, even if the solution itself is short. Hence, A*'s advantage over naive BFS really starts to show in cases where the number of visited nodes is very high (assuming one can find an appropriate heuristic).

Although the improvement from 0 -> 1 and 1 -> 2 is very high, after increasing the heuristic recursion depth to 3 we find rarely any noticeable change; this is due to the limited effects that further depths have on such a small grid/search space. One of the key takeaways from this project is that however simple a premise may seem, the inner numbers and interactions may be incredibly complex, and hence, there is no general "ruleset" for coming up with heuristics or clever BFS shortcuts, and considerable time must be spent on free exploration to come up with a good solution.

## TO-DO (Future?)
- Reduce runtime of current algorithm through improvements in code and implementation
- Employ and explore heuristics (A*) to increase efficiency in a more global manner
- Write code to generate difficult test-cases that can evaluate effect of various heuristics
  - Current generator code has multiple major bugs and usually produces trivial puzzles
- Implement graphics
