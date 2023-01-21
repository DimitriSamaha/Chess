from random import randint
from stockfish import Stockfish


class AI:
    def __init__(self, _color : str, _level : int) -> None:
        # Set chess engine         
        self.stockfish = Stockfish(path="C:\Python310\Lib\site-packages\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
        self.color = _color
        self.stockfish.set_skill_level(_level)



    def convert_to_fen(self, _board : list, _color : str) -> str:
        """
        Converts chess board from list to fen notation for stokfish modules
        """
        fen = ''
        for r in range(0, 8):
            i = 0
            for c in range(0, 8):
                if _board[r][c][1] == '-':
                    i += 1
                else:
                    if i != 0:
                        fen += str(i)
                        i = 0
                    if _board[r][c][0] == "w":
                        fen += _board[r][c][1].upper()
                    else:
                        fen += _board[r][c][1].lower()
            if i !=0:
                fen += str(i)
                i = 0
            fen += "/"

        fen = fen[:-1] + f" {_color}  - - 0 1"
        return fen


    def move(self, _board : list) -> list:
        letter = 'abcdefgh'        
        self.stockfish.set_fen_position(self.convert_to_fen(_board, self.color))
        move = randint(0, 4)
        dict_move = self.stockfish.get_top_moves()[move]
        move = dict_move['Move']
        previous = [8-int(move[1]), letter.index(move[0])]
        move = [8-int(move[3]), letter.index(move[2])]
        return [previous, move]

board = [    
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP' , 'bP' , 'bP' , 'bP', 'bP', 'bP' , 'bP' , 'bP' ],
        [' -' , ' -' , ' -' , ' -' , ' -', ' -' , ' -' , ' -' ],
        [' -' , 'wP' , ' -' , ' -' , ' -', ' -' , ' -' , ' -' ],
        [' -' , ' -' , ' -' , ' -' , ' -', ' -' , ' -' , ' -' ],
        [' -' , ' -' , ' -' , ' -' , ' -', ' -' , ' -' , ' -' ],
        ['wP' , ' -' , 'wP' , 'wP', 'wP', 'wP' , 'wP' , 'wP' ],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]


if __name__ == "__main__":
    bot = AI('b', 10)
    print(bot.move(board))
