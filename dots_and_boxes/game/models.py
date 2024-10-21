from django.db import models
import json
import logging

logger = logging.getLogger(__name__)

class Game(models.Model):
    GAME_MODES = [
        ('PVP', 'Player vs Player'),
        ('PVA', 'Player vs Agent'),
        ('AVA', 'Agent vs Agent'),
    ]

    mode = models.CharField(max_length=3, choices=GAME_MODES)

    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    player1_is_agent = models.BooleanField(default=False)
    player2_is_agent = models.BooleanField(default=False)
    
    player1_moves = models.TextField(default='[]')
    player2_moves = models.TextField(default='[]')

    agent_file = models.FileField(upload_to='agent_files/', null=True, blank=True)
    agent1_file = models.FileField(upload_to='agent_files/', null=True, blank=True)
    agent2_file = models.FileField(upload_to='agent_files/', null=True, blank=True)

    current_player = models.CharField(max_length=100)
    winner = models.CharField(max_length=100, null=True, blank=True)
    board = models.TextField(default='')

    def is_current_player_agent(self):
        return (self.current_player == self.player1 and self.player1_is_agent) or \
               (self.current_player == self.player2 and self.player2_is_agent)

    def get_player1_moves(self):
        return json.loads(self.player1_moves)

    def get_player2_moves(self):
        return json.loads(self.player2_moves)
    
    def add_move(self, row, col):
        logger.info(f"Adding move for {self.current_player}: ({row}, {col})")
        if self.current_player == self.player1:
            moves = None
            moves = self.get_player1_moves()
            moves.append([row, col])
            self.player1_moves = json.dumps(moves)
            print(f"Updated moves for {self.player1}: {moves}")
        elif self.current_player == self.player2:
            moves = None
            moves = self.get_player2_moves()
            moves.append([row, col])
            self.player2_moves = json.dumps(moves)
            print(f"Updated moves for {self.player2}: {moves}")
        else:
            print(f"Attempted to add move for unknown player: {self.current_player}")
        self.save()

    def clear_moves(self):
        self.player1_moves = '[]'
        self.player2_moves = '[]'
        self.save()

    def save(self, *args, **kwargs):
        if not self.board:
            self.board = json.dumps([
                [".", "+", ".", "+", ".", "+", ".", "+", "."],
                ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
                [".", "+", ".", "+", ".", "+", ".", "+", "."],
                ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
                [".", "+", ".", "+", ".", "+", ".", "+", "."],
                ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
                [".", "+", ".", "+", ".", "+", ".", "+", "."],
                ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
                [".", "+", ".", "+", ".", "+", ".", "+", "."],
            ])
        if not self.current_player:
            self.current_player = self.player1
        super().save(*args, **kwargs)

    def get_board(self):
        return json.loads(self.board)

    def set_board(self, new_board):
        self.board = json.dumps(new_board)

    def make_move(self, row, col):
        board = self.get_board()
        logger.info(f"Making move at ({row}, {col})")
        if board[row][col] == "+":
            if board[row][0] == ".":
                board[row][col] = "-"
            else:
                board[row][col] = "|"    
            
            self.set_board(board)  # Update the board after making the move
            
            # Add the move to the current player's moves
            self.add_move(row, col)
            
            boxes_completed = self.check_boxes_completed(row, col)
            logger.info(f"Boxes completed: {boxes_completed}")
            if not boxes_completed:
                self.switch_player()
            self.save()
            
            # Log the updated moves after the move is made
            print(f"Player 1 moves: {self.get_player1_moves()}")
            print(f"Player 2 moves: {self.get_player2_moves()}")
            
            return True
        return False

    def check_boxes_completed(self, row, col):
        board = self.get_board()
        boxes_completed = 0

        def is_valid_index(r, c):
            return 0 <= r < len(board) and 0 <= c < len(board[0])
        
        if board[row][col] == "-":
        # Check box above
            if (is_valid_index(row-1, col) and is_valid_index(row-1, col-1) and is_valid_index(row-1, col+1) and
                is_valid_index(row-2, col)):
                if (board[row-1][col-1] == "|" and board[row-1][col+1] == "|" and board[row-2][col] == "-" and
                    board[row-1][col] == " "):
                    board[row-1][col] = self.current_player[0].upper()
                    boxes_completed += 1
                    
                    if self.current_player == self.player1:
                        self.player1_score += 1
                    elif self.current_player == self.player2:
                        self.player2_score += 1


            # Check box below
            if (is_valid_index(row+1, col) and is_valid_index(row+1, col-1) and is_valid_index(row+1, col+1) and
                is_valid_index(row+2, col)):
                if (board[row+1][col-1] == "|" and board[row+1][col+1] == "|" and board[row+2][col] == "-" and
                    board[row+1][col] == " "):
                    board[row+1][col] = self.current_player[0].upper()
                    boxes_completed += 1

                    if self.current_player == self.player1:
                        self.player1_score += 1
                    elif self.current_player == self.player2:
                        self.player2_score += 1

        elif board[row][col] == "|":
            # Check box to the left
            if (is_valid_index(row, col-1) and is_valid_index(row-1, col-1) and is_valid_index(row+1, col-1) and
                is_valid_index(row, col-2)):
                if (board[row-1][col-1] == "-" and board[row+1][col-1] == "-" and board[row][col-2] == "|" and
                    board[row][col-1] == " "):
                    board[row][col-1] = self.current_player[0].upper()
                    boxes_completed += 1

                    if self.current_player == self.player1:
                        self.player1_score += 1
                    elif self.current_player == self.player2:
                        self.player2_score += 1


            # Check box to the right
            if (is_valid_index(row, col+1) and is_valid_index(row-1, col+1) and is_valid_index(row+1, col+1) and
                is_valid_index(row, col+2)):
                if (board[row-1][col+1] == "-" and board[row+1][col+1] == "-" and board[row][col+2] == "|" and
                    board[row][col+1] == " "):
                    board[row][col+1] = self.current_player[0].upper()
                    boxes_completed += 1

                    if self.current_player == self.player1:
                        self.player1_score += 1
                    elif self.current_player == self.player2:
                        self.player2_score += 1

        self.set_board(board)
        return boxes_completed > 0

    def is_box_completed(self, row, col):
        board = self.get_board()
        if 0 <= row < len(board) and 0 <= col < len(board[0]):
            if row % 2 == 1 and col % 2 == 1:
                return (board[row-1][col] != "+" and
                        board[row+1][col] != "+" and
                        board[row][col-1] != "+" and
                        board[row][col+1] != "+")
        return False

    def switch_player(self):
        old_player = self.current_player
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        logger.info(f"Switched player from {old_player} to {self.current_player}")

    def check_game_over(self):
        board = self.get_board()
        for row in board:
            if "+" in row:
                return False
        return True

    def get_winner(self):
        board = self.get_board()
        p1_score = sum(row.count(self.player1[0].upper()) for row in board)
        p2_score = sum(row.count(self.player2[0].upper()) for row in board)
        if p1_score > p2_score:
            return self.player1
        elif p2_score > p1_score:
            return self.player2
        else:
            return "Tie"

    def initialize_board(self):
        self.board = json.dumps([
            [".", "+", ".", "+", ".", "+", ".", "+", "."],
            ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
            [".", "+", ".", "+", ".", "+", ".", "+", "."],
            ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
            [".", "+", ".", "+", ".", "+", ".", "+", "."],
            ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
            [".", "+", ".", "+", ".", "+", ".", "+", "."],
            ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
            [".", "+", ".", "+", ".", "+", ".", "+", "."],
        ])

    def __str__(self):
        return f"{self.mode} - {self.player1} vs {self.player2}"
    
    def print_game_state(self):
        board = self.get_board()
        player1_moves = self.get_player1_moves()
        player2_moves = self.get_player2_moves()

        print("\nCurrent Game State:")
        print("------------------")
        
        # Print the board
        for row in board:
            print(" ".join(cell if cell != " " else "_" for cell in row))
        
        print("\nPlayer Moves:")
        print(f"{self.player1} (moves: {len(player1_moves)}):")
        for move in player1_moves:
            print(f"  Row: {move[0]}, Column: {move[1]}")
        
        print(f"\n{self.player2} (moves: {len(player2_moves)}):")
        for move in player2_moves:
            print(f"  Row: {move[0]}, Column: {move[1]}")
        
        print(f"\nCurrent Player: {self.current_player}")
        print(f"Scores - {self.player1}: {self.player1_score}, {self.player2}: {self.player2_score}")
        
        if self.winner:
            print(f"Winner: {self.winner}")
        
        print("------------------") 