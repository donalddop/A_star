# A* Pathfinding Visualization

This project is a Python implementation of the A* pathfinding algorithm with a Pygame visualization. The user can draw a maze and watch the algorithm find the shortest path.

## Getting Started

### Prerequisites

* Python 3.x
* pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/donalddop/A_star.git
   cd A_star
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```bash
python a_star.py
```

## Controls

*   **Left Mouse Button:** Draw walls in the grid.
*   **Right Mouse Button:** Erase walls from the grid.
*   **Spacebar:** Start the A* algorithm. The visualization will show the algorithm's progress.
*   **Enter:** Reset the grid to its initial state.

## Docker

You can also run the application using Docker.

1. Build the Docker image:
   ```bash
   docker build -t a-star-pygame .
   ```

2. Run the Docker container:
   ```bash
   docker run -it --rm --name a-star-pygame -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix a-star-pygame
   ```
   
   **Note:** The Docker command for GUI applications can vary depending on your operating system. The command above is for Linux. You might need to adjust it for macOS or Windows.
