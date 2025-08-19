import pygame
import sys
import os
from engine import GameState

class ChessPiece:
    def __init__(self, image, piece_type, color, x, y):
        self.image = image
        self.piece_type = piece_type
        self.color = color  # 'white' or 'black'
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * 75, y * 75)  # 75 is tile size
        self.is_hovered = False

def load_chess_pieces():
    """Load all chess piece images and return a dictionary"""
    pieces = {}
    pieces_dir = "pieces"
    
    # Define piece types and their file names
    piece_files = {
        'wK': 'wK.png', 'bK': 'bK.png',  # Kings
        'wQ': 'wQ.png', 'bQ': 'bQ.png',  # Queens
        'wR': 'wR.png', 'bR': 'bR.png',  # Rooks
        'wB': 'wB.png', 'bB': 'bB.png',  # Bishops
        'wN': 'wN.png', 'bN': 'bN.png',  # Knights
        'wp': 'wp.png', 'bp': 'bp.png'   # Pawns
    }
    
    for piece_key, filename in piece_files.items():
        filepath = os.path.join(pieces_dir, filename)
        try:
            image = pygame.image.load(filepath)
            # Scale the image to fit the tile size (75x75)
            image = pygame.transform.scale(image, (75, 75))
            pieces[piece_key] = image
        except pygame.error as e:
            print(f"Could not load {filepath}: {e}")
    
    return pieces

def draw_chess_board(screen, board_size=600, tile_size=75, offset_x=200, offset_y=60):
    """Draw a chess board with alternating grey and white tiles and shading"""
    colors = [(240, 240, 240), (128, 128, 128)]  # White and grey
    
    for row in range(8):
        for col in range(8):
            # Alternate colors for chess board pattern
            color_index = (row + col) % 2    # formula to define current color on grid
            color = colors[color_index]      # set color to current color
            
            # Calculate position
            x = col * tile_size + offset_x
            y = row * tile_size + offset_y
            
            # Draw the main tile
            pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
            
            # Add shading - darker top-left corner
            shade_color = (color[0] - 20, color[1] - 20, color[2] - 20)
            shade_points = [(x, y), (x + tile_size//4, y), (x + tile_size//4, y + tile_size//4), (x, y + tile_size//4)]
            pygame.draw.polygon(screen, shade_color, shade_points)

def draw_coordinates(screen, offset_x=200, offset_y=60, tile_size=75):
    """Draw coordinate labels inside the board border"""
    font = pygame.font.SysFont('arial', 16)
    
    # Letters along bottom (a-h) - inside the board border
    for col in range(8):
        letter = chr(ord('a') + col)
        letter_surface = font.render(letter, True, (0, 0, 0))
        letter_rect = letter_surface.get_rect(center=(offset_x + col * tile_size + tile_size//2, offset_y + 8 * tile_size + 15))
        screen.blit(letter_surface, letter_rect)
    
    # Letters along top (a-h) - inside the board border
    for col in range(8):
        letter = chr(ord('a') + col)
        letter_surface = font.render(letter, True, (0, 0, 0))
        letter_rect = letter_surface.get_rect(center=(offset_x + col * tile_size + tile_size//2, offset_y - 15))
        screen.blit(letter_surface, letter_rect)
    
    # Numbers along left side (1-8) - inside the board border
    for row in range(8):
        number = str(8 - row)
        number_surface = font.render(number, True, (0, 0, 0))
        number_rect = number_surface.get_rect(center=(offset_x - 15, offset_y + row * tile_size + tile_size//2))
        screen.blit(number_surface, number_rect)
    
    # Numbers along right side (1-8) - inside the board border
    for row in range(8):
        number = str(8 - row)
        number_surface = font.render(number, True, (0, 0, 0))
        number_rect = number_surface.get_rect(center=(offset_x + 8 * tile_size + 15, offset_y + row * tile_size + tile_size//2))
        screen.blit(number_surface, number_rect)

def check_hover(mouse_pos, game_state, offset_x=200, offset_y=60):
    """Check if mouse is hovering over any piece and return the hovered piece info"""
    mouse_x, mouse_y = mouse_pos
    tile_size = 75
    
    # Adjust mouse position for board offset
    adjusted_mouse_x = mouse_x - offset_x
    adjusted_mouse_y = mouse_y - offset_y
    
    for row in range(8):
        for col in range(8):
            piece = game_state.board[row][col]
            if piece != "--":  # If there's a piece on this square
                # Check if this piece belongs to the current player
                if (game_state.white_to_move and piece[0] == 'w') or (not game_state.white_to_move and piece[0] == 'b'):
                    piece_x = col * tile_size
                    piece_y = row * tile_size
                    
                    # Check if mouse is within the piece bounds
                    if (piece_x <= adjusted_mouse_x <= piece_x + tile_size and 
                        piece_y <= adjusted_mouse_y <= piece_y + tile_size):
                        return piece, (row, col)
    
    return None, None

def get_clicked_square(mouse_pos, offset_x=200, offset_y=60):
    """Convert mouse position to board coordinates"""
    mouse_x, mouse_y = mouse_pos
    tile_size = 75
    
    # Adjust mouse position for board offset
    adjusted_mouse_x = mouse_x - offset_x
    adjusted_mouse_y = mouse_y - offset_y
    
    col = adjusted_mouse_x // tile_size
    row = adjusted_mouse_y // tile_size
    
    if 0 <= row < 8 and 0 <= col < 8:
        return row, col
    return None

def draw_possible_moves(screen, possible_moves, tile_size=75, offset_x=200, offset_y=60):
    """Draw indicators for possible moves"""
    for move in possible_moves:
        # Draw a semi-transparent circle for possible moves
        center_x = move.end_col * tile_size + tile_size // 2 + offset_x
        center_y = move.end_row * tile_size + tile_size // 2 + offset_y
        
        # Create a surface for the circle with alpha
        circle_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (0, 255, 0, 128), (tile_size//2, tile_size//2), 15)
        screen.blit(circle_surface, (move.end_col * tile_size + offset_x, move.end_row * tile_size + offset_y))

def draw_selected_piece(screen, selected_pos, tile_size=75, offset_x=200, offset_y=60):
    """Highlight the selected piece"""
    if selected_pos:
        row, col = selected_pos
        x = col * tile_size + offset_x
        y = row * tile_size + offset_y
        
        # Draw a yellow border around the selected piece
        pygame.draw.rect(screen, (255, 255, 0), (x, y, tile_size, tile_size), 3)

def draw_side_panels(screen, game_state, pieces, captured_pieces=None):
    """Draw side panels showing captured pieces and turn indicator"""
    if captured_pieces is None:
        captured_pieces = {'w': [], 'b': []}
    
    # Left panel (captured white pieces) - full height from turn indicator to bottom
    left_panel_rect = pygame.Rect(0, 60, 220, 620)
    pygame.draw.rect(screen, (50, 50, 50), left_panel_rect)
    pygame.draw.rect(screen, (100, 100, 100), left_panel_rect, 3)
    
    # Right panel (captured black pieces) - full height from turn indicator to bottom
    right_panel_rect = pygame.Rect(880, 60, 220, 620)
    pygame.draw.rect(screen, (50, 50, 50), right_panel_rect)
    pygame.draw.rect(screen, (100, 100, 100), right_panel_rect, 3)
    
    # Draw captured pieces - adjusted y position
    draw_captured_pieces(screen, captured_pieces['b'], (10, 140), pieces)  # Left panel (captured white pieces)
    draw_captured_pieces(screen, captured_pieces['w'], (890, 140), pieces)  # Right panel (captured black pieces)

def draw_captured_pieces(screen, captured_pieces, start_pos, pieces, piece_size=40):
    """Draw captured pieces in a grid layout"""
    x, y = start_pos
    pieces_per_row = 4
    
    for i, piece_code in enumerate(captured_pieces):
        if piece_code in pieces:
            # Calculate position in grid
            grid_x = x + (i % pieces_per_row) * (piece_size + 5)
            grid_y = y + (i // pieces_per_row) * (piece_size + 5)
            
            # Scale piece to smaller size for captured pieces
            scaled_piece = pygame.transform.scale(pieces[piece_code], (piece_size, piece_size))
            screen.blit(scaled_piece, (grid_x, grid_y))

def draw_pieces(screen, pieces, game_state, hovered_piece=None, hovered_pos=None, offset_x=200, offset_y=60):
    """Draw all chess pieces on the board with hover effect"""
    for row in range(8):
        for col in range(8):
            piece = game_state.board[row][col]
            if piece != "--" and piece in pieces:  # If there's a piece and we have its image
                # Check if this piece is being hovered
                is_hovered = (piece == hovered_piece and (row, col) == hovered_pos)
                
                if is_hovered:
                    # Scale up the piece slightly when hovered
                    scaled_image = pygame.transform.scale(pieces[piece], (85, 85))
                    # Center the scaled image on the tile
                    draw_x = col * 75 - 5 + offset_x  # Offset by 5 pixels to center
                    draw_y = row * 75 - 5 + offset_y
                else:
                    # Draw normal size
                    scaled_image = pieces[piece]
                    draw_x = col * 75 + offset_x
                    draw_y = row * 75 + offset_y
                
                screen.blit(scaled_image, (draw_x, draw_y))

def draw_turn_indicator(screen, game_state):
    """Draw the turn indicator in a dedicated rectangle at the top"""
    # Draw turn indicator background rectangle
    turn_rect = pygame.Rect(0, 0, 1100, 60)
    pygame.draw.rect(screen, (40, 40, 40), turn_rect)
    pygame.draw.rect(screen, (150, 150, 150), turn_rect, 2)
    
    # Draw turn text
    font = pygame.font.SysFont('arial', 36)
    turn_text = "White's Turn" if game_state.white_to_move else "Black's Turn"
    turn_color = (255, 255, 0) if game_state.white_to_move else (255, 255, 255)
    turn_surface = font.render(turn_text, True, turn_color)
    turn_text_rect = turn_surface.get_rect(center=(550, 30))  # Center at x=550 (middle of 1100px window)
    screen.blit(turn_surface, turn_text_rect)

def main():
    pygame.init()
    
    # Set up the display (wider to accommodate side panels and board border)
    board_size = 600
    window_width = 1100  # 200 + 640 + 200 (640 for board + border)
    window_height = 680  # 60 for turn indicator + 620 for board + border
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Chess")
    
    # Calculate tile size and board offset
    tile_size = board_size // 8
    board_offset_x = 220  # Offset to center the board with room for border
    board_offset_y = 60   # Offset for turn indicator
    
    # Load chess pieces
    pieces = load_chess_pieces()
    
    # Create game state (this uses the same board as engine.py)
    game_state = GameState()
    
    # Game state variables
    selected_piece = None
    selected_pos = None
    possible_moves = []
    captured_pieces = {'w': [], 'b': []}  # Track captured pieces
    
    clock = pygame.time.Clock()
    running = True

    while running:
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Check for hover
        hovered_piece, hovered_pos = check_hover(mouse_pos, game_state, board_offset_x, board_offset_y)
        
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    clicked_square = get_clicked_square(mouse_pos, board_offset_x, board_offset_y)
                    if clicked_square:
                        row, col = clicked_square
                        piece = game_state.board[row][col]
                        
                        if selected_piece is None:
                            # Select a piece
                            if piece != "--":
                                # Check if it's the current player's piece
                                if (game_state.white_to_move and piece[0] == 'w') or (not game_state.white_to_move and piece[0] == 'b'):
                                    selected_piece = piece
                                    selected_pos = (row, col)
                                    # Get possible moves for this piece
                                    possible_moves = game_state.get_piece_moves(row, col, piece)
                        else:
                            # Check if clicking on a possible move
                            move_made = False
                            for move in possible_moves:
                                if move.end_row == row and move.end_col == col:
                                    # Execute the move
                                    captured_piece = game_state.make_move(move)
                                    
                                    # Add captured piece to the list if there was one
                                    if captured_piece:
                                        if captured_piece[0] == 'w':  # White piece was captured
                                            captured_pieces['w'].append(captured_piece)
                                        else:  # Black piece was captured
                                            captured_pieces['b'].append(captured_piece)
                                    
                                    print(f"Move from ({selected_pos[0]}, {selected_pos[1]}) to ({row}, {col})")
                                    if captured_piece:
                                        print(f"Captured: {captured_piece}")
                                    
                                    # Clear selection after move
                                    selected_piece = None
                                    selected_pos = None
                                    possible_moves = []
                                    
                                    move_made = True
                                    break
                            
                            # If not a valid move, select the new piece if it's the current player's
                            if not move_made:
                                if piece != "--":
                                    if (game_state.white_to_move and piece[0] == 'w') or (not game_state.white_to_move and piece[0] == 'b'):
                                        selected_piece = piece
                                        selected_pos = (row, col)
                                        possible_moves = game_state.get_piece_moves(row, col, piece)
                                    else:
                                        selected_piece = None
                                        selected_pos = None
                                        possible_moves = []
                                else:
                                    selected_piece = None
                                    selected_pos = None
                                    possible_moves = []

        # Fill the screen with a background color
        screen.fill((255, 255, 255))  # White background
        
        # Draw turn indicator first
        draw_turn_indicator(screen, game_state)
        
        # Draw side panels
        draw_side_panels(screen, game_state, pieces, captured_pieces)
        
        # Draw the chess board border first (so it's behind the board)
        border_rect = pygame.Rect(board_offset_x - 2, board_offset_y - 2, board_size + 4, board_size + 4)
        pygame.draw.rect(screen, (0, 0, 0), border_rect, 2)
        
        # Draw the chess board
        draw_chess_board(screen, board_size, tile_size, board_offset_x, board_offset_y)
        
        # Draw coordinates
        draw_coordinates(screen, board_offset_x, board_offset_y, tile_size)
        
        # Draw possible moves
        draw_possible_moves(screen, possible_moves, tile_size, board_offset_x, board_offset_y)
        
        # Draw selected piece highlight
        draw_selected_piece(screen, selected_pos, tile_size, board_offset_x, board_offset_y)
        
        # Draw the pieces with hover effect
        draw_pieces(screen, pieces, game_state, hovered_piece, hovered_pos, board_offset_x, board_offset_y)

        # Update the display
        pygame.display.flip()
        
        # Limit FPS to 60
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

                
                
