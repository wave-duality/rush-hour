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

    def __eqcar__(self, other):
        if self.x == other.x and self.y == other.y and self.length == other.length and self.orient == other.orient:
            return True
        return False


class State:
    def __init__(self, cars, freespaces, currmoves):
        self.cars = cars
        self.freespaces = freespaces
        self.currmoves = currmoves

    def __eqstate__(self, other):
        for i in range(0, len(self.cars)):
            if not self.cars[i].__eqcar__(other.cars[i]):
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
    cars = currstate.cars
   
    freespaces = currstate.freespaces
    #valid moves, given a car configuration
    moves = []
    for i in range(0, len(cars)):
        index = 1
        if cars[i].orient == 1:
            while (cars[i].x+cars[i].length-1+index <= n and [cars[i].x+cars[i].length-1+index, cars[i].y] in freespaces):
                moves.append([i+1, index])
                index += 1
            index = -1
            while (cars[i].x+index >= 1 and [cars[i].x+index, cars[i].y] in freespaces):
                moves.append([i+1, index])
                index -= 1
        else:
            while (cars[i].y+cars[i].length-1+index <= n and [cars[i].x, cars[i].y+cars[i].length-1+index] in freespaces):
                moves.append([i+1, index])
                index += 1
            index = -1
            while (cars[i].y+index >= 1 and [cars[i].x, cars[i].y+index] in freespaces):
                moves.append([i+1, index])
                index -= 1
    return moves


def applymove(move, oldstate):
    #change cars component
    State = copy.copy(oldstate)
    
    car = State.cars[move[0]-1]

    newcars = copy.copy(State.cars)
    index = newcars.index(car)
    newcars.remove(car)
    if car.orient == 1:
        newcar = Car(car.x+move[1], car.y, car.length, car.orient)
    else:
        newcar = Car(car.x, car.y+move[1], car.length, car.orient)
    newcars.insert(index, newcar)
    State.cars = copy.copy(newcars)
    #change freespaces component
    freespaces = copy.copy(State.freespaces)
 
    if car.orient == 1:
        if move[1] > 0:
            for i in range(1, move[1]+1):
                freespaces.append([car.x+i-1, car.y])
                freespaces.remove([car.x+i+car.length-1, car.y])
        else:
            for i in range(-1, move[1]-1, -1):
                freespaces.append([car.x+i+car.length, car.y])
                freespaces.remove([car.x+i, car.y])
    else:
        if move[1] > 0:
            for i in range(1, move[1]+1):
                freespaces.append([car.x, car.y+i-1])
                freespaces.remove([car.x, car.y+i+car.length-1])
        else:
            for i in range(-1, move[1]-1, -1):
                freespaces.append([car.x, car.y+i+car.length])
                freespaces.remove([car.x, car.y+i])
    State.freespaces = freespaces
    #change moves component
    moves = copy.copy(State.currmoves)
    moves.append(move)
    State.currmoves = moves
    
    return State


def check(state, visited):
    for i in visited:
        if i.__eqstate__(state):
            return True
    return False


target = [5, 3] #once our model left-right length 2 red car arrives here, the game is won
n, cars = takeInput()

'''
n = 6
Car1 = Car(1, 3, 2, 1)
Car2 = Car(1, 4, 3, 1)
Car3 = Car(3, 1, 3, 2)
Car4 = Car(5, 1, 2, 1)
Car5 = Car(6, 4, 3, 2)
cars = [Car1, Car2, Car3, Car4, Car5]
'''

freespaces = [[i,j] for i in range(1, n+1) for j in range(1, n+1)]
#initialize this list
for i in cars:
    for j in i.occupy():
        if j in freespaces:
            freespaces.remove(j)


initial = State(cars, freespaces, [])

visited = [] #stores instances of "State"

currstack = [initial]
foundsol = False

while (foundsol == False):
 
    #for curr in currstack:
        #print(curr.cars[0].x, curr.cars[0].y)
    curr = currstack[-1]
    currstack.pop()
    visited.append(curr)
    if curr.cars[0].x == target[0] and curr.cars[0].y == target[1]:
        print("Found a Solution! (" + str(len(curr.currmoves)) + " moves)")
        for i in curr.currmoves: print(i)
        foundsol = True
    moves = validmoves(curr)
    for i in moves:
        new = applymove(i, curr)
        if not check(new, visited):
            currstack.append(new)
    #print("-------")
    







          
