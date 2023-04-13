import copy
from queue import PriorityQueue
import time
import random
from math import *
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
    def __init__(self, board, cars, currmoves):
        self.board = board
        self.cars = cars
        self.currmoves = currmoves

    def __eq__(self, other):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

    def __lt__(self, other):
        return random.randint(0, 2)


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
    moves = copy.deepcopy(State.currmoves)
    moves.append(move)
    State.currmoves = moves
    
    return State


def check(state, visited):
    for i in visited:
        if i == state:
            return True
    return False

def hashvalue(state):
    #hashes each board state into a number
    res = 0
    base = len(state.cars)+1
    power = 0
    for i in range(0, len(state.board)):
        for j in range(0, len(state.board)):
            res += (base**power)*state.board[i][j]
            power += 1
    return res

def blocking(state, carlist):
    global n
    board = state.board
    #return the number of cars currently in the way from the red car to the exit
    blocks = {0}
    cars = state.cars
    for i in carlist:
        if i.orient == 1:
            for x in range(i.x+i.length-1, n):
                if board[i.y-1][x] not in blocks:
                    blocks.add(board[i.y-1][x])
        else:
            for x in range(i.y+i.length-1, n):
                if board[x][i.x-1] not in blocks:
                    blocks.add(board[x][i.x-1])
    return (len(blocks)-1, blocks)

def heuristic(state, mode):
    #A* considers the number of moves from the start and the expected # of moves to finish
    if mode == 1: return (len(state.currmoves))
    if mode == 2: return (len(state.currmoves)+blocking(state, [state.cars[0]])[0])
    if mode == 3:
        adj = blocking(state, [state.cars[0]])[1]
        carlist = []
        for j in adj:
            if j != 0:
                carlist.append(state.cars[j-1])
        new = blocking(state, carlist)[1]
        total = []
        for i in adj:
            if i not in total:
                total.append(i)
        for i in new:
            if i not in total:
                total.append(i)
        return (len(state.currmoves) + len(total)-1)
    if mode == 4:
        adj = blocking(state, [state.cars[0]])[1]
        carlist = []
        for j in adj:
            if j != 0:
                carlist.append(state.cars[j-1])
        new = blocking(state, carlist)[1]
        carlist = []
        for j in new:
            if j != 0:
                carlist.append(state.cars[j-1])
        new2 = blocking(state, carlist)[1]
        total = []
        for i in adj:
            if i not in total:
                total.append(i)
        for i in new:
            if i not in total:
                total.append(i)
        for i in new2:
            if i not in total:
                total.append(i)
        return (len(state.currmoves) + len(total)-1)
def printboard(state):
    dimension = len(state.board)
    res = "- "
    for j in range(3*dimension):
        res = res + "- "
    res = res + "\n"
    for i in range(len(state.board)):
        line1 = "|     "
        for j in range(dimension):
            line1 = line1+ "|     "
        line1 = line1 + "\n"
        res = res + line1
        line2 = "|"
        for j in range(dimension):
            if state.board[i][j] == 0:
                line2 = line2 + "  " + str(" ") + "  |"
            else:
                line2 = line2 + "  " + str(chr(state.board[i][j]+64)) + "  |"
        line2 = line2 + "\n"
        res = res + line2
        line3 = "|"
        for j in range(dimension):
            line3 = line3 + "_ _ _|"
        line3 = line3 + "\n"
        res = res + line3
    print(res)

def directions(state, move):
    car = state.cars[move[0]-1]
    if car.orient == 1:
        if move[1] > 0:
            return " " + str(move[1]) + " squares to the right."
        else:
            return " " + str((-1)*move[1]) + " squares to the left."
    else:
        if move[1] > 0:
            return " " + str(move[1]) + " squares downward."
        else:
            return " " + str((-1)*move[1]) + " squares upward."
    
def printsol(state):
    #start from the beginning, print the board one step at a time
    global initial
    print("Initial Board:")
    printboard(initial)
    step = 1
    for i in state.currmoves:
        initial = applymove(i, initial)
        print("Step #" + str(step) + ": " + "Move car \"" + chr(i[0]+64) + "\"" + directions(state, i))
        printboard(initial)
        step += 1
        
visited = set() #stores instances of "State"
pq = PriorityQueue()
solved = False
st = time.time()

def bfs():
    global solved, pq, visited
    index = 0
    while not solved:
        curr = pq.get()[1]
        if curr.cars[0].x == target[0] and curr.cars[0].y == target[1]:
            return (index+1, len(curr.currmoves))
        for i in validmoves(curr):
            new = applymove(i, curr)
            if hashvalue(new) not in visited:
                visited.add(hashvalue(new))
                pq.put((heuristic(new, 4), new))
        index += 1
        
            
target = [5, 3] #once our model left-right length 2 red car arrives here, the game is won
n = 6

#once our model left-right length 2 red car arrives here, the game is won
def interpret(puzzle):
    global visited, pq
    visited.clear(), pq.queue.clear()
    data = puzzle.split("\n")[:-1]
    n = int(data[0])
    numcars = int(data[1])
    startcars = []
    index = 2
    for j in range(numcars):
        x, y = int(data[index].split(" ")[0]), int(data[index].split(" ")[1])
        index += 1
        length = int(data[index])
        index += 1
        orient = int(data[index])
        index += 1
        startcars.append(Car(x, y, length, orient))
            
    startboard = []
    for i in range(n):
        l = []
        for j in range(n):
            l.append(0)
        startboard.append(l)

    for i in range(1, len(startcars)+1):
        for k in startcars[i-1].occupy():
            startboard[k[1]-1][k[0]-1] = i

    initial = State(startboard, startcars, [])
    pq.put((0, initial))


a = ""
b = ""
w = open("/Users/owenzhang/Documents/testdata4.txt", "w")
for i in range(1, 251):
    f = open("/Users/owenzhang/Documents/puzzles/p" + str(i) + ".txt", "r")
    interpret(f.read())
    c, d = bfs()
    a = a+str(c) + " "
    b = b+str(d) + " "
    print(i)
w.write(a)
w.write("\n")
w.write(b)
w.write("\n")
w.close()




    







          
