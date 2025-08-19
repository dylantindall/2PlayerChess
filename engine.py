"This will be responsible for handling the logic of the game."

import numpy as np

class GameState():
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bB"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
        self.white_to_move = True
        self.move_log = []

    def get_valid_moves(self):
        """Get all valid moves for the current player"""
        valid_moves = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "--":
                    # Check if this piece belongs to the current player
                    if (self.white_to_move and piece[0] == 'w') or (not self.white_to_move and piece[0] == 'b'):
                        piece_moves = self.get_piece_moves(row, col, piece)
                        valid_moves.extend(piece_moves)
        
        return valid_moves

    def get_piece_moves(self, row, col, piece):
        """Get all possible moves for a specific piece"""
        piece_type = piece[1]  # 'p', 'R', 'N', 'B', 'Q', 'K'
        moves = []
        
        if piece_type == 'p':  # Pawn
            moves = self.get_pawn_moves(row, col, piece[0])
        elif piece_type == 'R':  # Rook
            moves = self.get_rook_moves(row, col, piece[0])
        elif piece_type == 'N':  # Knight
            moves = self.get_knight_moves(row, col, piece[0])
        elif piece_type == 'B':  # Bishop
            moves = self.get_bishop_moves(row, col, piece[0])
        elif piece_type == 'Q':  # Queen
            moves = self.get_queen_moves(row, col, piece[0])
        elif piece_type == 'K':  # King
            moves = self.get_king_moves(row, col, piece[0])
        
        return moves

    def get_pawn_moves(self, row, col, color):
        """TODO: Implement pawn movement logic
        Pawns move forward one square (or two from starting position)
        Pawns capture diagonally
        Consider en passant and pawn promotion
        """
        moves = []
        
        if color == 'w':  # White pawns move up (decreasing row)
            # Forward move (1 square)
            if self.is_valid_position(row - 1, col) and self.is_empty_square(row - 1, col):
                moves.append(Move(row, col, row - 1, col))
                
                # Double move from starting position (row 6)
                if row == 6 and self.is_empty_square(row - 2, col):
                    moves.append(Move(row, col, row - 2, col))
            
            # Diagonal captures
            for col_offset in [-1, 1]:
                new_col = col + col_offset
                if (self.is_valid_position(row - 1, new_col) and 
                    self.is_enemy_piece(row - 1, new_col, color)):
                    moves.append(Move(row, col, row - 1, new_col))
        
        else:  # Black pawns move down (increasing row)
            # Forward move (1 square)
            if self.is_valid_position(row + 1, col) and self.is_empty_square(row + 1, col):
                moves.append(Move(row, col, row + 1, col))
                
                # Double move from starting position (row 1)
                if row == 1 and self.is_empty_square(row + 2, col):
                    moves.append(Move(row, col, row + 2, col))
            
            # Diagonal captures
            for col_offset in [-1, 1]:
                new_col = col + col_offset
                if (self.is_valid_position(row + 1, new_col) and 
                    self.is_enemy_piece(row + 1, new_col, color)):
                    moves.append(Move(row, col, row + 1, new_col))
        
        return moves

    def get_rook_moves(self, row, col, color):
        """TODO: Implement rook movement logic
        Rooks move horizontally and vertically any number of squares
        Cannot jump over other pieces
        """
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        
        for d_row, d_col in directions:
            for i in range(1, 8):
                new_row, new_col = row + i*d_row, col + i*d_col
                if not self.is_valid_position(new_row, new_col):
                    break
                if self.is_empty_square(new_row, new_col):
                    moves.append(Move(row, col, new_row, new_col))
                elif self.is_enemy_piece(new_row, new_col, color):
                    moves.append(Move(row, col, new_row, new_col))
                    break
                else:
                    break  # Friendly piece blocking
        
        return moves

    def get_knight_moves(self, row, col, color):
        """TODO: Implement knight movement logic
        Knights move in L-shape: 2 squares in one direction, then 1 square perpendicular
        Can jump over other pieces
        """
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for d_row, d_col in knight_moves:
            new_row, new_col = row + d_row, col + d_col
            if (self.is_valid_position(new_row, new_col) and 
                (self.is_empty_square(new_row, new_col) or 
                 self.is_enemy_piece(new_row, new_col, color))):
                moves.append(Move(row, col, new_row, new_col))
        
        return moves

    def get_bishop_moves(self, row, col, color):
        """TODO: Implement bishop movement logic
        Bishops move diagonally any number of squares
        Cannot jump over other pieces
        """
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # All diagonals
        
        for d_row, d_col in directions:
            for i in range(1, 8):
                new_row, new_col = row + i*d_row, col + i*d_col
                if not self.is_valid_position(new_row, new_col):
                    break
                if self.is_empty_square(new_row, new_col):
                    moves.append(Move(row, col, new_row, new_col))
                elif self.is_enemy_piece(new_row, new_col, color):
                    moves.append(Move(row, col, new_row, new_col))
                    break
                else:
                    break  # Friendly piece blocking
        
        return moves

    def get_queen_moves(self, row, col, color):
        """TODO: Implement queen movement logic
        Queens combine rook and bishop movements
        """
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),  # Rook directions
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Bishop directions
        
        for d_row, d_col in directions:
            for i in range(1, 8):
                new_row, new_col = row + i*d_row, col + i*d_col
                if not self.is_valid_position(new_row, new_col):
                    break
                if self.is_empty_square(new_row, new_col):
                    moves.append(Move(row, col, new_row, new_col))
                elif self.is_enemy_piece(new_row, new_col, color):
                    moves.append(Move(row, col, new_row, new_col))
                    break
                else:
                    break  # Friendly piece blocking
        
        return moves

    def get_king_moves(self, row, col, color):
        """TODO: Implement king movement logic
        Kings move one square in any direction
        Consider castling
        """
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if (self.is_valid_position(new_row, new_col) and 
                (self.is_empty_square(new_row, new_col) or 
                 self.is_enemy_piece(new_row, new_col, color))):
                moves.append(Move(row, col, new_row, new_col))
        
        return moves

    def make_move(self, move):
        """Execute a move on the board"""
        # Get the piece being moved
        piece = self.board[move.start_row][move.start_col]
        
        # Check if we're capturing a piece
        captured_piece = self.board[move.end_row][move.end_col]
        
        # Move the piece
        self.board[move.end_row][move.end_col] = piece
        self.board[move.start_row][move.start_col] = "--"
        
        # Add move to move log
        self.move_log.append(move)
        
        # Switch turns
        self.white_to_move = not self.white_to_move
        
        # Return captured piece info for display
        return captured_piece if captured_piece != "--" else None

    def is_valid_position(self, row, col):
        """Check if a position is within the board bounds"""
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty_square(self, row, col):
        """Check if a square is empty"""
        return self.board[row][col] == "--"

    def is_enemy_piece(self, row, col, color):
        """Check if a square contains an enemy piece"""
        piece = self.board[row][col]
        if piece == "--":
            return False
        return piece[0] != color

    def is_friendly_piece(self, row, col, color):
        """Check if a square contains a friendly piece"""
        piece = self.board[row][col]
        if piece == "--":
            return False
        return piece[0] == color


class Move():
    def __init__(self, start_row, start_col, end_row, end_col):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        