# Interactive Maze Solver

This project is an interactive web-based application that allows users to upload a maze image, set start and end points, and visualize the process of solving the maze in real-time using a pathfinding algorithm. The application uses Flask for the backend, Socket.IO for real-time communication, and HTML5 Canvas for front-end visualization.

## Features

- **Upload Maze Images**: Users can upload a maze image in grayscale, where white represents paths and black represents walls.
- **Interactive Point Selection**: Click to set start and end points on the maze.
- **Real-Time Maze Solving**: The maze-solving process is visualized live, showing the exploration and final solution.
- **A* Algorithm**: Uses the A* algorithm to efficiently find the shortest path.
- **Processing Time**: Displays the time taken to solve the maze.

## Demo
*(soon)*

![Maze Solver Demo](demo.gif)

## How It Works

1. **Upload Maze**: The user uploads a maze image, which is processed into a binary representation.
2. **Set Start and End Points**: The user selects a valid starting point and ending point on the maze.
3. **Real-Time Solving**: The algorithm explores the maze, and the progress is visualized in real-time.
4. **Final Path**: If a solution is found, the final path is displayed. If no path is found, the user is notified.

## Technology Stack

- **Backend**:
  - Flask: Web framework for handling requests and rendering pages.
  - Flask-SocketIO: Enables real-time communication between the server and the browser.
  - OpenCV: For image processing and converting the maze to a binary array.
  - Eventlet: For handling asynchronous operations in the server.
- **Frontend**:
  - HTML5 and CSS: For structure and design.
  - JavaScript (with Socket.IO): For interactivity and real-time communication.
  - Canvas: For rendering the maze and drawing the paths.

## Installation

### Prerequisites

- Python 3.7+
- Virtual environment (recommended)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/maze-solver.git
    cd maze-solver
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app:

    ```bash
    python app.py
    ```

5. Access the application in your browser at `http://localhost:5000`.

## Usage

1. **Upload a Maze Image**: Upload a maze in grayscale (white for paths, black for walls).
2. **Click to Set Start and End Points**: Click on valid points (white areas) in the maze to set the start and end points.
3. **Watch the Solver**: The A* algorithm will start solving the maze, and you can see the progress in real-time.
4. **View the Solution**: If the path is found, it will be displayed in gold. The processing time will be displayed below the maze.

## Limitations (to be fixed)
[ ] Fix path finding going around the maze on certain mazes
[ ] Fix the maze resoulution
[ ] Add a cropping feature

## File Structure

```bash
├── app.py                 # Flask application and server-side logic
├── templates/
│   ├── index.html         # Main HTML page for uploading and interacting with the maze
│   ├── maze_solution.html # Page for visualizing the maze solution
├── uploads/               # Directory for storing uploaded maze images
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation
```

## Contributing

Feel free to open issues or submit pull requests if you have any ideas for improvements or want to fix bugs.

## License

This project is licensed under the MIT License.
