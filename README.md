# Dots and Boxes Game Documentation

## Overview

A Django-based web application implementing the classic Dots and Boxes game, supporting multiple play modes including Player vs Player (PVP), Player vs Agent (PVA), and Agent vs Agent (AVA).

## Features

### 1. Multiple Game Modes

- Player vs Player (PVP)
- Player vs Agent (PVA)
- Agent vs Agent (AVA)

### 2. Interactive Game Board

- Real-time updates
- Click-to-play interface
- Visual feedback for moves
- Score tracking

### 3. Agent Integration

- Support for custom agent uploads
- REST API for agent communication
- Agent wrapper for running custom implementations

## API Endpoints

### Game State

- **Endpoint**: `/api/game/<game_id>/state/`
- **Method**: GET
- **Response**: Current game state including board, scores, and current player

### Make Move

- **Endpoint**: `/api/game/<game_id>/move/`
- **Method**: POST
- **Payload**:

```json
{
    "name": "agent_name",
    "row": row_number,
    "col": column_number
}
```

## Installation

1. Clone the repository
2. create a virtual environment (recomended)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

## Game Rules

1. Players take turns connecting dots with horizontal or vertical lines
2. When a player completes a box, they:
   - Get a point
   - Get another turn
3. Game ends when all boxes are completed
4. Player with the most boxes wins

## Technical Details

### Board DataStructure

- 5x5 grid
- Special characters:

  - `.` : Dots
  - `+` : Empty lines
  - `-` : Horizontal lines
  - `|` : Vertical lines
  - `A-Z` : Completed boxes (first letter of player's name)

- Empty board:

```python
[
    [".", "+", ".", "+", ".", "+", ".", "+", "."],
    ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
    [".", "+", ".", "+", ".", "+", ".", "+", "."],
    ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
    [".", "+", ".", "+", ".", "+", ".", "+", "."],
    ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
    [".", "+", ".", "+", ".", "+", ".", "+", "."],
    ["+", " ", "+", " ", "+", " ", "+", " ", "+"],
    [".", "+", ".", "+", ".", "+", ".", "+", "."],
]
```

! in player vs agent mode after agents move you need to update the website !

### Dependencies

- Django 5.1.2
- Django REST Framework 3.15.2
- Python Requests 2.32.3
- Additional dependencies listed in requirements.txt

## License

MIT License (Copyright (c) 2024 Nima Jelodari)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Submit a pull request

## Future Improvements

1. Implement more sophisticated AI agents
2. Add agent vs agent support
3. Improve UI/UX
4. Add tournament mode
5. Implement replay functionality

For more information or to report issues, please visit the project repository.
