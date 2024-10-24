import os
import cv2
import numpy as np
import logging
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit
import heapq
import eventlet

eventlet.monkey_patch()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=True,
    engineio_logger=True,
    ping_timeout=600,  # Increase timeout to 300 seconds
    ping_interval=60,  # Ping interval every 60 seconds
    max_http_buffer_size=50000000  # Increase buffer size for larger mazes
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    logging.debug("Rendering index page.")
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.debug("Handling file upload.")
    if 'file' not in request.files:
        logging.error("No file part found in request.")
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        logging.error("No file selected for upload.")
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        logging.debug(f"Saving file to {file_path}.")
        file.save(file_path)
        return redirect(url_for('solve_maze', filename=file.filename))

@app.route('/solve/<filename>')
def solve_maze(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    logging.debug(f"Processing maze from file: {file_path}")
    maze = process_maze(file_path)
    return render_template('maze_solution.html', filename=filename, maze=maze.tolist())

def process_maze(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_maze = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    logging.debug("Maze image processed into binary array.")
    return (binary_maze // 255).astype(np.uint8)

@socketio.on('start_bfs')
def handle_start_bfs(data):
    logging.debug("WebSocket event 'start_bfs' received.")
    try:
        maze = np.array(data['maze'])
        start = tuple(map(int, data['start']))
        end = tuple(map(int, data['end']))

        logging.debug(f"Start: {start}, End: {end}, Maze Shape: {maze.shape}")

        with app.app_context():
            eventlet.spawn(a_star_maze_solver, maze, start, end)
    except Exception as e:
        logging.error(f"Error in handle_start_bfs: {str(e)}")
        socketio.emit('error', {'message': f'Error: {str(e)}'})

def a_star_maze_solver(maze, start, end):
    logging.debug(f"Starting A* search from {start} to {end} in maze of shape {maze.shape}")

    # Validate start and end points
    if not (0 <= start[0] < maze.shape[0] and 0 <= start[1] < maze.shape[1]):
        logging.error(f"Invalid start point: {start}")
        socketio.emit('error', {'message': 'Invalid start point'})
        return

    if not (0 <= end[0] < maze.shape[0] and 0 <= end[1] < maze.shape[1]):
        logging.error(f"Invalid end point: {end}")
        socketio.emit('error', {'message': 'Invalid end point'})
        return

    if maze[start[0]][start[1]] != 0 or maze[end[0]][end[1]] != 0:
        logging.error("Start or end point is on a wall")
        socketio.emit('error', {'message': 'Start or end point must be on a path'})
        return

    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {start: None}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    explored = set()
    step_count = 0  # Track the number of steps

    while open_list:
        current_f, current = heapq.heappop(open_list)

        if current == end:
            path = reconstruct_path(came_from, start, end)
            logging.debug(f"Path found with length {len(path)}")
            socketio.emit('final_path', path)
            return

        if current in explored:
            continue

        explored.add(current)

        # Iterate over neighbors and check all directions
        for neighbor in get_neighbors(maze, current):
            if neighbor in explored:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

                step_count += 1

                # Emit exploration updates less frequently
                if step_count % 100 == 0:  # Emit every 100 steps
                    socketio.emit('explore_path', {'start': current, 'end': neighbor})

                # Yield control every 100 steps to keep the event loop responsive
                if step_count % 100 == 0:
                    eventlet.sleep(0)

    logging.debug("No path found")
    socketio.emit('no_path', {})


def heuristic(a, b):
    # Use Manhattan distance as the heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(maze, pos):
    row, col = pos
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dy, dx in directions:
        new_row, new_col = row + dy, col + dx
        if (0 <= new_row < maze.shape[0] and 
            0 <= new_col < maze.shape[1] and 
            maze[new_row][new_col] == 0):  # Check if it's a path
            neighbors.append((new_row, new_col))

    return neighbors

def reconstruct_path(came_from, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]  # Return the path from start to end

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
