# Grid Class - Amanda Bishop

# Import statements
import pygame
pygame.init()

# Initializing constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Grid(object):
    
    # Initializes Grid class
    def __init__(self,rect,columns,rows,space=0,colour=BLACK):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.columns = columns
        self.rows = rows
        self.colour = colour
        self.space = space
        self.cellWidth = (self.w / self.rows) - self.space
        self.cellHeight = (self.h / self.columns) - self.space
        self.cells = self.makeGrid()

    # Builds the grid's coordinates
    def makeGrid(self):
        grid = []
        x = self.x + self.space
        y = self.y + self.space
        for row in range(self.rows):
            for column in range(self.columns):
                grid.append((x,y,self.cellWidth,self.cellHeight))
                x += self.cellWidth + self.space
            x = self.x + self.space
            y += self.cellHeight + self.space
        return grid

    # Draws the grid
    def draw(self,win,currentCells):
        for i,cell in enumerate(self.cells):
            if i not in currentCells:
                pygame.draw.rect(win,self.colour,cell,1)
            else:
                pygame.draw.rect(win,RED,cell,1)
        pygame.draw.rect(win,BLACK,(self.x,self.y,self.w+self.space,self.h+self.space),1)

    # Returns which cells has been clicked on
    def getCellIndex(self,mp):
        for i,cell in enumerate(self.cells):
            if pygame.Rect(cell).collidepoint(mp):
                return i
        return -1

    # Returns the existing adjacent cells    
    def getAdjacentCells(self,i):
        currentRect = self.cells[i]
        cells = []
        if currentRect[0] != (self.x + self.space):
            cells.append(i-1)
        else:
            cells.append(-1)
        if currentRect[0] != (self.w - self.cellWidth + 500):
            cells.append(i+1)
        else:
            cells.append(-1)
        if currentRect[1] != (self.y + self.space):
            cells.append(i-self.columns)
        else:
            cells.append(-1)
        if currentRect[1] != (self.h - self.cellHeight+ 100):
            cells.append(i+self.columns)
        else:
            cells.append(-1)
        if i-1 in cells and i-self.columns in cells:
            cells.append(i-self.columns-1)
        else:
            cells.append(-1)
        if i+1 in cells and i+self.columns in cells:
            cells.append(i+self.columns+1)
        else:
            cells.append(-1)
        if i+1 in cells and i-self.columns in cells:
            cells.append(i-self.columns+1)
        else:
            cells.append(-1)
        if i-1 in cells and i+self.columns in cells:
            cells.append(i+self.columns-1)
        else:
            cells.append(-1)
        return cells
