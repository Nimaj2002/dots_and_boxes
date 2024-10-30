import requests
import time
import random
import sys

class RowFirstAgent:
    def __init__(self, server_url, game_id, player_name):
        self.server_url = server_url
        self.game_id = game_id
        self.player_name = player_name

    def get_game_state(self):
        url = f"{self.server_url}/api/game/{self.game_id}/state/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting game state: {response.status_code}")
            return None

    def make_move(self, row, col):
        url = f"{self.server_url}/api/game/{self.game_id}/move/"
        data = {
            "name": self.player_name,
            "row": row,
            "col": col
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error making move: {response.status_code}")
            return None

    def get_valid_moves(self, board):
        horizontal_moves = []
        other_moves = []
        
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == '+':
                    # Check if it's a horizontal line (odd row, even column)
                    if i % 2 == 1 and j % 2 == 0:
                        horizontal_moves.append((i, j))
                    else:
                        other_moves.append((i, j))
        
        return horizontal_moves, other_moves

    def play_game(self):
        while True:
            game_state = self.get_game_state()
            if not game_state:
                break

            if game_state['player1_score'] + game_state['player2_score'] == 16:
                print(f"Game over! Winner: {game_state['player1_name'] if game_state['player1_score'] > game_state['player2_score'] else game_state['player2_name']}")
                break

            if game_state['current_player'] == self.player_name:
                horizontal_moves, other_moves = self.get_valid_moves(game_state['board'])
                
                # Prioritize horizontal moves
                if horizontal_moves:
                    row, col = random.choice(horizontal_moves)
                elif other_moves:
                    row, col = random.choice(other_moves)
                else:
                    print("No valid moves available")
                    break
                
                print(f"Making move: row {row}, col {col}")
                self.make_move(row, col)
            else:
                print("Waiting for opponent's move...")
                time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python row_first_agent.py <server_url> <port> <game_id> <player_name>")
        sys.exit(1)

    server_url = sys.argv[1]
    game_id = int(sys.argv[3])
    player_name = sys.argv[4]

    full_server_url = f"{server_url}"
    agent = RowFirstAgent(full_server_url, game_id, player_name)
    agent.play_game() 