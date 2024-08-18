#Chess.py
"""
This class is responsible for storing all the information about the current state of a chess game
"""
class GameState():
    """
    self.board
        -Lists of lists
        -To represent every piece on the chess board
        -8x8 2d list, each element of the list has 2 characters.
        -First character represents the color of the piece
        -Second character represents the type of piece
    """
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
    "Takes a move as a parameter and executes it (This will not work for castling, and en-passant)"
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players


    '''Undo the last move made'''
    def undoMove(self):
        if len(self.moveLog) != 0: ##make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() # For now we will not worry about checks


    '''
    All moves without considering checks.
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c, moves) #calls the appropriate move function based on piece type
        return moves
    
    "Get all the pawn moves for the pawn located at row,col add these moves to the list"
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == '--': #1 square pawn advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c -1  >= 0: #captures to the left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r,c), (r-1, c-1), self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: #black pawn moves
            if self.board[r + 1][c] == "--": # 1 square move
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2 square move
                    moves.append(Move((r,c), (r+2, c), self.board))
                #captures
            if c-1 >= 0: #capture to left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1, c-1), self.board))
            if c + 1 <= 7: #capture to right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1, c+1), self.board))

    
    "Get all the rook moves for the rook located at row,col add these moves to the list"
    def getRookMoves(self,r,c,moves):
        pass
    "Get all the Knight moves for the Knight located at row,col add these moves to the list"
    def getKnightMoves(self,r,c,moves):
        pass
    "Get all the Bishop moves for the Bishop located at row,col add these moves to the list"
    def getBishopMoves(self,r,c,moves):
        pass
    "Get all the Queen moves for the Queen located at row,col add these moves to the list"
    def getQueenMoves(self,r,c,moves):
        pass
    "Get all the King moves for the King located at row,col add these moves to the list"
    def getKingMoves(self,r,c,moves):
        pass

 
class Move():
    #maps keys to values
    #key : value
    ranksToRows = {"1": 7,"2": 6,"3": 5,"4": 4,
                   "5": 3,"6": 2,"7": 1,"8": 0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)

    "Overriding the equals method"
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        #you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]