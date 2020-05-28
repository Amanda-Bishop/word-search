#Word Search Game - Amanda Bishop

# Imports
import pygame
pygame.init()
import GridClass

# Initializing Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 207, 62)
YELLOW = (255, 251, 143)
BKG = (204, 231, 255)
LR = 0
UD = 1
DTOR = 2
DTOL = 3

class Menu(GridClass.Grid):

    # Initializing the sub class of Grid, Menu
    def __init__(self,puzzles,rect,columns,rows,space=0,colour=BLACK):
        self.puzzles = puzzles
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
        self.cells = GridClass.Grid.makeGrid(self)
        self.buttons = self.makeBtns()

    # Makes buttons for the menu using the Button class
    def makeBtns(self):
        btns = []
        for i,cell in enumerate(self.cells):
            newBtn = Button(cell)
            btns.append(newBtn)
        return btns

    # Draws the menu
    def draw(self,win):
        for i,btn in enumerate(self.buttons):
            btn.draw(win)
            label = Label(self.puzzles[i])
            label.draw(win,btn.rect)

class WordList(GridClass.Grid):

    # Initializes the sub class of Grid, WordList
    def __init__(self,words,rect,columns,rows,space=0,colour=BLACK):
        self.words = words
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
        self.cells = GridClass.Grid.makeGrid(self)

    # Draws the wordlist
    def draw(self,win,foundWords):
        colour = self.colour
        for i,cell in enumerate(self.cells):
            if self.words[i] in foundWords:
                colour = GREEN
            else:
                colour = self.colour
            pygame.draw.rect(win,colour,cell,1)
            label = Label(self.words[i])
            label.draw(win,cell)


class Button(object):

    # Initializes the button class
    def __init__(self,rect,outline=BLACK,fill=YELLOW,outlineLen=2):
        self.rect = rect
        self.outline = outline
        self.fill = fill
        self.outlineLen = outlineLen

    # Draws the button
    def draw(self,win):
        pygame.draw.rect(win, self.fill, self.rect, 0)
        pygame.draw.rect(win, self.outline, self.rect, self.outlineLen)

    # Returns the button if it collides with a point
    def collide(self,point):
        if pygame.Rect(self.rect).collidepoint(point):
            return self.rect
        else:
            return -1

class Label(object):

    # Initializes the Label class
    def __init__(self,txt,align="center",size=15,font="yugothicyugothicuilight",colour=BLACK):
        self.txt = txt
        self.size = size
        self.font = font
        self.colour = colour
        self.align = align

    # Draws the labels
    def draw(self,win,rect):
        font =  pygame.font.SysFont(self.font,self.size)
        txtSurface = font.render(self.txt, True, self.colour)
        if self.align == "center":
            x = rect[0] + ((rect[2] / 2) - (txtSurface.get_width() / 2))
            y = rect[1] + ((rect[3] / 2) - (txtSurface.get_height() / 2))
        elif self.align == "left":
            x = rect[0]
            y = rect[1]
        elif self.align == "right":
            x = rect[0] + (rect[2] - txtSurface.get_width())
            y = rect[1]
        win.blit(txtSurface,(x,y))

class WordSearch(object):

    # Initializes the WordSearch class
    def __init__(self,letters,cells):
        self.ltrs = letters
        self.cells = cells
        self.direction = LR
        self.currentCells = []
        self.adjacentCells = []

    # Draws the letters using the Label class
    def drawLtrs(self,win,rects):
        for i,ltr in enumerate(self.ltrs):
            label = Label(ltr)
            label.draw(win,rects[i])

    # Finds the current cells being selected
    def findCurrentCells(self,mp,mb):
        gIndex = self.cells.getCellIndex(mp)
        # If the left mouse button is clicked
        if mb == 1:
            # If it is the first cell clicked
            if self.currentCells == []:
                if gIndex != -1:
                    self.adjacentCells = self.cells.getAdjacentCells(gIndex)
                    self.currentCells.append(gIndex)
            # If it is not the first cell then it checks if it is an adjacent cell and if it is in the correct direction
            else:
                if gIndex != -1:
                    if gIndex in self.adjacentCells:
                        directionIndex = self.adjacentCells.index(gIndex)
                        if directionIndex == 0 or directionIndex == 1:
                            if self.direction != LR:
                                cell = self.currentCells[-1]
                                self.currentCells = []
                                self.currentCells.append(cell)
                            self.currentCells.append(gIndex)
                            self.direction = LR
                        elif directionIndex == 2 or directionIndex == 3:
                            if self.direction != UD:
                                cell = self.currentCells[-1]
                                self.currentCells = []
                                self.currentCells.append(cell)
                            self.direction = UD
                            self.currentCells.append(gIndex)
                        elif directionIndex == 4 or directionIndex == 5:
                            if self.direction != DTOL:
                                cell = self.currentCells[-1]
                                self.currentCells = []
                                self.currentCells.append(cell)
                            self.direction = DTOL
                            self.currentCells.append(gIndex)
                        elif directionIndex == 6 or directionIndex == 7:
                            if self.direction != DTOR:
                                cell = self.currentCells[-1]
                                self.currentCells = []
                                self.currentCells.append(cell)
                            self.direction = DTOR
                            self.currentCells.append(gIndex)
                    else:
                        self.currentCells = []
                        self.currentCells.append(gIndex)
                    self.adjacentCells = self.cells.getAdjacentCells(gIndex)
        # If the right mouse button is clicked
        elif mb == 3:
            # Removes the cell from the current cells
            if gIndex == self.currentCells[0] or gIndex == self.currentCells[-1]:
                self.currentCells.pop(self.currentCells.index(gIndex))

    # Puts a line through the current cells to show which are selected
    def lineThrough(self,win):
        if len(self.currentCells) > 0:
            initial = self.currentCells[0]
            final = self.currentCells[-1]
            grid = self.cells.cells
            width = grid[initial][2]
            height = grid[initial][3]
            if self.direction == LR:
                startxy = (grid[initial][0], grid[initial][1]+(height/2))
                endxy = (grid[final][0]+width, grid[final][1]+(height/2))
            elif self.direction == UD:
                startxy = (grid[initial][0]+(width/2), grid[initial][1])
                endxy = (grid[final][0]+(width/2), grid[final][1]+height)
            elif self.direction == DTOL:
                startxy = (grid[initial][0], grid[initial][1])
                endxy = (grid[final][0]+width, grid[final][1]+height)
            elif self.direction == DTOR:
                startxy = (grid[initial][0], grid[initial][1]+height)
                endxy = (grid[final][0]+width, grid[final][1])
            pygame.draw.line(win,RED,startxy,endxy,3)

    # Makes the word using the indicies of the current cells
    def makeWord(self):
        word = ''
        for i in self.currentCells:
            word += str(self.ltrs[i])
        return word

    # Makes the word appear on the screen
    def blitWord(self,win,word):
        font =  pygame.font.SysFont("yugothicyugothicuilight",30)
        txtSurface = font.render(word, True, BLACK)
        win.blit(txtSurface,(300,650))
        
    # Checks the word to see if it is in the word list
    def checkWord(self,word,wordList):
        if word in wordList:
            return True

class DataStructure(object):

    # Initializes the DataStructure class
    def __init__(self,title,row,column,ltrs,words):
        self.title = title
        self.rows = row
        self.columns = column
        self.ltrs = ltrs
        self.words = words

# Function to open the puzzle file and then return a list of DataStructures based on the puzzle file
def openPuzzle():
    fi = open('puzzles.txt', 'r')
    puzzles = []
    numOfPuzzles = int(fi.readline().strip())
    for p in range(numOfPuzzles):
        newTitle = fi.readline().strip()
        rows = int(fi.readline().strip())
        columns = int(fi.readline().strip())
        letters = []
        for row in range(rows):
            newRow = fi.readline().strip().split()
            letters += newRow
        numWords = int(fi.readline().strip())
        words = []
        for word in range(numWords):
            newWord = fi.readline().strip()
            words.append(newWord)
        newPuzzle = DataStructure(newTitle,rows,columns,letters,words)
        puzzles.append(newPuzzle)
    return puzzles

def drawWin():
    global isMenuScreen
    global isGameScreen
    global isDoneScreen
    win.fill(BKG)
    # Displays the Menu Screen with the title and buttons
    if isMenuScreen:
        isGameScreen = False
        isDoneScreen = False
        font =  pygame.font.SysFont("yugothicyugothicuilight",50)
        txtSurface = font.render('Word Search', True, BLACK)
        win.blit(txtSurface,(220,100))
        menu.draw(win)
    # Displays the game screen with title, grid, word, and word list
    elif isGameScreen:
        font =  pygame.font.SysFont("yugothicyugothicuilight",50)
        txtSurface = font.render(puzzles[current].title, True, BLACK)
        x = (700/2) - (txtSurface.get_width()/2)
        win.blit(txtSurface,(x,25))
        allCells = wordSearch.currentCells + foundCells
        grid.draw(win,allCells)
        wordSearch.drawLtrs(win,grid.cells)
        wordSearch.blitWord(win,word)
        wordList.draw(win,foundWords)
        wordSearch.lineThrough(win)
    # Displays the screen when the player is done with the word search with text and a button
    elif isDoneScreen:
        font =  pygame.font.SysFont("yugothicyugothicuilight",30)
        txtSurface = font.render('Congratulations you found all the words', True, BLACK)
        win.blit(txtSurface,(120,200))
        home.draw(win)
        txtSurface = font.render('Home', True, BLACK)
        win.blit(txtSurface,(310,310))
    pygame.display.update()

# Initialize variables 
win = pygame.display.set_mode((700,700))
current = 0
inPlay = True
isMenuScreen = True
isGameScreen = False
ifDoneScreen = False
puzzles = openPuzzle()
titles = []
for puzzle in puzzles:
    titles.append(puzzle.title)
menu = Menu(titles,(200,200,300,300),2,2,10)
home = Button((300,300,100,50))

# Main game loop
while inPlay:
    drawWin()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        # If the mousehas been clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            mouseBtn = event.button
            if isMenuScreen:
                # Tests which button has been clicked and initializes the game screen
                for i,btn in enumerate(menu.buttons):
                    button = btn.collide(mousePos)
                    if button != -1:
                        current = i
                        isGameScreen = True
                        isMenuScreen = False
                        grid = GridClass.Grid((50,100,500,500),puzzles[current].columns,puzzles[current].rows,4)
                        ltrs = puzzles[current].ltrs
                        wordSearch = WordSearch(ltrs,grid)
                        wordList = WordList(puzzles[current].words,(600,150,700,50),1,7)
                        word = ''
                        foundWords = []
                        foundCells = []
            if isGameScreen:
                # Updates current cells and the word 
                wordSearch.findCurrentCells(mousePos,mouseBtn)
                word = wordSearch.makeWord()
                # Checks if the word is in the word list
                if wordSearch.checkWord(word,puzzles[current].words):
                    foundWords.append(word)
                    foundCells += wordSearch.currentCells
                # Checks if all the words have been found
                if set(foundWords) == set(puzzles[current].words):
                    isDoneScreen = True
                    isGameScreen = False
            if isDoneScreen:
                # Sends the player to the home screen once the button has been clicked
                if home.collide(mousePos) != -1:
                    isMenuScreen = True
                    isDoneScreen = False
                    
                                    

pygame.quit()
