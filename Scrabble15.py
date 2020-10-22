from enum import Enum
from numpy import random
from pathlib import Path
import re
import sys



#==============================================
# Words Dictionary
#==============================================

class Words:
    letterPoints = {
        "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, 
        "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, 
        "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1,
        "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
        }
    
    words = []
    @classmethod
    def load(cls):
        cls.words = Words.readFile()

    @classmethod
    def readFile(cls):
        pathName = r"C:\Users\casey ranft\Documents\Casey Ranft\Artificial Intelligence"
        fileName = r"Collins Scrabble Words (2019).txt"
        words = []

        # is words file local to module or in a path?
        if Path(pathName + "\\" + fileName).exists():
            fullPath = pathName + "\\" + fileName
        elif Path(fileName).exists():
            fullPath = fileName
        else:
            print("Words file is not found")
            quit()
             
        try:
            with open(fullPath, 'r') as file:
                words = list(map(str.strip, file.readlines()))

        except IOError:
            print("Words file is found but not read accessible")
            quit()
        
        return words


    # ensures all words can be fully made with the available letters
    # supplements filterRegex which includes duplicates letters.
    #   Ex rubber might come up via regex but there's only one "b" available in tiles
    @classmethod
    def filterByCount(cls, playerLetters, boardRun, words):
        #TODO: Can be Optimized
        copyFil = list.copy(words)
        remW = " "
        for f in copyFil:
            for i in playerLetters:
                countPl = playerLetters.count(i)
                countB = boardRun.count(i)
                total = countPl + countB
                #print(i, f)
                #print("Pl", countPl)
                countF = f.count(i)
                #print("F", countF)
                if countF > total:
                    if f is not remW:
                        #print("Word to Remove",f)
                        remW = f
                        words.remove(f)
        return words
        
    # filters to just words that are made up of only player letters surrounding a board string
    @classmethod
    def filterByRegex(cls, playerLetters, boardRun, words):
        #TODO: Can be Optimized by quantifying how many letters the board has space for both before and after 
        pattern = "^[" + playerLetters + "]*" + boardRun + "[" + playerLetters + "]*$"

        # doing a lot of regex calls O(1) so precompile the pattern
        prog = re.compile(pattern)
        words = list(filter(prog.search, words))
        return words

    @classmethod
    def toString(cls, words):
        return ", ".join(words)


#==============================================
# Letter Tiles
#==============================================

class Tile:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

        
class Tiles:
    tileQuantities = {
        "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, 
        "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, 
        "O": 8, "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6, "U": 4,
        "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1
        }
    tiles = []

    @classmethod
    def load(cls):
        cls.createTiles()
        cls.randomizeTiles()
        
    # create the letter tiles allowed in Scrabble
    # NOTE: the blank tile is not implemented
    @classmethod
    def createTiles(cls):
        for item in cls.tileQuantities:
            value = Words.letterPoints.get(item)
            for i in range(cls.tileQuantities.get(item)):
                cls.tiles.append(Tile(item, value))
 
    # mix up the ordering of the letter tiles
    @classmethod
    def randomizeTiles(cls):
        random.seed(9001)
        random.shuffle(cls.tiles)
    
    # return the first tile (or null) and remove from list
    @classmethod
    def pullTile(cls):
        if len(cls.tiles) > 0:
            return cls.tiles.pop(0)
        else:
            return None

    @classmethod
    def toString(cls, tiles):
        sb = StringBuilder()
        for tile in tiles:
            sb.add(tile.letter + "(" + str(tile.value) + "), ")
        return sb.toString()
    

#==============================================
# Board of Squares 
#==============================================

class MoveDirections(Enum):
    ACROSS = 0
    DOWN = 1

class ScoreMultipliers(Enum):
    Normal = 1
    DoubleLetter = 2
    TripleLetter = 3
    DoubleWord = 4
    TripleWord = 5

class Square:
    def __init__(self, squareType):
        self.scoreMultiplier = squareType
        self.tile = None

class Board:
    squares = []

    @classmethod
    def load(cls):
        cls.squares = cls.createBoard(); 

    # create board squares
    @classmethod
    def createBoard(cls):
        #Create 2D 15x15 array of Squares
        cls.squares = [[Square(ScoreMultipliers.Normal) for row in range(15)] for col in range(15)]
        
        for row in range(15):
            for col in range(15):

                #Along both diagonals
                if (row == 0 and col == 0) or (row == 0 and col == 14):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleWord)
                if (row == 5 and col == 5) or (row == 5 and col == 9):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleLetter)
                if (row == 9 and col == 5) or (row == 9 and col == 9):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleLetter)
                if (row == 6 and col == 6) or (row == 6 and col == 8):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if (row == 8 and col == 6) or (row == 8 and col == 8):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if (row == 1 and col == 1) or (row == 1 and col == 13):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
                if (row == 2 and col == 2) or (row == 2 and col == 12):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
                if (row == 3 and col == 3) or (row == 3 and col == 11):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
                if (row == 4 and col == 4) or (row == 4 and col == 10):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
                if (row == 13 and col == 1) or (row == 13 and col == 13):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
                if (row == 12 and col == 2) or (row == 12 and col == 12):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
                if (row == 11 and col == 3) or (row == 11 and col == 11):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
                if (row == 10 and col == 4) or (row == 10 and col == 10):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
                if (row == 7 and col == 7):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleWord)
        
                #3L Values
                if (row == 1 and col == 5) or (row == 1 and col == 9):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleLetter)
                if (row == 5 and col == 1) or (row == 9 and col == 1):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleLetter)
                if (row == 5 and col == 13) or (row == 9 and col == 13):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleLetter)
                if (row == 13 and col == 5) or (row == 13 and col == 9):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleLetter)

                #2L Values
                if (row == 0 and col == 3) or (row == 0 and col == 11):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if (row == 3 and col == 0) or (row == 11 and col == 0):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if (row == 3 and col == 14) or (row == 11 and col == 14):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if (row == 14 and col == 3) or (row == 14 and col == 11):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                    
                if (row == 2 and col == 6) or (row == 2 and col == 8):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if (row == 6 and col == 2) or (row == 8 and col == 2):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if (row == 12 and col == 6) or (row == 12 and col == 8):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if (row == 6 and col == 12) or (row == 8 and col == 12):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                    
                if (row == 3 and col == 7) or (row == 7 and col == 3):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)
                if(row == 7 and col == 11) or (row == 11 and col == 7):
                    cls.squares[row][col] = Square(ScoreMultipliers.DoubleLetter)

                #3W Values
                if (row == 7 and col == 0) or (row == 0 and col == 7):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleWord)
                if (row == 7 and col == 14) or (row == 14 and col == 7):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleWord)
                if (row == 14 and col == 0) or (row == 14 and col == 14):
                    cls.squares[row][col] = Square(ScoreMultipliers.TripleWord)

        return cls.squares

    # get an existing word (or letter) for a position on the board
    @classmethod
    def getRunForward(cls, row, col, moveDirection, includeStart=True):
        run = ""
        r = row
        c = col

        # While board tile exist
        while (r < 15 and c < 15):
            if (includeStart or r != row or c != col):
                if(Board.squares[r][c].tile is not None):
                    run = run + Board.squares[r][c].tile.letter
                else:
                    break

            # handle based on direction
            if moveDirection == MoveDirections.ACROSS:
                c = c + 1
            else:
                r = r + 1

        return run

    # get an existing word (or letter) for a position on the board
    @classmethod
    def getRunBackward(cls, row, col, moveDirection, includeStart= True):
        run = ""
        r = row
        c = col

        # While board tile exist
        while (r < 15 and c < 15):
            if (includeStart or r != row or c != col):
                if (Board.squares[r][c].tile is not None):
                    run = run + Board.squares[r][c].tile.letter
                else:
                    break

            # handle based on direction
            if moveDirection == MoveDirections.ACROSS:
                c = c - 1
            else:
                r = r - 1

        return run

#==============================================
# Player
#==============================================

class PlayerTypes(Enum):
    Person = 1
    Computer = 2

class Player:
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = PlayerTypes(playerType) 
        self.score = 0
        self.playerTiles = []
        self.recentPass = False

    # brings the player back up to 7 letter tiles if possible
    def pullTiles(self):
        while len(self.playerTiles) < 7 :
            t = Tiles.pullTile()
            if t is None:
                break
            else:
                self.playerTiles.append(t)

    def getPlayerTiles(self):
        return self.playerTiles

    def getTileByLetter(self, l):
        tiles = self.getPlayerTiles()
        for t in tiles:
            if t.letter == l:
                return t
                
    def removeTileByLetter(self, letter):
        tiles = self.getPlayerTiles()
        for t in tiles:
            if t.letter == letter:
                self.playerTiles.remove(t)
                break

    def getPlayerLetters(self):
        letters = ""
        for t in self.getPlayerTiles():
            letters = letters + t.letter
        return letters

    def updateScore(self, score):
        self.score = self.score + score


class Move:
    def __init__(self, word="", row=0, col=0, moveDirection=MoveDirections.ACROSS, score=0):
        self.word = word
        self.row = row
        self.col = col
        self.moveDirection = moveDirection
        self.score = score
        self.isPass = False


#==============================================
# Scrabble App Model
#==============================================

class Model:
    
    # could ask question how many Person players and how many computer players?
    # for now one of each
    @classmethod
    def load(cls):
        cls.players = [ Player("Player 1", PlayerTypes.Person),
                         Player("Player 2", PlayerTypes.Computer) ]
        cls.currentTurnPlayerIndex = 0

        Tiles.load()
        Board.load()

    # returns player pointed to by the current player index
    @classmethod
    def getCurrentTurnPlayer(cls):
        return cls.players[cls.currentTurnPlayerIndex]

    # no more tiles in inventory
    # and no tiles in player hands or if all players pass in sequence
    @classmethod
    def gameOver(cls):
        inventoryEmpty = (len(Tiles.tiles) == 0)
        playersEmpty = True
        for player in cls.players:
            if len(player.playerTiles) > 0:
                playersEmpty = False
        playersPassing = True
        for player in cls.players:
            if not player.recentPass:
                playersPassing = False
        
        return inventoryEmpty and (playersEmpty or playersPassing)
        

#==============================================
# Scrabble App Controller
#==============================================

class Controller:
    @classmethod
    def load(cls):
        Words.load()
    
    # advances the current player index wrapping it back to 0 when it hits the end
    @classmethod
    def advanceTurn(cls):
        Model.currentTurnPlayerIndex = Model.currentTurnPlayerIndex + 1
        if (Model.currentTurnPlayerIndex >= len(Model.players)):
            Model.currentTurnPlayerIndex = 0

    @classmethod
    def playMove(cls, player, move):
        # check if move is a pass
        if move.isPass:
            player.recentPass = move.isPass
        else:
            # update player score
            cls.updateScore(player, move.score)
            # place tiles on board
            cls.placeTiles(player, move)
            

    # moves tiles from player to board squares
    @classmethod
    def placeTiles(cls, player, move):
        row = move.row
        col = move.col
        
        Trace.print("placeAcrossTiles.word ", move.word)
        for l in move.word:
            square = Board.squares[row][col]
            if (square.tile is None):
                tile = player.getTileByLetter(l)
                if tile == None:
                    raise Exception("None encountered when should be a tile")
                square.tile = tile
                player.removeTileByLetter(l)

            # handle based on direction
            if move.moveDirection == MoveDirections.ACROSS:
                col = col + 1
            else:
                row = row + 1
                    
    @classmethod
    def updateScore(cls, player, score):
        player.updateScore(score)

    # returns best move from the whole
    @classmethod
    def getFittestMove(cls, player):
        Trace.print("getFittestMove")
        moveAcross = cls.getFittestMoveByDirection(player, MoveDirections.ACROSS)
        moveDown = cls.getFittestMoveByDirection(player, MoveDirections.DOWN)
        bestMove = None
        
        if ((moveAcross is not None) and (moveDown is None)):
            bestMove = moveAcross
        elif((moveAcross is None) and (moveDown is not None)):
            bestMove = moveDown
        elif((moveAcross is not None) and (moveDown is not None)):
            if moveAcross.score > moveDown.score:
                bestMove = moveAcross
            else:
                bestMove = moveDown

        # no move found? then pass
        if bestMove is None:
            bestMove = Move()
            bestMove.isPass = True

        return bestMove 
        
    # returns best move by direction for the whole board
    @classmethod
    def getFittestMoveByDirection(cls, player, moveDirection):
        Trace.print("getFittestMoveByDirection", moveDirection)

        move = None
        score = 0
        bestMove = None

        row = 0
        col = 0

        while row < 15 and col < 15:

            boardRunForward = Board.getRunForward(row, col, moveDirection)
            if len(boardRunForward) > 0:
                # found a run of some letters so check 
                move = cls.getFittestByColRow(player, boardRunForward, row, col, moveDirection)
                if move is not None:
                    if move.score > score:
                        bestMove = move

            # move based on direction
            if len(boardRunForward) > 0:
                if moveDirection == MoveDirections.ACROSS:
                    col = col + len(boardRunForward)
                else:
                    row = row + len(boardRunForward)
            else:
                if moveDirection == MoveDirections.ACROSS:
                    col = col + 1
                else:
                    row = row + 1

            # wrapping required?
            if col >= 15:
                row = row + 1
                col = 0
            elif row >= 15:
                col = col + 1
                row = 0

        Trace.print("getFittestMoveByDirection", bestMove)                  
        return bestMove
                        
    #returns best move at the board row and col
    @classmethod
    def getFittestByColRow(cls, player, boardRun, runRow, runCol, moveDirection):
        Trace.print("getFittestByColRow", boardRun, runRow, runCol, moveDirection)
        wordList = cls.getWords(player, boardRun)
        Trace.print("getFittestByColRow wordList", Words.toString(wordList))
        bestMove = None

        wordRow = runRow
        wordCol = runCol
        maxScore = 0

        for word in wordList:

            # run might be in the word more than once. eg: an in bananna
            start = 0
            while (start < len(word)):
                pos = word.find(boardRun, start)
                if pos == -1:
                    break
                else:
                    # set up to find next occurence
                    start = pos + len(boardRun)

                    # handle based on direction
                    if moveDirection == MoveDirections.ACROSS:
                        wordCol = runCol - pos
                    else:
                        wordRow = runRow - pos

                    # get score 
                    if(cls.wordInBounds(word, wordRow, wordCol, moveDirection)):
                        score = cls.scoreWord(word, wordRow, wordCol, moveDirection)
                        if (score > maxScore):
                            maxScore = score
                            bestMove = Move(word, wordRow, wordCol, moveDirection, score)
                    
        return bestMove

    # returns list of words that could work around the run
    # use Words 'filter' methods plus Board 'run' to find potential words in database
    @classmethod
    def getWords(cls, player, boardRun):
        Trace.print("getWords", boardRun)

        if len(boardRun) == 0:
            return []
        
        playerLetters = player.getPlayerLetters()
        Trace.print("playerLetters", playerLetters)
        Trace.print("boardRun", boardRun, "len(boardRun)", len(boardRun))
        Trace.print("len(Words.words)", len(Words.words))

        words1 = Words.filterByRegex(playerLetters, boardRun, Words.words)
        Trace.print("len(words1)", len(words1))
        Trace.print(Words.toString(words1))
            
        words2 = Words.filterByCount(playerLetters, boardRun, words1)
        Trace.print(Words.toString(words1))
        
        return words2

    #Check for word inbounds of 15x15 
    @classmethod
    def wordInBounds(cls, word, row, col, moveDirection):
        #TODO: If trying to place on tiles already laid down

        #print(len(word))
        #If off the board
        if col < 0 or row < 0:
            return False
        elif col > 14 or row > 14:
            return False
        elif moveDirection == MoveDirections.ACROSS and(col + len(word)) > 15:
            return False
        elif moveDirection == MoveDirections.DOWN and (row + len(word)) > 15:
            return False
        else:
            return True

    #Check for word in dictionary
    @classmethod
    def inWords(cls, word):  
        return (word in Words.words)

    @classmethod
    def scoreWord(cls, word, row, col, moveDirection):
        score = cls.scoreWordDirection(word, row, col, moveDirection)

        # check for words in the crossing direction
        if moveDirection == MoveDirections.ACROSS:
            crossDirection = MoveDirections.DOWN
        else:
            crossDirection = MoveDirections.ACROSS

        # for each letter in moveDirection see if cross word
        for l in word:
            if (Board.squares[row][col].tile is None):
                crossRunBackward = Board.getRunBackward(row, col, crossDirection, False)
                crossRunForward = Board.getRunForward(row, col, crossDirection, False)

                # found a crossing word?
                if len(crossRunBackward) > 0 or len(crossRunForward) > 0:
                    crossWord = crossRunBackward + l + crossRunForward

                    # crossword not a word? then fail original word
                    if not cls.inWords(crossWord):
                        score = 0
                        break
                    else:
                        # real row col start of word
                        crossRow = row
                        crossCol = col
                    
                        if len(crossRunBackward) > 0:
                            if crossDirection == MoveDirections.ACROSS:
                                crossCol = crossCol - len(crossRunBackward)
                            else:
                                crossrow = crossRow - len(crossRunBackward)

                        # score the crossword
                        crossScore = cls.scoreWordDirection(crossWord, crossRow, crossCol, crossDirection)

                        # cross word fails for some reason? fail original word
                        if crossScore == 0:
                            score = 0
                            break
                        else:
                            score = score + crossScore

            # advance letter in original word based on direction
            if moveDirection == MoveDirections.ACROSS:
                col = col + 1
            else:
                row = row + 1

        return score

    # return a score for a specific new word at a row and col
    @classmethod
    def scoreWordDirection(cls, word, row, col, moveDirection):
        wordScore = 0
        wordScoreMultiplier = 0

        for l in word:
            # letter is scored by default whether pre-existing or not
            letterScore = Words.letterPoints[l]
            square = Board.squares[row][col]

            # no tile placed yet so possibility of multipliers
            if square.tile is None:
                # normal, double or triple bumps up letter
                if square.scoreMultiplier == ScoreMultipliers.DoubleLetter:
                    letterScore = letterScore * 2
                elif square.scoreMultiplier == ScoreMultipliers.TripleLetter:
                    letterScore = letterScore * 3
                elif square.scoreMultiplier == ScoreMultipliers.DoubleWord:
                    wordScoreMultiplier = wordScoreMultiplier + 2
                elif square.scoreMultiplier == ScoreMultipliers.TripleWord:
                    wordScoreMultiplier = wordScoreMultiplier + 3

            # accumulate letterscores
            wordScore = wordScore + letterScore

            # handle based on direction
            if moveDirection == MoveDirections.ACROSS:
                col = col + 1
            else:
                row = row + 1

        # any word multipliers? bump word score
        if wordScoreMultiplier > 0:
            wordScore = wordScore * wordScoreMultiplier

        return wordScore
    
#==============================================
# COLOR 
#==============================================
    
class Colors(Enum):
    RED = "COMMENT"
    ORANGE = "KEYWORD"
    GREEN = "STRING"
    BLUE = "stdout"
    PURPLE = "BUILTIN"
    BLACK = "SYNC"
    BROWN = "console"

    try:
        colorPrint = sys.stdout.shell
    except AttributeError:
        colorPrint = None
        print("==========================")
        print("Colors only work with IDLE")
        print("==========================")
        
    @classmethod
    def print(cls, *args):
        colors = args[0::2]
        values = args[1::2]
        
        # even number of args? ok, else error
        if len(colors) != len(values):
            raise ValueError("Colors.print(color, text, ...) requires an even number of inputs")
        else:
            # non idle? then just print
            if cls.colorPrint is None:
                print(values)
            else:
                # space separate inputs 
                for i in range(len(values)):
                    text = str(values[i])
                    if i < len(values)-1:
                        text = text + " "
                    sys.stdout.shell.write(text, colors[i].value)

                # Create new line
                #sys.stdout.shell.write("\n")


#lightLine = "─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ "
#heavyLine = "━ ┃ ┏ ┓ ┗ ┛ ┣ ┫ ┳ ┻ ╋ " 


#==============================================
# Miscellaneous
#==============================================

class Trace:
    printEnable = False
    
    @classmethod
    def enablePrint(cls):
        cls.printEnable = True

    @classmethod
    def disablePrint(cls):
        cls.printEnable = False

    @classmethod
    def print(cls, *args):
        if cls.printEnable:
            sb = StringBuilder()
            for s in args:
                sb.add(str(s))
                sb.add(" ")
            print(sb.toString())


class StringBuilder:
    def __init__(self):
        self.s = ""

    def add(self, addS):
        self.s = self.s + addS

    def toString(self):
        return self.s
   

#==============================================
# ScrabbleApp View
#==============================================

class ViewStates(Enum):
    INTRO = 0
    PLAYING = 1
    GAMEOVER = 2
    QUIT = 3

class View:
    scoreMultiplierAbbreviations = {
        ScoreMultipliers.Normal: "   ",
        ScoreMultipliers.DoubleLetter: "Lx2",
        ScoreMultipliers.TripleLetter: "Lx3",
        ScoreMultipliers.DoubleWord: "Wx2",
        ScoreMultipliers.TripleWord: "Wx3"
        }

    @classmethod
    def load(cls):
        cls.viewState = ViewStates.INTRO

    @classmethod
    def startView(cls):
        while cls.viewState != ViewStates.QUIT:
            if cls.viewState == ViewStates.INTRO:
                cls.drawIntro()
                cls.waitForStartGame()
                cls.viewState = ViewStates.PLAYING
               
            elif cls.viewState == ViewStates.PLAYING:
                player = Model.getCurrentTurnPlayer()
                player.pullTiles()

                # computer vs person
                if player.playerType == PlayerTypes.Computer:
                    cls.drawPlaying(player)
                    move = Controller.getFittestMove(player)
                    if move.isPass:
                        cls.drawPass(player)
                    else:
                        Controller.playMove(player, move)
                else:
                    cls.drawPlaying(player)
                    move = cls.getMove()
                    if move.isPass:
                        cls.drawPass(player)
                    else:
                        Controller.playMove(player, move)
                        

                # done? or continue
                if Model.gameOver():
                    cls.viewState == ViewStates.GAMEOVER            
                else:
                    Controller.advanceTurn()

            elif cls.viewState == ViewStates.GAMEOVER:
                cls.drawGameOver()
                cls.waitForStartGame();
                cls.viewState == ViewStates.Playing

    @classmethod
    def waitForStartGame(cls):
        input("Press ENTER to start a new game.")

    @classmethod
    def drawIntro(cls):
        cls.drawHeader()
        print("How to play Scrabble \n")
        print("Place tiles across or down to score points \n")
        print("Different letters have different values \n")
        print("The board also has multipliers  \n")
        print("Differences in this online version: \n")
        print("\tNo blank tiles \n")
        print("\tComputer has big vocabulary but misses some opportunities \n")
        print("\tExpects all tiles to be placed for game to be over \n")
        cls.drawFooter()

    @classmethod
    def drawPlaying(cls, player):
        cls.drawHeader()
        cls.drawPlayerScores()
        cls.drawBoard()
        cls.drawPlayerTiles(player)
        cls.drawFooter()

    @classmethod
    def drawGameOver(cls):
        cls.drawHeader()
        cls.drawBoard()
        cls.drawWinner()
        cls.drawFooter()

    @classmethod
    def drawHeader(cls):
        Colors.print(Colors.BLACK, "\n━━━ SCRABBLE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    @classmethod
    def drawPlayerScores(cls):
        Colors.print(Colors.BLACK, "──────────────────────────────────────────────────────────────────\n")
        #sb = StringBuilder()
        Colors.print(Colors.BLACK, "│  ")
        #sb.add("│  ")
        for player in Model.players:
            Colors.print(Colors.BLACK, player.name + ": " + str(player.score) + "   │    ")
            #sb.add(player.name + ": " + str(player.score) + "   │    ")
        print()
        #print(sb.toString())
        Colors.print(Colors.BLACK, "──────────────────────────────────────────────────────────────────\n")


    @classmethod
    def drawBoard(cls):
        # print blank corner + col index numbers each 3 chars wide
        Colors.print(Colors.BLACK, "┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐\n")
        Colors.print(Colors.BLACK, "│   │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │10 │11 │12 │13 │14 │\n")
        Colors.print(Colors.BLACK, "│───│───│───│───│───│───│───│───│───│───│───│───│───│───│───│───│\n")

        # for row 0-15
        for row in range(0, 15):
            # print row index number 3 chars wide
            if row < 10:
                Colors.print(Colors.BLACK, "│ " + str(row) + " │")
            else:
                Colors.print(Colors.BLACK, "│ " + str(row) + "│")

            # for col 0-15
            for col in range(0, 15):
                square = Board.squares[row][col]
                # if a tile is already placed then print tile letter 3 chars wide
                if square.tile is not None:
                    Colors.print(Colors.BLUE, " " + square.tile.letter)
                    Colors.print(Colors.BLACK, " │")
                else:
                    Colors.print(Colors.BLACK, View.scoreMultiplierAbbreviations[square.scoreMultiplier] + "│")
            print()
            
            if row < 14:
                Colors.print(Colors.BLACK,  "├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤")
                print()
            else:
                Colors.print(Colors.BLACK,  "└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘")
                print()
          
    @classmethod
    def drawPlayerTiles(cls, player):
        print("─── Player Tiles ─────────────────────────────────────────────────")
        sb = StringBuilder()
        sb.add(player.name + ": letter(value): ")

        # forech tile in player.tiles
        for tile in player.playerTiles:
            #print tile.letter and tile.value
            sb.add(str(tile.letter) + "(" + str(tile.value) + ") ")
        print(sb.toString())
        print("──────────────────────────────────────────────────────────────────")

    @classmethod
    def drawPass(cls, player):
        print("─── Player PASSES ─────────────────────────────────────────────────")
        print("    " + player.name + " Passes with Letters: " + player.getPlayerLetters())        
        print("──────────────────────────────────────────────────────────────────")
        
    @classmethod
    def drawWinner(cls):
        winningPlayer = max(Model.players, key=lambda player: player.score)
       
        print("─── GAME OVER ─────────────────────────────────────────────────")
        print(" Congratulations to " + winningPlayer.name + " with a score of " + str(winningPlayer.score))
        print("──────────────────────────────────────────────────────────────────")
 
    @classmethod
    def drawFooter(cls):
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    @classmethod
    def getMove(cls):
        while (True):
            inputString = input("Enter a move in the format: word,row,col,across|down, or pass \n\t")
            inputString = inputString.upper()
            if inputString == "PASS":
                move = Move()
                move.isPass = True
                return move
            inputs = inputString.strip().split(",")            
            if len(inputs) != 4:
                Colors.print(Colors.RED, "\n\t<Missing some inputs. Please correct. \n\n")
            else:
                wordInput = inputs[0].strip()
                rowInput = inputs[1].strip()
                colInput = inputs[2].strip()
                moveDirectionInput = inputs[3].strip()

                # missing
                if len(wordInput) == 0:
                    Colors.print(Colors.RED, "\n\tMissing 'Word'. Please correct. \n\n")
                elif len(rowInput) == 0:
                    Colors.print(Colors.RED, "\n\tMissing 'row'. Please correct. \n\n")
                elif len(colInput) == 0:
                    Colors.print(Colors.RED, "\n\tMissing 'column'. Please correct. \n\n")
                elif len(moveDirectionInput) == 0:
                    Colors.print(Colors.RED, "\n\tMissing 'direction'. Please correct. \n\n")

                # wrong type or range
                elif re.match("^[A-Z]+$", wordInput) == None:
                    Colors.print(Colors.RED, "\n\tWord can only contain letters'. Please correct. \n\n")
                elif re.match("^\d+$", rowInput) == None:
                    Colors.print(Colors.RED, "\n\tRow should be a number from 0 to 14'. Please correct. \n\n")
                elif re.match("^\d+$", colInput) == None:
                    Colors.print(Colors.RED, "\n\tColumn should be a number from 0 to 14'. Please correct. \n\n")
                elif not Controller.wordInBounds(wordInput, int(rowInput), int(colInput), MoveDirections[moveDirectionInput]):
                    Colors.print(Colors.RED, "\n\tWord out of bounds'. Please correct. \n")
                elif re.match("^ACROSS|DOWN$", moveDirectionInput) == None:
                    Colors.print(Colors.RED, "\n\tDirection should be either 'across' or 'down'. Please correct. \n\n")
                elif not Controller.inWords(wordInput):
                    Colors.print(Colors.RED, "\n\tWord: " + wordInput +" NOT IN DICTIONARY \n\n")


                # check that the word works at the place on the board
                else:
                    word = wordInput
                    row = int(rowInput)
                    col = int(colInput)
                    
                    moveDirection = MoveDirections.DOWN
                    if moveDirectionInput == "ACROSS":
                        moveDirection = MoveDirections.ACROSS

                    score = Controller.scoreWord(word, row, col, moveDirection)  
                    if score == 0:
                        Colors.print(Colors.RED, "\n\tInvalid move. Please correct. \n\n")
                    else:
                        return Move(word, row, col, moveDirection, score)
                    
#==============================================
# TEST
#==============================================

class Test:
   
    def wordsTest(self):
        print("===============")  
        print("wordsTest setup")
        Words.load()
        playerLetters = "AABESTD"
        boardRun = "LI"

        print("===============")  

        matches1 = Words.filterByRegex(playerLetters, boardRun, Words.words)

        print("METHOD:")
        print("  return List() Words.filterByRegex(playerLetters, boardRun, words)")
        print("Description:")
        print("  Search database to return words that include the boardRun exactly and otherwise only playerLetters")
        print("PARAMETERS")
        print("  playerLetters: ", playerLetters)
        print("  boardRun: ", boardRun)
        print("  words:", "<Words.words> full database")
        print("RETURN: ")
        print("  " + ",".join(matches1))
        print()


        matches2 = Words.filterByCount(playerLetters, boardRun, matches1)

        print("METHOD:")
        print("  return List() Words.filterByCount(playerLetters, boardRun, words)")
        print("Description:")
        print("  Filters list of words by letter counts available in the boardRun and playerLetters")
        print("PARAMETERS")
        print("  playerLetters: ", playerLetters)
        print("  boardRun: ", boardRun)
        print("  words:", "a filtered list")
        print("RETURN: ")
        print("  " + ",".join(matches2))
        print()

        print("===============")  
        print("wordsTest teardown")
        print("===============")  


    def tilesTest(self):

        print("===============")  
        print("tilesTest setup")
        Tiles.load()

        print("===============")  

        tile = Tiles.pullTile()

        print("METHOD:")
        print("  return Tile Tiles.pullTile()")
        print("Description:")
        print("  Pop an available tile from the randomized tile inventory")
        print("RETURN: ")
        print("  Tile letter(value): " + str(tile.letter) + "(" + str(tile.value) + ")" )
        print()

        print("===============")  
        print("tilesTest teardown")
        print("===============")  


    def boardTest(self):
        print("===============")  
        print("boardTest setup")
        Model.load()
        View.load()
       
        print("===============")  
        print(" board loaded at init using View.drawBoard() to show")
        View.drawBoard()

        print("===============")  
        print("boardTest teardown")
        print("===============")  


    def playerTest(self):
        print("===============")  
        print("playerTest setup")
        Tiles.load()
        player = Player('Jeffery', 1)

        print("===============")  

        player.pullTiles()

        print("METHOD:")
        print("  void Player.pullTiles()")
        print("Description:")
        print("  get up to 7 tiles from the Tiles inventory and assign them to the players 'hand'")
        print("RETURN: ")
        print(" using View.drawPlayerTiles(player)")
        View.drawPlayerTiles(player)
        print()

        #trivial updateScore()

        print("===============")  
        print("playerTest teardown")
        print("===============")  


    def controllerTest(self):
       
        print("===============")  
        print("controllerTest setup")
       
        Model.load()
        Controller.load()
        View.load()
        
        player = Player("Jeffrey", 1)
        player.pullTiles()

        print("===============")
        """
        move = Move("ROTA", 7, 7, 0)
        Controller.placeTiles(player, move)
                
        if Controller.isValidMove(move):
            print("word", move.word, "True")
        else:
            print("word", move.word, "False")

        move = Move("VEG", 6, 7, 0)
        Controller.placeTiles(player, move)
        
        if Controller.isValidMove(move):
            print("word", move.word, "True")
        else:
            print("word", move.word, "False")
        """  
        word = player.getPlayerLetters()
        row = 0
        col = 0
        moveDirection = MoveDirections.ACROSS
        score = Controller.scoreWord(word, row, col, moveDirection)
        
        #score = Contorller.scoreWord(move.word, move.row, move.col, move.moveDirection)

        
        print("METHOD:")
        print(" int scoreWord(word, row, col, moveDirection)")
        print("Description:")
        print("  score a potential word on the board taking into accont square multipliers and pre-exiting tiles")
        print("PARAMETERS")
        print("  word: " + word)
        print("  row: " + str(row))
        print("  col: " + str(col))
        print("  moveDirection: " + str(moveDirection))
        print("RETURN: ")
        print("  score: " + str(score))

        print("===============")
        
        Controller.placeTiles(player, Move(word, row, col, moveDirection, 0))

        print("METHOD:")
        print(" int placeTiles(player, word, row, col, moveDirection)")
        print("Description:")
        print("  move the tiles from the player to the board")
        print("PARAMETERS")
        print("  player: " + player.name)
        print("  word: " + word)
        print("  row: " + str(row))
        print("  col: " + str(col))
        print("  moveDirection: " + str(moveDirection))
        print("RETURN: ")
        print("  show using View.DrawBoard the letters at row, col ")

        View.drawBoard()

        # trivial 

        print("===============")  
        print("controllerTest teardown")
        print("===============")


#==============================================
# MAIN
#==============================================

def main():
    test = Test()

    #test.wordsTest()
    #test.tilesTest()
    #test.boardTest()
    #test.playerTest()
    #test.controllerTest()
   
    Model.load()
    Controller.load()
    View.load()

    View.startView()
   
main()
