import pygame
import Engine
from AI import AI


class UserInterface():
    def __init__(self) -> None:        
        self.HEIGHT = 640
        self.WIDTH = 640        
        self.GRID_SIZE = self.HEIGHT/8

        self.game = Engine.Game()


    def draw_board(self, _WINDOW) -> None:
        """
        Draws an 8*8 board
        """
        for row in range(0, 8):
            for column in range(0, 8):
                if (row+column) %  2 == 0:
                    pygame.draw.rect(_WINDOW, (118,150,86), pygame.Rect(column*self.GRID_SIZE, row*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))
                else:
                    pygame.draw.rect(_WINDOW, (238,238,210), pygame.Rect(column*self.GRID_SIZE, row*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))
        return

    def draw_pieces(self, _WINDOW, _board : list) -> None:
        """
        Draw pieces on board
        """
        for r in range(0, 8):
            for c in range(0, 8):
                if type(_board[r][c]) != str:
                    # self.draw_piece(self.WINDOW, self.pieces_board[r][c], [c, r]) 
                    image = pygame.image.load(_board[r][c].image)
                    image = pygame.transform.scale(image, (60, 60))
                    _WINDOW.blit(image, [c*self.GRID_SIZE +10, r*self.GRID_SIZE + 10])
        return

    def controls(self, controls) -> list:
        """
        List with number to get current state and needed data adequately.
        0:nothing
        1:piece is chosen
        2: move is chosen
        """
        if pygame.mouse.get_pressed()[0]:
            # Get square
            for i in range(0, 8):
                if pygame.mouse.get_pos()[0] - (40+80*i) < 40:
                    column = i
                    break
            for i in range(0, 8):
                if pygame.mouse.get_pos()[1] - (40+80*i) < 40:
                    row = i
                    break          
            chosen_piece = self.game.pieces_board[row][column]
            # Check if what is chosen is a right piece
            if type(chosen_piece) != str and self.current_color == chosen_piece.color:
                available_moves = chosen_piece.find_moves(self.game.board, [row, column])
                return [1, available_moves, [row, column]]
            # check if what is chosen is an available move
            elif controls[0] == 1:
                for move in controls[1]:
                    if [row, column] == move[0]:                        
                        piece = self.game.pieces_board[controls[2][0]][controls[2][1]]
                        if type(self.game.pieces_board[move[0][0]][move[0][1]]) != str:
                            self.game.eat(controls[2], move[0])
                        else:
                            self.game.move(controls[2], move[0])
                        piece.moves += 1    
                        if self.current_color == "w"                    :
                            self.current_color = "b"
                        else:
                            self.current_color="w"
                        return [0]
            else:
                return [0] # No piece have been clicked on

        elif controls[0] == 1: # Show available moves
            for move in controls[1]:
                    pygame.draw.circle(self.WINDOW, [255, 0, 50], [int(self.GRID_SIZE/2) + move[0][1]*self.GRID_SIZE, int(self.GRID_SIZE/2) + move[0][0]*self.GRID_SIZE], 10)
            return controls
        
        return [0]

    def main_loop(self) -> None:
        """
        Main UI loop, pygame loop
        """
        # Initialisation
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()
        controls = [0]
        self.current_color = "w"
        self.bot = AI('b', 10)

        playing = True
        while playing:
            # Draw the board
            self.draw_board(self.WINDOW)

            # Draw the pieces on board
            self.draw_pieces(self.WINDOW, self.game.pieces_board)         

            # Get the mouse controls
            if self.current_color == 'w':
                controls = self.controls(controls)
            else:
                previous, next = self.bot.move(self.game.board)
                if type(self.game.pieces_board[next[0]][next[1]]) == str:
                    self.game.move(previous, next)
                else:
                    self.game.eat(previous, next)
                self.current_color = "w"

            clock.tick(60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False

        return

ui = UserInterface()
ui.main_loop()
