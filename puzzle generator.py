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

def numofcars(size, difficulty):
    if difficulty == 1: #easy
        return random.randint(floor(size**2/6), floor(size**2/4)), random.randint(floor(size**2/20), floor(size**2/12))
    if difficulty == 2: #medium
        return random.randint(floor(size**2/5), floor(size**2/3.75)), random.randint(floor(size**2/16), floor(size**2/11))
    if difficulty == 3: #hard
        return random.randint(floor(size**2/4), floor(size**2/3.5)), random.randint(floor(size**2/12), floor(size**2/10))

def available(length, orientation, board):
    #returns an array of available locations
    possible = []
    if orientation == 1:
        #check left-right
        for i in range(0, len(board)):
            if i != floor((len(board)+1)/2)-1: #can NOT be in the same row as the target car!
                for j in range(0, len(board)-length+1):
                    valid = True
                    for k in range(j, j+length):
                        if board[i][k] != 0:
                            valid = False
                    if valid == True:
                        possible.append([j+1, i+1])
    else:
        #check up-down
        for i in range(0, len(board)): #column
            for j in range(0, len(board)-length+1):
                valid = True
                for k in range(j, j+length):
                    if board[k][i] != 0:
                        valid = False
                if valid == True:
                    possible.append([i+1, j+1])
    return possible

def validmoves(currstate):
    board = currstate.board
    cars = currstate.cars
    #valid moves, given a car configuration
    moves = []
    for i in range(0, len(cars)):
        index = 1
        if cars[i].orient == 1:
            while (cars[i].x+cars[i].length-1+index <= len(board) and board[cars[i].y-1][cars[i].x+cars[i].length-1+index-1] == 0):
                moves.append([i+1, index])
                index += 1
            index = -1
            while (cars[i].x+index >= 1 and board[cars[i].y-1][cars[i].x+index-1] == 0):
                moves.append([i+1, index])
                index -= 1
        else:
            while (cars[i].y+cars[i].length-1+index <= len(board) and board[cars[i].y+cars[i].length-1+index-1][cars[i].x-1] == 0):
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
    
def generate(size, difficulty, quantity):
    #generates rush hour puzzles of a particular grid size, difficulty, and quantity
    acquired = 0
    while acquired != quantity:
        res = "" + str(size) + "\n"
        twocars, threecars = numofcars(size, difficulty)
        res = res + str(twocars+threecars) + "\n"
        successful = False
        while not successful:
            successful = True
            cars = []
            board = []
            for i in range(size):
                l = []
                for j in range(size):
                    l.append(0)
                board.append(l)
            #place three-length cars first since more restrictive
            redcar = Car(size-1, floor((size+1)/2), 2, 1)
            board[floor((size+1)/2)-1][size-2] = 1
            board[floor((size+1)/2)-1][size-1] = 1
            cars.append(redcar)
            for k in range(threecars):
                orient = random.randint(1,2)
                location = available(3, orient, board)
                if len(location) == 0:
                    successful = False
                else:
                    chosen = random.choice(location)
                    curr = Car(chosen[0], chosen[1], 3, orient)
                    for l in curr.occupy():
                        board[l[1]-1][l[0]-1] = k+2
                    cars.append(curr)
            for p in range(twocars-1): #already put the red car down
                orient = random.randint(1,2)
                location = available(2, orient, board)
                if len(location) == 0:
                    successful = False
                else:
                    chosen = random.choice(location)
                    curr = Car(chosen[0], chosen[1], 2, orient)
                    for l in curr.occupy():
                        board[l[1]-1][l[0]-1] = j+threecars+2
                    cars.append(curr)
                    
        state = State(board, cars, [])
        puzzle = scramble(state, 30)
        if len(puzzle.cars) > 0:
            acquired += 1
            printboard(puzzle)
    
def scramble(State, depth):
    scrambled = False
    while not scrambled:
        for i in range(depth):
            choices = validmoves(State)
            if len(choices) == 0:
                return State([], [], [])
            if [1, -1] in choices:
                State = applymove([1,-1], State)
            else:
                j = random.choice(choices)
                State = applymove(j, State)
        if State.cars[0].x <= floor(len(State.board)/2)-1:
            scrambled = True
    return State
        
            
        
        
        





