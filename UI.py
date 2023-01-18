import pygame
import main


class UserInterface():
    def __init__(self) -> None:        
        self.HEIGHT = 640
        self.WIDTH = 640        
        self.GRID_SIZE = self.HEIGHT/8

        self.game = main.Game()
        self.pieces_board = self.game.pieces_board

    def draw_board(self, _WINDOW):
        for row in range(0, 8):
            for column in range(0, 8):
                if (row+column) %  2 == 0:
                    pygame.draw.rect(_WINDOW, (118,150,86), pygame.Rect(column*self.GRID_SIZE, row*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))
                else:
                    pygame.draw.rect(_WINDOW, (238,238,210), pygame.Rect(column*self.GRID_SIZE, row*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))
        return

    def draw_piece(self, _WINDOW, _piece, _indexes : list) -> None:
        image = pygame.image.load(_piece.image)
        image = pygame.transform.scale(image, (60, 60))
        _WINDOW.blit(image, [_indexes[0]*self.GRID_SIZE +10, _indexes[1]*self.GRID_SIZE + 10])
        return

    def mechanics(self, mechanics):
        """
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
            chosen_piece = self.pieces_board[row][column]
            # Check if what is chosen is a right piece
            if type(chosen_piece) != str and self.current_color == chosen_piece.color:
                available_moves = chosen_piece.find_moves(self.game.board, [row, column])
                return [1, available_moves, [row, column]]
            # check if what is chosen is an available move
            elif mechanics[0] == 1:
                for move in mechanics[1]:
                    if [row, column] == move[0]:                        
                        piece = self.pieces_board[mechanics[2][0]][mechanics[2][1]]
                        if type(self.pieces_board[move[0][0]][move[0][1]]) != str:
                            self.game.eat(mechanics[2], move[0])
                        else:
                            self.game.move(mechanics[2], move[0])
                        piece.moves += 1    
                        if self.current_color == "w"                    :
                            self.current_color = "b"
                        else:
                            self.current_color="w"
                        return [0]
            else:
                return [0] # No piece have been clicked on

        elif mechanics[0] == 1: # Show available moves
            for move in mechanics[1]:
                    pygame.draw.circle(self.WINDOW, [255, 0, 50], [int(self.GRID_SIZE/2) + move[0][1]*self.GRID_SIZE, int(self.GRID_SIZE/2) + move[0][0]*self.GRID_SIZE], 10)
            return mechanics
        
        return [0]

    def main_loop(self):
        playing = True
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()
        mechanics = [0]
        self.current_color = "w"

        while playing:
            # Draw the board
            self.draw_board(self.WINDOW)

            # Draw the pieces on board
            self.pieces_board = self.game.pieces_board
            for r in range(0, 8):
                for c in range(0, 8):
                    if type(self.pieces_board[r][c]) != str:
                        self.draw_piece(self.WINDOW, self.pieces_board[r][c], [c, r])            

            mechanics = self.mechanics(mechanics)

            clock.tick(60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False

        return

ui = UserInterface()
ui.main_loop()
