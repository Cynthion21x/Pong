import os
import time
import random
import sys

# Representation of cells
class cell:

    #Container of data
    def __init__(self, ty, x, y):

        self.ty = ty
        self.x = x
        self.y = y

        if ty == "paddle":
            
            self.symbol = "|"

        elif ty == "ball":

            self.symbol = "O"

        elif ty == "none":

            self.symbol = " "

    def getSymbol(self):

        return " " + self.symbol + " "
            
    def __str__(self):

        return f" {self.symbol} "

# Representation of board
class board:

    #Make empty board
    def __init__(self, width, height):

        self.main = []

        for i in range(0, height):

            self.main.append([])

            for j in range(0, width-1):

                self.main[i].append(cell("none", i, j))

    #Main cell fuctions
    def setCell(self, ty, x, y):

        self.main[y][x] = cell(ty, x, y)
        
    def readPos(self, x, y):

        return self.main[x][y]

    def checkPos(self, x, y):

        return self.main[y][x]

    #def moveCell():      

# Main functions, Game state
class core:

    def __init__(self, width, height):
        
        self.height = height
        self.width = width

        self.active = True
        self.keyDown = None

        self.b = board(width, height)

        self.ballX = (width) // 2 -1
        self.ballY = (height) // 2 -1

        self.paddle1Y = (height) // 2 -1
        self.paddle2Y = (height) // 2 -1

        self.paddle1vel = 0
        self.paddle2vel = 0

        self.xvel = 1
        self.yvel = self.yvel = random.randint(-2,2)

        self.Lscore = 0
        self.Rscore = 0

        self.nVel = 0
        self.reset = -1

        #print(self.b.readPos(1, 1))

    #State
    def Active(self):

        return self.active

    #logic
    def Update(self):
            
        # --- Bounce ---

        if self.reset == 0:
            
            self.xvel = self.nVel
            self.reset = -1

        if self.reset >= 0:

            self.reset -= 1
            

        #left
        if self.ballX >= self.width - 2:
            
            if self.b.checkPos(self.ballX, self.ballY).ty == "paddle":

                self.xvel = -1
                self.yvel = random.randint(-2,2)

            else:
                
                self.b.setCell("none", self.ballX , self.ballY)
                self.ballX = (self.width) // 2 -1
                self.ballY = (self.height) // 2 -1
                
                self.reset = 5
                
                self.xvel = 0
                self.yvel = 0
                self.nVel = -1
                
                self.Lscore += 1
                
        #right
        if self.ballX <= 0:

            if self.b.checkPos(self.ballX, self.ballY).ty == "paddle":

                self.xvel = 1
                self.yvel = random.randint(-2,2)

            else:
                     
                self.b.setCell("none", self.ballX , self.ballY)
                self.ballX = (self.width) // 2 -1
                self.ballY = (self.height) // 2 -1

                self.reset = 5
                           
                self.nVel = 1
                self.xvel = 0
                self.yvel = 0
                
                self.Rscore += 1

        #top
        if self.ballY >= self.height - 2:
            self.yvel = -1

        #bottom
        if self.ballY <= 0:
            self.yvel = 1

        # --- Paddles ---

        #Player

        if self.keyDown is not None:

        # Handle the key input
            if self.keyDown == 'w':
                self.paddle2vel = -1
                pass

            elif self.keyDown == 's':
                self.paddle2vel = 1
                pass

            elif self.keyDown == 'p':
                self.active = False;
                pass

        else:

            self.paddle2vel = 0

        '''
        #Left
        if self.ballX < self.width // 2:

            if self.paddle2Y > self.ballY:

                self.paddle2vel = -1

            elif self.paddle2Y < self.ballY:

                self.paddle2vel = 1

            else:

                self.paddle2vel = 0

        else:

            self.paddle2vel = 0
        '''

        #Right
        if self.ballX > self.width // 2 - 2:

            if self.paddle1Y > self.ballY:

                self.paddle1vel = -1

            elif self.paddle1Y < self.ballY:

                self.paddle1vel = 1

            else:

                self.paddle1vel = 0

        else:

            self.paddle1vel = 0        

        #calculate new position
        self.b.setCell("none", self.ballX , self.ballY)
        self.b.setCell("none", self.width - 2, self.paddle1Y)
        self.b.setCell("none", 0, self.paddle2Y)

        self.b.setCell("none", self.width - 2, self.paddle1Y+1)
        self.b.setCell("none", 0, self.paddle2Y+1)

        self.b.setCell("none", self.width - 2, self.paddle1Y-1)
        self.b.setCell("none", 0, self.paddle2Y-1)

        self.ballX += self.xvel
        self.ballY += self.yvel

        self.paddle2Y += self.paddle2vel

        if self.paddle2Y >= self.height-3:

            self.paddle2Y = self.height-3

        if self.paddle2Y <= 2:
        
            self.paddle2Y = 2

        self.paddle1Y += self.paddle1vel

        #update cells
        self.b.setCell("ball", self.ballX , self.ballY)
        
        self.b.setCell("paddle", self.width - 2, self.paddle1Y)
        self.b.setCell("paddle", 0, self.paddle2Y)

        self.b.setCell("paddle", self.width - 2, self.paddle1Y+1)
        self.b.setCell("paddle", 0, self.paddle2Y+1)

        self.b.setCell("paddle", self.width - 2, self.paddle1Y-1)
        self.b.setCell("paddle", 0, self.paddle2Y-1)

        #store previous position
        self.paddleY = self.ballY

    #Display
    def Render(self):

        print("==========================  Pong  =========================")

        print("")

        print("+----------- Player Score: " + str(self.Lscore) + "  Robot Score: " + str(self.Rscore) + " -------------+")

        for i in range(0, self.height-1):
            row = "|"
            for j in range(0, self.width-1):
                row += self.b.readPos(i, j).getSymbol()
            print(row + "|")

        print("+---------------------------------------------------------+")

        print("")

        print("press w and s to move and use p to exit")

        time.sleep(0.1)
        os.system('cls')

    #Get input
    def Event(self):

        if os.name == 'nt':  # Windows
        
            import msvcrt

            if msvcrt.kbhit():
                self.keyDown = msvcrt.getch().decode()
            else:
                self.keyDown = None

        else:  # Unix-like systems (Linux, macOS)
            
            import tty
            import termios
            
            stdin_fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(stdin_fd)

            try:
                tty.setraw(stdin_fd)
                if sys.stdin.read(1):
                    self.keyDown = sys.stdin.read(1)
                else:
                    self.keyDown = None
            
            finally:
                termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_settings)

    #Close
    def Exit(self):
        
        del self
