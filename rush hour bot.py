import copy
#coordinates start at 1 at the top, 1 at the left
class Car:
    def __init__(self, x, y, length, orient):
        self.x = x
        self.y = y
        self.length = length
        self.orient = orient #1 = left/right, 2 = top/bottom

    def occupy(self):
        spaces = []
        if self.orient == 1:
            for i in range(self.length):
                spaces.append([self.x+i, self.y])
        else:
            for i in range(self.length):
                spaces.append([self.x, self.y+i])
        return spaces

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.length == other.length and self.orient == other.orient:
            return True
        return False


class State:
    MAX_CAR = 10

    def __init__(self, n, board, cars, currmoves):
        self.board_size = n
        self.board = board
        self.cars = cars
        self.currmoves = currmoves   

    def hash_value(self):
        val = 0
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if i > 0 or j > 0:
                    val *= self.MAX_CAR
                val += self.board[i][j]
        return val

    def __eq__(self, other):
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True


def toggle(n):
    if n == 1:
        return "left-right."
    else:
        return "top-bottom."


def takeInput():
    print("What would you like the grid size to be?")
    n = int(input())
    print("How many cars would you like?")
    c = int(input())
    cars = []
    print("We'll represent the grid with coordinates, with the x-position increasing from left to right and the y-position increasing from top to bottom. All coordinates begin at 1.")
    print("\n")
    for i in range(c):
        print("Enter the x and y coordinate of the top-left square of car #" + str(i+1) + " with a single space in between the two numbers.")
        coords = input().split(" ")
        xcoord = int(coords[0])
        ycoord = int(coords[1])
        print("How long is the car?")
        length = int(input())
        print("Finally, is the car's body spanning left-right or top-bottom? Enter 1 for left/right and 2 for top/bottom.")
        direction = int(input())
        car = Car(xcoord, ycoord, length, direction)
        cars.append(car)
    print("You initialized a puzzle with the following cars: ")

    for j in range(len(cars)):
        c = cars[j]
        print("Car #" + str(j+1) + ": " + "top left corner at [" + str(c.x) + ", " + str(c.y) + "] with length " + str(c.length) + " and spanning " + toggle(c.orient))
    print("We will now begin finding a solution.")

    return n, cars


def validmoves(currstate):
    board = currstate.board
    cars = currstate.cars
    #valid moves, given a car configuration
    moves = []
    for i in range(0, len(cars)):
        index = 1
        if cars[i].orient == 1:
            while (cars[i].x+cars[i].length-1+index <= n and board[cars[i].y-1][cars[i].x+cars[i].length-1+index-1] == 0):
                moves.append([i+1, index])
                index += 1
            index = -1
            while (cars[i].x+index >= 1 and board[cars[i].y-1][cars[i].x+index-1] == 0):
                moves.append([i+1, index])
                index -= 1
        else:
            while (cars[i].y+cars[i].length-1+index <= n and board[cars[i].y+cars[i].length-1+index-1][cars[i].x-1] == 0):
                moves.append([i+1, index])
                index += 1
            index = -1
            while (cars[i].y+index >= 1 and board[cars[i].y+index-1][cars[i].x-1] == 0):
                moves.append([i+1, index])
                index -= 1
    return moves


def applymove(move, oldstate):

    State = copy.deepcopy(oldstate)
    car = State.cars[move[0]-1]
    
    newboard = copy.deepcopy(State.board)
    if car.orient == 1:
        for i in range(0, car.length):
            newboard[car.y-1][car.x+i-1] = 0
            #print(car.y-1, car.x+i-1)
        for i in range(0, car.length):
            newboard[car.y-1][car.x+i+move[1]-1] = move[0]
            #print(car.y-1, car.x+i+move[1]-1)
    else:
        for i in range(0, car.length):
            newboard[car.y+i-1][car.x-1] = 0
        for i in range(0, car.length):
            newboard[car.y+i+move[1]-1][car.x-1] = move[0]
    State.board = newboard

    newcars = copy.deepcopy(State.cars)
    index = newcars.index(car)
    newcars.remove(car)
    if car.orient == 1:
        newcar = Car(car.x+move[1], car.y, car.length, car.orient)
    else:
        newcar = Car(car.x, car.y+move[1], car.length, car.orient)
    newcars.insert(index, newcar)
    State.cars = newcars
    #change moves component
    moves = copy.copy(State.currmoves)
    moves.append(move)
    State.currmoves = moves
    
    return State


def check(state, visited):
    return state.hash_value() in visited

visited = set() #stores instances of "State"

def dfs(state):
    #if too long, terminate
    #explore neighbors, mark as visited
    #if return, mark as unvisited
    if state.cars[0].x == target[0] and state.cars[0].y == target[1]:
        print("Found a Solution! (" + str(len(state.currmoves)) + " moves)")
        for i in state.currmoves: print(i)
    else:
        v = state.hash_value()
        visited.add(v)
        moves = validmoves(state)
        for i in moves:
            new = applymove(i, state)
            if not check(new, visited) and len(new.currmoves) < 10:
                dfs(new)
        visited.remove(v)
        

target = [5, 3] #once our model left-right length 2 red car arrives here, the game is won
n, startcars = takeInput()

startboard = []
for i in range(n):
    l = []
    for j in range(n):
        l.append(0)
    startboard.append(l)

for i in range(1, len(startcars)+1):
    for k in startcars[i-1].occupy():
        startboard[k[1]-1][k[0]-1] = i


initial = State(n, startboard, startcars, [])


dfs(initial)



    







          
