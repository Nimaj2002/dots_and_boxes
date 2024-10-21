import sys
import importlib.util
import subprocess

def run_agent(file_path, game_id, player_name, server_url, port):
    # Run the agent script as a separate process
    subprocess.Popen([sys.executable, file_path, server_url, port, str(game_id), player_name])

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python agent_wrapper.py <file_path> <game_id> <player_name> <server_url> <port>")
        sys.exit(1)

    file_path = sys.argv[1]
    game_id = sys.argv[2]  # Keep as string, will be parsed in the agent script
    player_name = sys.argv[3]
    server_url = sys.argv[4]
    port = sys.argv[5]

    run_agent(file_path, game_id, player_name, server_url, port)