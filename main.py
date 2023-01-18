class Game:
    def __init__(self) -> None:
        """
        Initialize game variables
        """
        self.board = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP' , 'bP' , 'bP' , 'bP', 'bP', 'bP' , 'bP' , 'bP' ],
        [' -' , ' -' , ' -' , ' -' , ' -', ' -' , ' -' , ' -' ],
        [' -' , ' -' , ' -' , ' -' , ' -', ' -' , ' -' , ' -' ],
        [' -' , ' -' , ' -' , ' -' , ' -', ' -' , ' -' , ' -' ],
        [' -' , ' -' , ' -' , ' -' , ' -', ' -' , ' -' , ' -' ],
        ['wP' , 'wP' , 'wP' , 'wP', 'wP', 'wP' , 'wP' , 'wP' ],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.pieces_board = [[],[],[],[],[],[],[],[]]
        for r in range(8):
            for c in range(8):
                piece = self.find_piece(self.board[r][c])
                if piece != None:
                    self.pieces_board[r].append(piece)
                else:
                    self.pieces_board[r].append(self.board[r][c] + "   ")
        

        self.current_color = "w"


    def update(self):
        """
        Game loop
        """
        playing = True
        while  playing:
            self.print()
            # Chose piece
            available_pieces = self.find_available_pieces() # find availalbe pieces 
            print("Your pieces are") # print pieces
            self.print(available_pieces) # print pieces
            # While piece isnt properly chosen cause no moves # gets piece and availabe moves
            piece_is_chosen = False
            while piece_is_chosen != True:
                piece = int(input("Which one do you want to move??(index)")) # chose which piece to move
                if piece == 100:
                    break
                indexes = available_pieces[piece][1] # get index of the piece on the board
                chosen_piece = self.pieces_board[indexes[0]][indexes[1]] # get the piece object
                # Get moves
                available_moves = chosen_piece.find_moves(self.board, indexes) # get available moves for piece
                if len(available_moves) != 0:
                    piece_is_chosen = True
                else:
                    print("The piece u have chosen has no moves. Please kindly chose another one u Dumb MFing Bitch u dont know how to play?")
            print(available_moves)
            move = available_moves[int(input("Which move? [i]"))][0] # get new coordinates to move to
            # If eating or just moving
            if self.board[move[0]][move[1]] != ' -': 
                self.eat(indexes, move)
                chosen_piece.moves += 1
            else:
                self.move(indexes, move)     
                chosen_piece.moves += 1 
            # change color:
            if self.current_color == "w":
                self.current_color = "b"
            else:
                self.current_color = "w"


    def board_to_str(self) -> str:
        """
        Convert board to string
        """
        board_str = ""
        for i in range(8):
            board_str = board_str + ','.join(self.board[i]) + ','
        return  board_str[:-1]

    def find_piece(self, code : str):
        """
        Turn piece code into class
        """
        first_letter = code[0]
        second_letter = code[1]
        if  second_letter == "K":
            return self.King(first_letter)
        elif second_letter == "Q":
            return self.Queen(first_letter)
        elif second_letter == "B":
            return self.Bishop(first_letter)
        elif second_letter == "N":
            return self.Knight(first_letter)
        elif second_letter == "R":
            return self.Rook(first_letter)
        elif second_letter == "P":
            return self.Pawn(first_letter)
        else:
            return None

    def find_available_pieces(self) -> list:
        """
        Find players pieces so he can choose to move
        """
        available_pieces  = []
        index = 0
        for r in range(8):
            for c in range(8):
                if self.board[r][c][0] == self.current_color:
                    available_pieces.append([self.board[r][c]+ " " +  str(index), [r, c]] )
                    index += 1

        return available_pieces

    def print(self, _board = "") -> None:
        """
        Prints The board properly for good UI
        """
        if _board == "":
            board = self.board
        else:
            board = _board
        for i in range (len(board)):
            print(board[i])

    def move(self, _indexes : list, _move : list) -> None:
        # change in board
        piece = self.board[_indexes[0]][_indexes[1]]
        next = self.board[_move[0]][_move[1]]

        self.board[_indexes[0]][_indexes[1]] = next
        self.board[_move[0]][_move[1]] = piece

        # change in pieces board
        piece = self.pieces_board[_indexes[0]][_indexes[1]]
        next = self.pieces_board[_move[0]][_move[1]]

        self.pieces_board[_indexes[0]][_indexes[1]] = next
        self.pieces_board[_move[0]][_move[1]] = piece
        return

    def eat(self, _indexes : list, _move : list) -> None:
        self.move(_indexes, _move)

        self.board[_indexes[0]][_indexes[1]] = ' -'
        self.pieces_board[_indexes[0]][_indexes[1]] = ' -'

        return

    class King:
        def __init__(self, color : str) -> None:
            self.color = color
            if self.color == "w":
                self.image = "images/white_king.png"
            else:
                self.image = "images/black_king.png"
            self.moves = 0

        def __repr__(self):
            return f"King({self.color})"

        def find_moves(self, _board :list, _position :list) -> list:
            available_moves = []
            # up
            try:
                if _board[_position[0]-1][_position[1]] == ' -':
                    available_moves.append([[_position[0]-1, _position[1]], 'u'])
                elif _board[_position[0]-1][_position[1]][0] != self.color:
                    available_moves.append([[_position[0]-1, _position[1]], 'eat u'])
            except:
                print("Cant move up exception")

            # down
            try:
                if _board[_position[0]+1][_position[1]] == ' -':
                    available_moves.append([[_position[0]+1, _position[1]], 'd'])
                elif _board[_position[0]+1][_position[1]][0] != self.color:
                    available_moves.append([[_position[0]+1, _position[1]], 'eat d'])
            except:
                print("Cant move up exception")

            # left
            try:
                if _board[_position[0]][_position[1]-1] == ' -':
                    available_moves.append([[_position[0], _position[1]-1], 'L'])
                elif _board[_position[0]][_position[1]-1][0] != self.color:
                    available_moves.append([[_position[0], _position[1]-1], 'eat L'])
            except:
                print("Cant move up exception")

            # right
            try:
                if _board[_position[0]][_position[1]+1] == ' -':
                    available_moves.append([[_position[0], _position[1]+1], 'R'])
                elif _board[_position[0]][_position[1]+1][0] != self.color:
                    available_moves.append([[_position[0], _position[1]+1], 'eat R'])
            except:
                print("Cant move up exception")

            # up right
            try:
                if _board[_position[0]-1][_position[1]+1] == ' -':
                    available_moves.append([[_position[0]-1, _position[1]+1], 'uR'])
                elif _board[_position[0]-1][_position[1]+1][0] != self.color:
                    available_moves.append([[_position[0]-1, _position[1]+1], 'eat uR'])
            except:
                print("Cant move up right exception")

            # up left
            try:
                if _board[_position[0]-1][_position[1]-1] == ' -':
                    available_moves.append([[_position[0]-1, _position[1]-1], 'uL'])
                elif _board[_position[0]-1][_position[1]-1][0] != self.color:
                    available_moves.append([[_position[0]-1, _position[1]-1], 'eat uL'])
            except:
                print("Cant move up left exception")

            # down right
            try:
                if _board[_position[0]+1][_position[1]+1] == ' -':
                    available_moves.append([[_position[0]+1, _position[1]+1], 'dR'])
                elif _board[_position[0]+1][_position[1]+1][0] != self.color:
                    available_moves.append([[_position[0]+1, _position[1]+1], 'eat dR'])
            except:
                print("Cant move down right exception")

            # down left
            try:
                if _board[_position[0]+1][_position[1]-1] == ' -':
                    available_moves.append([[_position[0]+1, _position[1]-1], 'dR'])
                elif _board[_position[0]+1][_position[1]-1][0] != self.color:
                    available_moves.append([[_position[0]+1, _position[1]-1], 'eat dR'])
            except:
                print("Cant move down left exception")

            return available_moves

    class Queen:
        def __init__(self, color : str) -> None:
            self.color = color 
            if self.color == "w":
                self.image = "images/white_queen.png"
            else:
                self.image = "images/black_queen.png"

            self.moves = 0
            pass

        def __repr__(self):
            return f"Queen({self.color})"

        def find_moves(self, _board : list, _position : list) -> list:
            available_moves = []
            bishop_moves = Game.Bishop.find_moves(Game.Bishop(self.color), _board, _position)
            rook_moves = Game.Rook.find_moves(Game.Rook(self.color), _board, _position)
            for move in bishop_moves:
                available_moves.append(move)
            for move in rook_moves:
                available_moves.append(move)
            return available_moves

    class Bishop:
        def __init__(self, color : str) -> None:
            self.color = color
            if self.color == "w":
                self.image = "images/white_bishop.png"
            else:
                self.image = "images/black_bishop.png"

            self.moves = 0
            return

        def __repr__(self) -> str:
            return f"Bishop({self.color})"
            
        def find_moves(self, _board : list, _position : list) -> list:
            availalbe_moves = []
            #up right
            up_right_min = min(_position[0], 7-_position[1])        
            for i in range(1, up_right_min+1):
                # move
                if _board[_position[0]-i][_position[1]+i] == ' -':
                    availalbe_moves.append([[_position[0]-i, _position[1]+i], f'move uR{i}'])
                # eat
                elif _board[_position[0]-i][_position[1]+i][0] != self.color:
                    availalbe_moves.append([[_position[0]-i, _position[1]+i], 'eat uR'])
                    break
                else:
                    break

            # up left
            up_left_min = min(_position[0], _position[1])
            for i in range(1, up_left_min+1):
                if _board[_position[0]-i][_position[1]-i] == ' -':
                    availalbe_moves.append([[_position[0]-i, _position[1]-i], f'move uL{i}'])
                elif _board[_position[0]-i][_position[1]-i][0] != self.color:
                    availalbe_moves.append([[_position[0]-i, _position[1]-i], 'eat uL'])
                    break
                else:
                    break

            # down right
            down_right_min = min(7-_position[0], 7-_position[1])
            for i in range(1, down_right_min+1):
                if _board[_position[0]+i][_position[1]+i] == ' -':
                    availalbe_moves.append([[_position[0]+i, _position[1]+i], f'move dR{i}'])
                elif _board[_position[0]+i][_position[1]+i][0] != self.color:
                    availalbe_moves.append([[_position[0]+i, _position[1]+i], 'eat dR'])
                    break
                else:
                    break

            # down left
            down_left_min = min(7-_position[0], _position[1])
            for i in range(1, down_left_min+1):
                if _board[_position[0]+i][_position[1]-i] == ' -':
                    availalbe_moves.append([[_position[0]+i, _position[1]-i], f'move dL{i}'])
                elif _board[_position[0]+i][_position[1]-i][0] != self.color:
                    availalbe_moves.append([[_position[0]+i, _position[1]-i], 'eat dL'])
                    break
                else:
                    break
            
            return availalbe_moves

    class Knight:
        def __init__(self, color : str) -> None:
            self.color = color
            if self.color == "w":
                self.image = "images/white_knight.png"
            else:
                self.image = "images/black_knight.png"
            self.moves = 0

        def __repr__(self):
            return f"Knight({self.color})"

        def find_moves(self, _board : list, _position : list) -> list:
            available_moves = []
            # up right
            try:
                if _board[_position[0]-2][_position[1]+1] == ' -':
                    available_moves.append([[_position[0]-2, _position[1]+1], 'uR'])
                elif _board[_position[0]-2][_position[1]+1][0] != self.color:
                    available_moves.append([[_position[0]-2, _position[1]+1], 'eat uR'])
            except:
                print("Cant move up right exception")

            # up left
            try:
                if _board[_position[0]-2][_position[1]-1] == ' -':
                    available_moves.append([[_position[0]-2, _position[1]-1], 'uL'])
                elif _board[_position[0]-2][_position[1]-1][0] != self.color:
                    available_moves.append([[_position[0]-2, _position[1]-1], 'eat uL'])
            except:
                print("Cant move up left exception")

            # down right
            try:
                if _board[_position[0]+2][_position[1]+1] == ' -':
                    available_moves.append([[_position[0]+2, _position[1]+1], 'dR'])
                elif _board[_position[0]+2][_position[1]+1][0] != self.color:
                    available_moves.append([[_position[0]+2, _position[1]+1], 'eat dR'])
            except:
                print("Cant move down right exception")

            # down left
            try:
                if _board[_position[0]+2][_position[1]-1] == ' -':
                    available_moves.append([[_position[0]+2, _position[1]-1], 'dL'])
                elif _board[_position[0]+2][_position[1]-1][0] != self.color:
                    available_moves.append([[_position[0]+2, _position[1]-1], 'eat dL'])
            except:
                print("Cant move down left exception")

            # right up
            try:
                if _board[_position[0]-1][_position[1]+2] == ' -':
                    available_moves.append([[_position[0]-1, _position[1]+2], 'Ru'])
                elif _board[_position[0]-1][_position[1]+2][0] != self.color:
                    available_moves.append([[_position[0]-1, _position[1]+2], 'eat Ru'])
            except:
                print("Cant move right up exception")

            # right down
            try:
                if _board[_position[0]+1][_position[1]+2] == ' -':
                    available_moves.append([[_position[0]+1, _position[1]+2], 'Rd'])
                elif _board[_position[0]+1][_position[1]+2][0] != self.color:
                    available_moves.append([[_position[0]+1, _position[1]+2], 'eat Rd'])
            except:
                print("Cant move right down exception")

            # left up
            try:
                if _board[_position[0]-1][_position[1]-2] == ' -':
                    available_moves.append([[_position[0]-1, _position[1]-2], 'Lu'])
                elif _board[_position[0]-1][_position[1]-2][0] != self.color:
                    available_moves.append([[_position[0]-1, _position[1]-2], 'eat Lu'])
            except:
                print("Cant move left up exception")

            # left down
            try:
                if _board[_position[0]+1][_position[1]-2] == ' -':
                    available_moves.append([[_position[0]+1, _position[1]-2], 'Ld'])
                elif _board[_position[0]+1][_position[1]-2][0] != self.color:
                    available_moves.append([[_position[0]+1, _position[1]-2], 'eat Ld'])
            except:
                print("Cant move left down exception")

            return available_moves

    class Rook:
        def __init__(self, color : str) -> None:
            self.color = color
            if self.color == "w":
                self.image = "images/white_rook.png"
            else:
                self.image = "images/black_rook.png"
            self.moves = 0
            return

        def __repr__(self) -> str:
            return f"Rook({self.color})"
            
        def find_moves(self, _board : list, _position : list) -> list:
            availalbe_moves = []
            #up       
            for i in range(1, _position[0]+1):
                # move
                if _board[_position[0]-i][_position[1]] == ' -':
                    availalbe_moves.append([[_position[0]-i, _position[1]], f'move u{i}'])
                # eat
                elif _board[_position[0]-i][_position[1]][0] != self.color:
                    availalbe_moves.append([[_position[0]-i, _position[1]], 'eat u'])
                    break
                else:
                    break

            # left
            for i in range(1, _position[1]+1):
                if _board[_position[0]][_position[1]-i] == ' -':
                    availalbe_moves.append([[_position[0], _position[1]-i], f'move L{i}'])
                elif _board[_position[0]][_position[1]-i][0] != self.color:
                    availalbe_moves.append([[_position[0], _position[1]-i], 'eat L'])
                    break
                else:
                    break

            # down 
            for i in range(1, 7-_position[0]+1):
                if _board[_position[0]+i][_position[1]] == ' -':
                    availalbe_moves.append([[_position[0]+i, _position[1]], f'move d{i}'])
                elif _board[_position[0]+i][_position[1]][0] != self.color:
                    availalbe_moves.append([[_position[0]+i, _position[1]], 'eat d'])
                    break
                else:
                    break

            # right
            for i in range(1, 7-_position[1]+1):
                if _board[_position[0]][_position[1]+i] == ' -':
                    availalbe_moves.append([[_position[0], _position[1]+i], f'move R{i}'])
                elif _board[_position[0]][_position[1]+i][0] != self.color:
                    availalbe_moves.append([[_position[0], _position[1]+i], 'eat R'])
                    break
                else:
                    break
            
            return availalbe_moves

    class Pawn:
        def __init__(self, color : str) -> None:
            self.color = color
            if self.color == 'w':
                self.direction = -1
                self.image = "images/white_pawn.png"
            else:
                self.direction = 1
                self.image = "images/black_pawn.png"
            self.moves = 0
            return

        def __repr__(self):
            return f"Pawn({self.color})"

        def find_moves(self, _board : list, _position : list) -> list:
            available_moves  = []
            # move one square forward
            if _board[_position[0]+self.direction][_position[1]] == ' -':
                available_moves.append([[_position[0]+self.direction, _position[1]], "1"])
            # eat on the right
            try:
                if _board[_position[0]+self.direction][_position[1]+1] != ' -' and _board[_position[0]+self.direction][_position[1]+1][0] != self.color:
                    available_moves.append([[_position[0]+self.direction, _position[1]+1], "eat r"])
            except:
                print("Cant eat on the right exception")
            # eat on the left
            try:
                if _board[_position[0]+self.direction][_position[1]-1] != ' -' and _board[_position[0]+self.direction][_position[1]-1][0] != self.color:
                    available_moves.append([[_position[0]+self.direction, _position[1]-1], "eat l"])
            except:
                print("Cant eat on the left exception")
            # move two squares forward
            if self.moves == 0 and _board[_position[0]+self.direction][_position[1]] == ' -' and _board[_position[0]+self.direction*2][_position[1]] == ' -':
                available_moves.append([[_position[0]+self.direction*2, _position[1]], "2"])


            return available_moves


if __name__ == "__main__":
    game = Game()
    game.update()
